import unittest
from DigraphePondere import DigraphePondere


class DigraphePondereConstructionTest(unittest.TestCase):
    def test_construction_deux_sommets(self):
        self.g = DigraphePondere(2, [(0, 1, 23.4)])
        self.assertEqual("0 --> 1(23.4)\n1 -->", self.g.__str__())
        self.assertEqual(23.4, self.g.lire_ponderation(0, 1))


class DigraphePondereDijkstraTest(unittest.TestCase):
    def setUp(self) -> None:
        self.g = DigraphePondere(4, [(0, 1, 2.0), (1, 2, 1.0), (2, 3, 3.0), (0, 3, 7.0), (0, 2, 1.0)])
        self.g_neg = DigraphePondere(4, [(0, 1, 2.0), (1, 2, 1.0), (2, 3, 3.0), (0, 3, 7.0), (2, 0, -1.0)])
        self.g_neg_cycle = DigraphePondere(4, [(0, 1, 2.0), (1, 2, 1.0), (2, 3, 3.0), (0, 3, 7.0), (2, 0, -18.0)])

    def test_dijkstra_4(self):
        pred, dist = self.g.dijkstra(0)
        self.assertEqual([None, 0, 0, 2], pred)
        self.assertEqual([0.0, 2.0, 1.0, 4.0], dist)

    def test_bellman_ford(self):
        pred, dist = self.g.bellman_ford(0)
        self.assertEqual([None, 0, 0, 2], pred)
        self.assertEqual([0.0, 2.0, 1.0, 4.0], dist)

    def test_bellman_ford_4_neg(self):
        pred, dist = self.g_neg.bellman_ford(0)
        self.assertEqual([None, 0, 1, 2], pred)
        self.assertEqual([0.0, 2.0, 3.0, 6.0], dist)

    def test_bellmann_ford_4_neg_cycle(self):
        with self.assertRaises(ValueError):
            self.g_neg_cycle.bellman_ford(0)
