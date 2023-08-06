import os.path
import subprocess
import sys
from enum import Enum
from pathlib import Path

from pymol import colorprinting
from pymol.plugins import pref_get, pref_set
from pymol import cmd as pm

from .commons import rscript

PLUGIN_DATA_DIR = os.path.expanduser("~/.pymol/labimm")
os.makedirs(PLUGIN_DATA_DIR, exist_ok=True)


class Capabilities:
    def _get_path(self, pref_name: str) -> str:
        return pref_get(pref_name, "").strip()

    @property
    def obabel_exe(self) -> str:
        return self._get_path("LABIMM_OBABEL")

    @property
    def adt_python_exe(self) -> str:
        return self._get_path("LABIMM_ADT_PYTHON")

    @property
    def prepare_flexreceptor_path(self) -> str:
        return self._get_path("LABIMM_PREPARE_FLEXRECEPTOR")

    @property
    def prepare_receptor_path(self) -> str:
        return self._get_path("LABIMM_PREPARE_RECEPTOR")

    @property
    def vina_exe(self) -> str:
        return self._get_path("LABIMM_VINA")

    @property
    def rscript_exe(self) -> str:
        return self._get_path("LABIMM_RSCRIPT")

    @property
    def is_docking_available(self) -> bool:
        return all(
            map(
                os.path.exists,
                [
                    self.obabel_exe,
                    self.adt_python_exe,
                    self.prepare_flexreceptor_path,
                    self.prepare_receptor_path,
                    self.vina_exe,
                ],
            )
        )

    @property
    def is_r_available(self) -> bool:
        return os.path.isfile(self.rscript_exe)

    @property
    def is_bio3d_available(self) -> bool:
        if self.is_r_available:
            out, _ = rscript("library(bio3d)")
            return "there is no packaged called" not in out
        return False

    @property
    def is_docking_enabled(self) -> bool:
        return pref_get("LABIMM_ENABLE_DOCKING", False)

    @property
    def is_fake_ligand_enabled(self) -> bool:
        return pref_get("LABIMM_ENABLE_FAKE_LIGAND", False)


CAPS = Capabilities()


pref_set("LABIMM_OBABEL", pref_get("LABIMM_OBABEL", ""))
pref_set("LABIMM_VINA", pref_get("LABIMM_VINA", ""))
pref_set("LABIMM_ADT_PYTHON", pref_get("LABIMM_ADT_PYTHON", ""))
pref_set("LABIMM_PREPARE_FLEXRECEPTOR", pref_get("LABIMM_PREPARE_FLEXRECEPTOR", ""))
pref_set("LABIMM_PREPARE_RECEPTOR", pref_get("LABIMM_PREPARE_RECEPTOR", ""))
pref_set("LABIMM_ENABLE_DOCKING", pref_get("LABIMM_ENABLE_DOCKING", False))
pref_set("LABIMM_ENABLE_FAKE_LIGAND", pref_get("LABIMM_ENABLE_FAKE_LIGAND", False))


def install_bio3d():
    assert CAPS.is_r_available

    colorprinting.parrot("Installing Bio3D, please wait.")
    out, success = rscript("install.packages('bio3d')")
    if success:
        print(out)
        colorprinting.parrot("Bio3D was successfully installed.")
    else:
        print(out)
        colorprinting.error("Error: Bio3D was not installed.")


class Channels(Enum):
    STABLE = 'https://pypi.org/simple'
    BETA = 'https://test.pypi.org/simple'


@pm.extend
def upgrade_plugin(channel = 'stable'):
    colorprinting.parrot("Upgrading the plugin, please wait.")
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "pip",
            "--disable-pip-version-check",
            "install",
            "--index-url",
            Channels.BETA.value if channel == 'beta' else Channels.STABLE.value,
            "pymol_labimm",
        ],
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = process.communicate()
    if out:
        print(out)
    if err:
        colorprinting.error(err)
    if CAPS.is_r_available:
        install_bio3d()
