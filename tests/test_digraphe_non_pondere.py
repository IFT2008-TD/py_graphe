import unittest
from DigrapheNonPondere import DigrapheNonPondere


class DigrapheNonPondereConstructionTest(unittest.TestCase):
    def test_init_vide(self):
        g = DigrapheNonPondere()
        self.assertEqual("", g.__str__())

    def test_init_un_sommet_zero_arete(self):
        g = DigrapheNonPondere(1)
        self.assertEqual("0 -->", g.__str__())

    def test_init_deux_sommets_une_arete(self):
        g = DigrapheNonPondere(2, [(0, 1)])
        self.assertEqual("0 --> 1\n1 -->", g.__str__())

    def test_init_deux_sommets_deux_aretes(self):
        g = DigrapheNonPondere(2, [(0, 1), (1, 0)])
        self.assertEqual("0 --> 1\n1 --> 0", g.__str__())


class DigrapheNonPondereInterfaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.g21 = DigrapheNonPondere(2, [(0, 1)])
        self.g21str = "0 --> 1\n1 -->"
        self.g22 = DigrapheNonPondere(2, [(0, 1), (1, 0)])
        self.g22str = "0 --> 1\n1 --> 0"
        self.g68a = DigrapheNonPondere(6, [(0, 1), (0, 3), (1, 2), (1, 5), (1, 4), (2, 5), (3, 4), (4, 5)])
        self.g68c = DigrapheNonPondere(6, [(0, 1), (0, 3), (1, 2), (5, 1), (1, 4), (2, 5), (3, 4), (4, 5)])

    def test_ajouter_sommet(self):
        self.g21.ajouter_sommet()
        self.assertEqual(self.g21str + "\n2 -->", self.g21.__str__())

    def test_ajouter_arete(self):
        self.g21.ajouter_arete(1, 0)
        self.assertEqual(self.g22str, self.g21.__str__())

    def test_retirer_arete(self):
        self.g22.retirer_arete(1, 0)
        self.assertEqual(self.g21str, self.g22.__str__())

    def test_retirer_sommet_source(self):
        self.g22.retirer_sommet(1)
        self.assertEqual("0 -->", self.g22.__str__())

    def test_retirer_sommet_puits(self):
        self.g22.retirer_sommet(0)
        self.assertEqual("0 -->", self.g22.__str__())

    def test_arite_entree(self):
        self.assertEqual(1, self.g22.arite_entree_du_sommet(0))
        self.assertEqual(1, self.g22.arite_sortie_du_sommet(0))


class DigrapheNonPondereAlgorithmesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.g21 = DigrapheNonPondere(2, [(0, 1)])
        self.g21str = "0 --> 1\n1 -->"
        self.g22 = DigrapheNonPondere(2, [(0, 1), (1, 0)])
        self.g22str = "0 --> 1\n1 --> 0"
        self.g65 = DigrapheNonPondere(6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
        self.g68a = DigrapheNonPondere(6, [(0, 1), (0, 3), (1, 2), (1, 5), (1, 4), (2, 5), (3, 4), (4, 5)])
        self.g68c = DigrapheNonPondere(6, [(0, 1), (0, 3), (1, 2), (5, 1), (1, 4), (2, 5), (3, 4), (4, 5)])

    def test_explorer_en_profondeur_le_graphe_21(self):
        self.assertEqual([1, 0], self.g21.explorer_en_profondeur_le_graphe())

    def test_explorer_en_profondeur_le_graphe_68a(self):
        self.assertEqual([5, 2, 4, 1, 3, 0], self.g68a.explorer_en_profondeur_le_graphe())

    def test_explorer_en_profondeur_le_graphe_65(self):
        self.assertEqual([5, 4, 3, 2, 1, 0], self.g65.explorer_en_profondeur_le_graphe())

    def test_tri_topologique_defs_graphe_68a(self):
        self.assertEqual([5, 2, 4, 1, 3, 0], self.g68a.tri_topologique_dfs())

    def test_tri_topologique_dfs_graphe_68c(self):
        with self.assertRaises(ValueError):
            self.g68c.tri_topologique_dfs()

    def test_graphe_inverse(self):
        self.assertEqual("0 -->\n1 --> 0", self.g21.graphe_inverse().__str__())

    def test_kosaraju_21(self):
        self.assertEqual([[1], [0]], self.g21.kosaraju())

    def test_kosaraju_68c(self):
        self.assertEqual([[5, 2, 4, 1], [3], [0]], self.g68c.kosaraju())



if __name__ == '__main__':
    unittest.main()
