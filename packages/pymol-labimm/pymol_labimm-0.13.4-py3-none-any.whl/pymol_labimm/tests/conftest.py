import pkg_resources
import pymol.cmd as pm
import pymol.plugins
import pytest
from pytest import fixture

from pymol_labimm import commons


@pytest.fixture(scope="session", autouse=True)
def load_pymol_plugin():
    pymol.plugins.plugin_load("pymol_labimm")


@fixture
def atlas_pdb():
    pdb = pkg_resources.resource_filename(
        "pymol_labimm.tests.data", "NS5-full_01_atlas.pdb"
    )
    with commons.disable_feedback("all", "warnings"):
        pm.load(pdb)


@fixture
def ftmap_pdb():
    pdb = pkg_resources.resource_filename("pymol_labimm.tests.data", "fftmap.88200.pdb")
    with commons.disable_feedback("all", "warnings"):
        pm.load(pdb)


@fixture
def reinitialize_pymol(scope="function"):
    pm.reinitialize()
