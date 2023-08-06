import json
import os
import shutil
import traceback
from glob import glob
from os import listdir
from os.path import basename, dirname, splitext
from pathlib import Path
from typing import Callable

import numpy as np
from pymol import cmd as pm
from pymol import colorprinting

from ..capabilities import CAPS
from ..commons import run


def find_ligands(folder: Path) -> [Path]:
    return [
        *(Path(p) for p in glob(str(folder / "*.smi"))),
        *(Path(p) for p in glob(str(folder / "*.sdf"))),
    ]


class ProjectPath:
    def __init__(self, cwd):
        self.cwd = Path(cwd)

    def path(self, *args):
        return Path(self.cwd, *args)


def run_vina_protocol(
    results_folder: Path,
    ligands_folder: Path,
    target_sel: str,
    box_sel: str,
    log_emitter: Callable[[str], None] = lambda *a: None,
    count_emitter: Callable[[int], None] = lambda *a: None,
    total_emitter: Callable[[int], None] = lambda *a: None,
    done_emitter: Callable[[bool], None] = lambda *a: None,
    box_margin: float = 5,
    flex_sel: str = "",
    ligand_ph: float = 7,
    exhaustiveness: int = 8,
    num_modes: int = 9,
    energy_range: float = 3,
    seed: int = 0,
) -> bool:
    if not CAPS.is_docking_available:
        colorprinting.error("Docking is not available, check your preferences.")
        done_emitter(False)
        return False

    proj = ProjectPath(results_folder)
    with open(proj.path("log.html"), "w") as log_file:

        def log(msg: str) -> None:
            log_emitter(msg)
            log_file.write(msg + "\n")
            log_file.flush()

        try:
            log("<h1>Docking procedure</h1>")

            #
            # Check if the output is empty
            #

            if os.listdir(proj.cwd) != ["log.html"]:
                log(
                    f"""                <br/>
                    <font color="red">
                        <b>Warning: the output folder is not empty,
                           the content will be overwritten and merged!</b>
                    </font>
                """
                )

            #
            # Create ligand directory
            #

            try:
                os.mkdir(proj.path("ligands"))
            except FileExistsError:
                shutil.rmtree(proj.path("ligands"))
                os.mkdir(proj.path("ligands"))

            #
            # Collect ligands and convert them into PDBQT
            #
            log("<h2>Ligand preparation</h2>")
            for ligands_path in find_ligands(ligands_folder):
                cmd = (
                    f'"{CAPS.obabel_exe}" "{ligands_path}"'
                    f" -ph {ligand_ph} --gen3d -m"
                    f' -O "{proj.path("ligands", ".pdbqt")}"'
                )
                log(
                    f"""
                    Running: <pre>{cmd}</pre>
                """
                )
                output, success = run(cmd)
                log(f"<pre>{output}</pre>")
                if not success:
                    log(
                        f"""
                        <br/>
                        <b>Ligands conversion to PDBQT failed.</b>
                    """
                    )
                    done_emitter(False)
                    return False

                #
                # Rename PDBQT files
                #
                for pdbqt_path in glob(str(proj.path("ligands", "*.pdbqt"))):
                    with open(pdbqt_path) as pdbqt_file:
                        line = pdbqt_file.readline()
                        assert "Name =" in line
                        mol_name = line.split("=")[1].strip()
                        shutil.move(
                            pdbqt_path, proj.path("ligands", f"{mol_name}.pdbqt")
                        )

            #
            # The number of dockings to do
            #
            n_ligands = len(listdir(proj.path("ligands")))
            if n_ligands == 0:
                log("<br/><b>No ligand converted</b>")
                done_emitter(False)
                return False
            total_emitter(n_ligands)

            #
            # Prepare rigid target
            #
            log("<h2>Target preparation</h2>")
            target_pdb = proj.path("target.pdb")
            pm.save(target_pdb, str(target_sel))

            cmd = f'"{CAPS.adt_python_exe}" "{CAPS.prepare_receptor_path}" -r "{target_pdb}"'
            log(
                f"""
                Running: <pre>{cmd}</pre>
            """
            )
            output, success = run(cmd, cwd=dirname(target_pdb))
            log(f"<pre>{output}</pre>")
            if not success:
                log(
                    f"""
                    <br/>
                    <b>Rigid target preparation failed.</b>
                """
                )
                done_emitter(False)
                return False

            #
            # Prepare flexible target
            #
            if flex_sel != "":
                #
                # Construct residues string
                #
                flex_residues = set()
                for atom in pm.get_model(flex_sel).atom:
                    flex_residues.add(f"{atom.chain}:{atom.resn}{atom.resi}")

                flex_residues = ",".join(f"target:{res}" for res in flex_residues)

                target_pdbqt = proj.path("target.pdbqt")
                cmd = (
                    f'"{CAPS.adt_python_exe}"'
                    f'"{CAPS.prepare_flexreceptor_path}"'
                    f' -r "{target_pdbqt}"'
                    f" -s {flex_residues}"
                )
                log(
                    f"""
                    Running: <pre>{cmd}</pre>
                """
                )
                output, success = run(cmd, cwd=dirname(target_pdb))
                log(f"<pre>{output}</pre>")
                if not success:
                    log(
                        f""">
                        <br/>
                        <br/><b>Flexible target preparation failed.</b>
                    """
                    )
                    done_emitter(False)
                    return False

            #
            # Create Vina results directory
            #

            output_dir = proj.path("poses")
            try:
                os.mkdir(str(output_dir))
            except FileExistsError:
                pass

            #
            # Compute box variables
            #
            box_coords = pm.get_coords(box_sel)

            max = np.max(box_coords, axis=0) + box_margin
            min = np.min(box_coords, axis=0) - box_margin

            half_size = (max - min) / 2
            center = min + half_size

            size_x, size_y, size_z = half_size * 2
            center_x, center_y, center_z = center

            size_x, size_y, size_z = (
                round(float(size_x), 2),
                round(float(size_y), 2),
                round(float(size_z), 2),
            )

            center_x, center_y, center_z = (
                round(float(center_x), 2),
                round(float(center_y), 2),
                round(float(center_z), 2),
            )

            #
            # Project data
            #

            project_data = {
                "program": "vina",
                "size_x": size_x,
                "size_y": size_y,
                "size_z": size_z,
                "center_x": center_x,
                "center_y": center_y,
                "center_z": center_z,
            }

            if flex_sel == "":
                project_data.update(
                    {"flexible": False, "target_pdbqt": str(proj.path("target.pdbqt"))}
                )
            else:
                project_data.update(
                    {
                        "flexible": True,
                        "rigid_pdbqt": str(proj.path("target_rigid.pdbqt")),
                        "flex_pdbqt": str(proj.path("target_flex.pdbqt")),
                    }
                )
            #
            # Prompt for user confirmation
            #
            base_cmd = (
                f'"{CAPS.vina_exe}"'
                f" --center_x {center_x}"
                f" --center_y {center_y}"
                f" --center_z {center_z}"
                f" --size_x {size_x}"
                f" --size_y {size_y}"
                f" --size_z {size_z}"
                f" --seed {seed}"
                f" --exhaustiveness {exhaustiveness}"
                f" --num_modes {num_modes}"
                f" --energy_range {energy_range}"
            )
            if project_data["flexible"]:
                rigid_pdbqt = project_data["rigid_pdbqt"]
                flex_pdbqt = project_data["flex_pdbqt"]
                base_cmd += f' --receptor "{rigid_pdbqt}"' f' --flex "{flex_pdbqt}"'
            else:
                target_pdbqt = project_data["target_pdbqt"]
                base_cmd += f' --receptor "{target_pdbqt}"'
            log(
                f"""
                <h2>Docking</h2>
                <b>Vina base command:</b> {base_cmd}
            """
            )

            script_command = base_cmd.replace(str(results_folder), "./")
            with open(str(proj.path("run_vina_screening.sh")), "w") as script_file:
                script_file.write(
                    f"""#!/bin/bash
                    for ligand_pdbqt in $(find ligands -name '*.pdbqt')
                    do
                        name=$(basename ${{ligand_pdbqt%.pdbqt}})
                        {script_command} \
                            --ligand $ligand_pdbqt \
                            --out poses/$name.out.pdbqt \
                            --log poses/$name.log
                    done
                """
                )

            fail_count = 0
            for i, ligand_pdbqt in enumerate(
                glob(str(proj.path("ligands", "*.pdbqt")))
            ):
                name, _ = splitext(basename(ligand_pdbqt))
                output_pdbqt = proj.path("poses", f"{name}.out.pdbqt")
                log_txt = proj.path("poses", f"{name}.log")

                cmd = base_cmd + (
                    f' --ligand "{ligand_pdbqt}"'
                    f' --out "{output_pdbqt}"'
                    f' --log "{log_txt}"'
                )
                output, success = run(cmd)
                count_emitter(i + 1)
                if not success:
                    fail_count += 1
                    if fail_count <= 10:
                        log(
                            f"""
                            <br/>
                            <font color="red">
                                <b>Vina command failed:</b> {cmd}
                                <br/>
                                <pre>{output}</pre>
                            </font>
                        """
                        )
                    elif fail_count == 11:
                        log(
                            f"""
                            <br/>
                            <h3>
                                <font color="red">
                                    Too many errors. Omitting output.
                                </font>
                            <h3>f
                        """
                        )

            done_ligands = len(glob(str(proj.path(output_dir, "*.out.pdbqt"))))

            log("<br/><h2>Summary</h2>")
            summary = f"""
                <br/><b>Total expected runs:</b> {n_ligands}
                <br/><b>Total failures:</b> {fail_count}
                <br/><b>Total found PDBQT files:</b> {done_ligands}
            """
            if done_ligands < n_ligands or fail_count > 0:
                log(f"<font color='red'>{summary}</font>")
            else:
                log(summary)

            with open(proj.path("docking.json"), "w") as proj_file:
                json.dump(project_data, proj_file, indent=2)
            done_emitter(True)
            return True
        except Exception as exc:
            tb = traceback.format_exception(type(exc), exc, exc.__traceback__)
            log(
                f"""
                <br/>
                <b>Unexpected fail:<b/>
                <br/>
                <pre>{tb}</pre>
            """
            )
            done_emitter(False)
            return False
