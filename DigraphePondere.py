from DigrapheNonPondere import DigrapheNonPondere
import math


def _min_index(queue, distances):
    min_index = 0
    min_distance = distances[queue[0]]
    for i in range(1, len(queue)):
        if distances[queue[i]] < min_distance:
            min_distance = distances[queue[i]]
            min_index = i
    return min_index


class DigraphePondere(DigrapheNonPondere):
    def __init__(self, vertices=None, aretes_generalisees=None):
        if aretes_generalisees is not None:
            self.ponderations = {(s, d): p for (s, d, p) in aretes_generalisees}
            super().__init__(vertices, self.ponderations.keys())
        else:
            self.ponderations = None
            super().__init__(vertices, None)

    def _invariant(self):
        for s in range(self.num_vertices):
            for d in self.lists[s]:
                if (s, d) not in self.ponderations.keys():
                    return False
        for k in self.ponderations.keys():
            if not self.arete_existe(k[0], k[1]):
                return False
        return super()._invariant()

    def __str__(self):
        resultat = ""
        for i in range(self.num_vertices):
            resultat += f"{i} -->"
            for j in range(len(self.lists[i])):
                resultat += f" {self.lists[i][j]}"
                try:
                    pond = self.lire_ponderation(i, self.lists[i][j])
                    resultat += f"({pond})"
                finally:
                    if j < len(self.lists[i]) - 1:
                        resultat += " - "
            if i < self.num_vertices - 1:
                resultat += "\n"
        return resultat

    def ajouter_arete(self, source, dest, pond=1.0):
        super().ajouter_arete(source, dest)
        self.ponderations[(source, dest)] = pond
        assert self._invariant()

    def lire_ponderation(self, source, dest):
        assert self.arete_existe(source, dest)
        return self.ponderations[(source, dest)]

    def _relaxer(self, voisin, courant, distances, predecesseurs):
        temp = distances[courant] + self.lire_ponderation(courant, voisin)
        if temp < distances[voisin]:
            distances[voisin] = temp
            predecesseurs[voisin] = courant
            return False, distances, predecesseurs
        return True, distances, predecesseurs

    def dijkstra(self, depart):
        assert self._numero_de_sommet_est_valide(depart)
        predecesseurs = [None for _ in range(self.num_vertices)]
        distances = [math.inf for _ in range(self.num_vertices)]
        distances[depart] = 0
        non_solutionnes = [i for i in range(self.num_vertices)]
        while non_solutionnes:
            courant = non_solutionnes.pop(_min_index(non_solutionnes, distances))
            for voisin in self.lists[courant]:
                _, distances, predecesseurs = self._relaxer(voisin, courant, distances, predecesseurs)
        return predecesseurs, distances

    def bellman_ford(self, depart):
        assert self._numero_de_sommet_est_valide(depart)
        predecesseurs = [None for _ in range(self.num_vertices)]
        distances = [math.inf for _ in range(self.num_vertices)]
        distances[depart] = 0
        k = 0
        stable = False
        while not stable and k < self.num_vertices:
            stable = True
            for (source, dest) in self.ponderations.keys():
                demeure_stable, distances, predecesseurs = self._relaxer(dest, source, distances, predecesseurs)
                stable = stable and demeure_stable
            k += 1
        if not stable:
            raise ValueError("Cycle de poids négatif détecté")
        return predecesseurs, distances
