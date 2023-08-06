from glob import glob
from os.path import dirname
from pathlib import Path
from tempfile import mkdtemp

import pytest
from pymol import cmd as pm

from pymol_labimm.docking.vina import (ProjectPath, find_ligands,
                                       run_vina_protocol)


def test_find_ligands():
    tmp_dir = Path(mkdtemp())
    open(tmp_dir / "file.smi", "w").close()
    open(tmp_dir / "file.sdf", "w").close()
    assert set(find_ligands(tmp_dir)) == set(
        [Path(tmp_dir / "file.smi"), Path(tmp_dir / "file.sdf")]
    )
    open(tmp_dir / "file.sdf", "w").close()
    assert set(find_ligands(tmp_dir)) == set(
        [Path(tmp_dir / "file.smi"), Path(tmp_dir / "file.sdf")]
    )


def test_project():
    dock = ProjectPath(".")
    assert dock.cwd == Path("")
    assert dock.path("ligands", "1.pdbqt") == Path("", "ligands", "1.pdbqt")


@pytest.mark.skip
def test_run_vina_protocol():
    results_folder = mkdtemp(prefix="test_vina.")
    ligands_folder = Path(dirname(__file__))

    pm.fetch("4OUA")
    assert run_vina_protocol(
        results_folder,
        ligands_folder,
        "polymer or resn CU1",
        "resn CU1 and chain A",
        exhaustiveness=1,
    )
    with open(results_folder + "/log.html") as log_file:
        assert (
            log_file.read(99999999).replace(results_folder, "./")
            == '<h1>Docking procedure</h1>\n                <br/>\n                    <font color="red">\n                        <b>Warning: the output folder is not empty,\n                           the content will be overwritten and merged!</b>\n                    </font>\n                \n<h2>Ligand preparation</h2>\n\n                    Running: <pre>"/usr/bin/obabel" "/home/peu/Projects/pymol-labimm/tests/smiles.smi" -ph 7 --gen3d -m -O ".//ligands/.pdbqt"</pre>\n                \n<pre>1 molecule converted\n</pre>\n<h2>Target preparation</h2>\n\n                Running: <pre>"/home/peu/Apps/mgltools_x86_64Linux2_1.5.6/bin/python" "/home/peu/Apps/mgltools_x86_64Linux2_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py" -r ".//target.pdb"</pre>\n            \n<pre>Sorry, there are no Gasteiger parameters available for atom target:A:CU1401:CU\nSorry, there are no Gasteiger parameters available for atom target:A:CU1402:CU@A\nSorry, there are no Gasteiger parameters available for atom target:A:CU1402:CU@B\nSorry, there are no Gasteiger parameters available for atom target:B:CU1601:CU\nSorry, there are no Gasteiger parameters available for atom target:B:CU1602:CU\n</pre>\n\n                <h2>Docking</h2>\n                <b>Vina base command:</b> "/usr/bin/vina" --center_x 28.9 --center_y 51.34 --center_z 42.92 --size_x 14.3 --size_y 11.32 --size_z 14.37 --seed 0 --exhaustiveness 1 --num_modes 9 --energy_range 3 --receptor ".//target.pdbqt"\n            \n<br/><h2>Summary</h2>\n\n                <br/><b>Total expected runs:</b> 1\n                <br/><b>Total failures:</b> 0\n                <br/><b>Total found PDBQT files:</b> 1\n            \n'
        )

    assert set(
        map(
            lambda p: p.replace(results_folder, "./"),
            glob(results_folder + "/**", recursive=True),
        )
    ) == set(
        [
            ".//",
            ".//target.pdb",
            ".//ligands",
            ".//ligands/FAD.pdbqt",
            ".//poses",
            ".//poses/FAD.log",
            ".//poses/FAD.out.pdbqt",
            ".//log.html",
            ".//target.pdbqt",
            ".//run_vina_screening.sh",
            ".//docking.json",
        ]
    )
