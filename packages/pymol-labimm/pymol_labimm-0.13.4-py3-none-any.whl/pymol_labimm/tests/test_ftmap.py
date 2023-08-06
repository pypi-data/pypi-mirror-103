from operator import attrgetter

from pytest import approx, mark

from pymol_labimm.ftmap.core import Cluster, Ensemble, Kozakov2015Ensemble


@mark.incremental
class TestCluster:
    def test_collect_atlas(self, reinitialize_pymol, atlas_pdb):
        clusters = list(Cluster.collect_atlas())
        assert len(clusters) == 13
        assert "consensus.001.015" in map(attrgetter("sele"), clusters)

    def test_collect_ftmap(self, reinitialize_pymol, ftmap_pdb):
        clusters = list(Cluster.collect_ftmap())
        assert len(clusters) == 12
        assert "consensus.001.018" in map(attrgetter("sele"), clusters)

    def test_attrs_atlas(self, reinitialize_pymol, atlas_pdb):
        clusters = list(Cluster.collect_atlas())
        assert clusters[2].strength == 13
        assert len(clusters[3].coords) == 52

    @mark.skip
    def test_attrs_ftmap(self, reinitialize_pymol, ftmap_pdb):
        clusters = list(Cluster.collect_ftmap())
        assert clusters[2].strength == 15
        assert len(clusters[3].coords) == 41
        assert clusters[0].max_dist == approx(8.1, abs=0.1)
        assert clusters[0].surf_area == approx(230, abs=0.1)
        assert clusters[0].compactness == approx(0.49, abs=0.01)
        assert clusters[0].polar_count == 10
        assert clusters[0].apolar_count == 10


@mark.incremental
class TestEnsemble:
    def test_collect_atlas(self, reinitialize_pymol, atlas_pdb):
        ensembles = list(Ensemble.collect_atlas(3))
        assert len(ensembles) == 377

    def test_collect_ftmap(self, reinitialize_pymol, ftmap_pdb):
        ensembles = list(Ensemble.collect_ftmap(3))
        assert len(ensembles) == 298

    @mark.skip
    def test_attrs(self, reinitialize_pymol, atlas_pdb):
        ensembles = list(Ensemble.collect_atlas(3))
        assert len(ensembles[2].clusters) == 1
        assert ensembles[2].strength == 13
        assert approx(ensembles[1].max_dist, abs=0.1) == 6.9
        assert approx(ensembles[15].surf_area, abs=0.1) == 413.2
        assert ensembles[0].hydrophilic_count == 10
        assert ensembles[0].hydrophobic_count == 10
        for (cluster_a, cluster_b), dist in ensembles[1].center_to_center.items():
            pass  # print(cluster_a, cluster_b, dist)


@mark.incremetal
class TestKozakov2015Essemble:
    def test_collect(self, reinitialize_pymol, atlas_pdb):
        ensembles = list(Kozakov2015Ensemble.collect_atlas(3))
        assert len(ensembles) == 377
        assert all(isinstance(e, Kozakov2015Ensemble) for e in ensembles)

    @mark.skip
    def test_classes(self, reinitialize_pymol, atlas_pdb):
        ensembles = list(Kozakov2015Ensemble.collect_atlas(3))
        assert ensembles[0].is_druggable and not ensembles[0].is_druggable_large
