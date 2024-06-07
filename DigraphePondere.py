from DigrapheNonPondere import DigrapheNonPondere
import math


def _min_index(queue, distances):
    """
    Fonction auxiliaire utilisée dans Dijkstra.
    :param queue: Liste des sommets non-résolus
    :param distances: Liste des distances en fonction des sommets
    :return: L'élément de queue ayant une distance minimale.
    """
    assert len(queue) <= len(distances)
    min_index = 0
    min_distance = distances[queue[0]]
    for i in range(1, len(queue)):
        if distances[queue[i]] < min_distance:
            min_distance = distances[queue[i]]
            min_index = i
    return min_index


class DigraphePondere(DigrapheNonPondere):
    """
    Classe représentant des graphes dirigés et pondérés.
    """
    def __init__(self, vertices=None, aretes_generalisees=None):
        """
        Construit un graphe ayant un nombre défini de sommets et des arêtes pondérées.
        :param vertices: Nombre de sommets demandés.
        :param aretes_generalisees: Liste des arêtes pondérées.  Chaque arête est un triplet (source: int, arrivée: int, pondération: float)
        représentant un arc entre le sommet source et le sommet arrivée, de poids pondération.  Les paramètres source et arrivée
        doivent donc être des numéros de sommet valide!
        """
        if aretes_generalisees is not None:
            self.ponderations = {(s, d): p for (s, d, p) in aretes_generalisees}
            super().__init__(vertices, self.ponderations.keys())
        else:
            self.ponderations = None
            super().__init__(vertices, None)

    def _invariant(self):
        """
        Validité de l'instance.  Chaque entrée des pondérations doit être un arc qui existe dans le graphe. Et chaque
        arc doit avoir une pondération.
        :return: True si l'instance est valide
        """
        for s in range(self.num_vertices):
            for d in self.lists[s]:
                if (s, d) not in self.ponderations.keys():
                    return False
        for k in self.ponderations.keys():
            if not self.arete_existe(k[0], k[1]):
                return False
        return super()._invariant()

    def __str__(self):
        """
        Représentation textuelle.
        :return: Un objet string contenant chaque sommet suivi de sa liste d'adjacence avec les pondérations entre
        parenthèses.
        """
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
        """
        Ajoute une arête au graphe.
        :param source: Sommet de départ
        :param dest: Sommet d'arrivée
        :param pond: Pondération de l'arête
        :return: None
        """
        super().ajouter_arete(source, dest)
        self.ponderations[(source, dest)] = pond
        assert self._invariant()

    def lire_ponderation(self, source, dest):
        """
        Retourne la pondération de l'arce entre source et dest.
        :param source: Sommet source
        :param dest: Sommet arrivée
        :return: Pondération de l'arc
        """
        assert self.arete_existe(source, dest)
        return self.ponderations[(source, dest)]

    def _relaxer(self, voisin, courant, distances, predecesseurs):
        """
        Relaxe le voisin à l'aide d'un sommet courant.
        :param voisin: Sommet à relaxer
        :param courant: Sommet prédécesseur servant à la relaxation
        :param distances: Liste des distances
        :param predecesseurs: Liste des prédécesseurs
        :return: (bool, distances, prédécesseurs) un triplet contenant un bool indiquant True si le voisin a effectivement
        changé de prédécesseurs, la liste des distances mise à jour, la liste des prédécesseurs mise à jour.
        """
        temp = distances[courant] + self.lire_ponderation(courant, voisin)
        if temp < distances[voisin]:
            distances[voisin] = temp
            predecesseurs[voisin] = courant
            return False, distances, predecesseurs
        return True, distances, predecesseurs

    def dijkstra(self, depart):
        """
        Algorithme de Dijkstra à partir de départ.  NB: Le comportement de l'algorithme est NON-DÉFINI si une pondération
        négative est présente.
        :param depart: Numéro du sommet de départ
        :return: (pred, dist) = (la liste de prédécesseurs, la liste des distances minimales).  Un sommet inaccessible
        à partir de départ aura None comme prédécesseurs et math.inf comme distance.
        """
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
        """
        Algorithme de Bellman-Ford à partir d'un sommet donné.
        :param depart: Numéro du sommet de départ
        :return: (pred, dist) la liste des prédécesseurs et la liste des distances minimales.
        :raises: ValueError si un cycle de poids négatif est présent.
        """
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
