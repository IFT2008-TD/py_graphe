import sys
from typing import List


class DigrapheNonPondere:
    """
    Modélise un digraphe non-pondéré, soit un ensemble de sommets, représentés par des numéros consécutifs, reliés
    entre eux par des arêtes.
    """

    @staticmethod
    def all_elements_unique_in(x):
        return len(set(x)) == len(x)

    def __init__(self, vertices=None, edges=None):
        """
        Construit un digraphe non-pondéré avec le nombre de sommets désirés et une liste de tuples représentant des
        arêtes selon le schéma (source, destination).
        :param vertices: Nombre de sommets demandés, peut être nul.  Les sommets seront numérotés consécutivement de
        0 à vertices-1.
        :param edges: Listes des tuples (source, destination) signalant une arête.  Chaque arête doit être unique et
        constituée de numéros d'arête valides (< vertices)
        """
        if vertices is None:
            self.num_vertices = 0
        else:
            self.num_vertices = vertices
        self.lists: List[List[int]] = [[] for _ in range(self.num_vertices)]
        if edges is not None:
            for edge in edges:
                self.lists[edge[0]].append(edge[1])

        assert(self._invariant())

    def __str__(self):
        resultat = ""
        for i in range(self.num_vertices):
            resultat += f"{i} -->"
            for j in range(len(self.lists[i])):
                resultat += f" {self.lists[i][j]}"
                if j < len(self.lists[i]) - 1:
                    resultat += " - "
            if i < self.num_vertices - 1:
                resultat += "\n"
        return resultat

    def _numero_de_sommet_est_valide(self, n):
        """Retourne True si le paramètre n est un numéro de sommet valide."""
        return n < self.num_vertices

    def _invariant(self):
        """
        Vérifie les conditions de validité du digraphe: pour chaque liste d'adjacence, chaque élément est un numéro de
        sommet valide, et est unique.
        :return: True si le digraphe est valide.
        """
        if self.num_vertices != len(self.lists):
            return False
        for liste in self.lists:
            x = set()
            for sommet in liste:
                if self._numero_de_sommet_est_valide(sommet) and sommet not in x:
                    x.add(sommet)
                else:
                    return False
        return True

    def _liste_adjacence_pour_le_sommet(self, sommet):
        assert(self._numero_de_sommet_est_valide(sommet))
        return self.lists[sommet]

    def ajouter_sommet(self):
        """
        Ajouter un sommet au graphe.
        :return:  None
        """
        self.lists.append([])
        self.num_vertices += 1
        assert(self._invariant())

    def sommet_existe(self, n):
        """
        Vérifie si un numéro de sommet correspond à un sommet existant
        :param n: Numéro à vérifier
        :return:  True si le numéro de sommet existe, dans notre cas: est valide
        """
        return self._numero_de_sommet_est_valide(n)

    def arete_existe(self, source, dest):
        """
        Vérifie si le digraphe contient une arête allant de source à dest
        :param source : Sommet départ de l'arête
        :param dest : Sommet d'arrivée
        :return: True si une arête existe entre source et dest
        """
        assert(self._numero_de_sommet_est_valide(source) and self._numero_de_sommet_est_valide(dest))
        return dest in self.lists[source]

    def ajouter_arete(self, source, dest, *args):
        """
        Rajoute une arête entre source et dest
        :param source: Numéro du sommet source
        :param dest: Numéro du sommet destination
        :return: None
        """
        assert(not self.arete_existe(source, dest))
        self.lists[source].append(dest)
        assert(self._invariant())

    def retirer_arete(self, source, dest):
        """
        Retire l'arête entre source et dest
        :param source: Numéro du sommet source
        :param dest: Numéro du sommet destination
        :return: None
        """
        assert(self.arete_existe(source, dest))
        self.lists[source].remove(dest)
        assert(self._invariant())

    def retirer_sommet(self, sommet):
        """
        Enlève un sommet du digraphe
        :param sommet: Numéro du sommet à retirer
        :return: None
        """
        assert(self._numero_de_sommet_est_valide(sommet))
        for liste in self.lists:
            if sommet in liste:
                liste.remove(sommet)
            for dest in liste:
                if dest > sommet:
                    dest -= 1
        self.lists.pop(sommet)
        self.num_vertices -= 1
        assert(self._invariant())

    def arite_entree_du_sommet(self, sommet):
        """Retourne l'arité d'entrée du sommet demandé"""
        assert(self._numero_de_sommet_est_valide(sommet))
        arite = 0
        for liste in self.lists:
            if sommet in liste:
                arite += 1
        return arite

    def arite_sortie_du_sommet(self, sommet):
        """Retourne l'arité de sortie du sommet demandé"""
        assert(self._numero_de_sommet_est_valide(sommet))
        return len(self.lists[sommet])

    def _aux_explorer_en_profondeur_le_sommet(self, sommet, visites, abandons):
        """
        Exploration en profondeur du digraphe à partir d'un sommet de départ. Méthode récursive.
        :param sommet: Numéro du sommet de départ
        :param visites: Liste de booléens marquant les noeuds visités, devrait être initialement une liste de False
        :param abandons: Liste des noeuds abandonnés, devrait être initialement []
        :return: None
        """
        assert(self._numero_de_sommet_est_valide(sommet))
        visites[sommet] = True
        for voisin in self.lists[sommet]:
            if not visites[voisin]:
                self._aux_explorer_en_profondeur_le_sommet(voisin, visites, abandons)
        assert(sommet not in abandons)
        abandons.append(sommet)

    def explorer_en_profondeur_le_graphe(self):
        """
        Exploration en profondeur de tout le graphe.
        :return: La liste des noeuds abandonnés dans l'ordre de leur abandon.  On peut donc récupérer les noeuds en ordre
        topologique en appelant pop() sur cette liste.
        """
        visites = [False for _ in range(self.num_vertices)]
        abandons = []
        for sommet in range(self.num_vertices):
            if not visites[sommet]:
                self._aux_explorer_en_profondeur_le_sommet(sommet, visites, abandons)
        assert(len(abandons) == self.num_vertices)
        return abandons

    def explorer_le_graphe_en_profondeur_en_partant_du_sommet(self, sommet, visites):
        """
        Exploration en profondeur du graphe, en exigeant un sommet de départ pour débuter l'algorithme.
        :param sommet: Sommet de départ
        :param visites: Liste de bool contenant les sommets déjà visités, lors d'appels précédents par exemple.
        :return: La liste des sommets visités en ordre d'abandon.
        """
        assert(self._numero_de_sommet_est_valide(sommet))
        abandons = []
        self._aux_explorer_en_profondeur_le_sommet(sommet, visites, abandons)
        assert(len(abandons) <= self.num_vertices)
        return abandons

    def _aux_tri_topologique_dfs(self, sommet, abandonnes, en_cours, abandons):
        """
        Fonction auxiliaire récursive pour le tri topologique utilisant dfs.
        :param sommet: Sommet de départ
        :param abandonnes: Liste de bool indiquant quels sommets ont été abandonnés
        :param en_cours: Liste des noeuds visités mais non encore abandonnés
        :param abandons: Liste des noeuds abandonnés en ordre d'abandon
        :return: None
        """
        assert(self._numero_de_sommet_est_valide(sommet))
        en_cours[sommet] = True
        for voisin in self.lists[sommet]:
            if not abandonnes[voisin]:
                if not en_cours[voisin]:
                    self._aux_tri_topologique_dfs(voisin, abandonnes, en_cours, abandons)
                else:
                    raise ValueError(f"Sommet {voisin} déjà en cours de visite.  Cycle détecté, pas de tri topologique possible.")
        assert(sommet not in abandons)
        abandons.append(sommet)
        abandonnes[sommet] = True

    def tri_topologique_dfs(self):
        """
        Tri topologique par exploration en profondeur.
        :return: La liste des sommets visités en ordre d'abandon.
        :raises: ValueError si un cycle est détecté.
        """
        abandonnes = [False for _ in range(self.num_vertices)]
        abandons = []
        for sommet in range(self.num_vertices):
            if not abandonnes[sommet]:
                en_cours = [False for _ in range(self.num_vertices)]
                self._aux_tri_topologique_dfs(sommet, abandonnes, en_cours, abandons)
        assert(len(abandons) == self.num_vertices)
        return abandons

    def graphe_inverse(self):
        """
        Retourne un graphe inverse, donc contenant les mêmes sommets, mais toutes les arêtes sont inversées.
        :return: Le graphe inverse
        """
        inv = DigrapheNonPondere(self.num_vertices,
                                  [(dest, depart) for depart in range(self.num_vertices) for dest in self.lists[depart]])
        return inv

    def kosaraju(self):
        """
        Trouve les composantes fortement connexes du graphe courant.
        :return: La liste des composantes fortement connexes.  Chaque composante est elle-même une liste de sommets.
        """
        cfc = []
        ordre = self.graphe_inverse().explorer_en_profondeur_le_graphe()
        visites = [False for _ in range(self.num_vertices)]
        while ordre:
            courant = ordre.pop()
            if not visites[courant]:
                cfc.append(self.explorer_le_graphe_en_profondeur_en_partant_du_sommet(courant, visites))
        return cfc

    def explorer_en_largeur_en_partant_du_sommet(self, depart=0):
        """
        Exploration en largeur (BFS)
        :param depart: Numéro du sommet de départ
        :return: Liste des prédécesseurs, et longueur du chemin pour chaque sommet.  Si un sommet est inaccessible,
        le prédécesseur sera None, et la distance sera sys.maxsize
        """
        predecesseurs = [None for _ in range(self.num_vertices)]
        distances = [sys.maxsize for _ in range(self.num_vertices)]
        distances[depart] = 0
        visites = [False for _ in range(self.num_vertices)]
        visites[depart] = True
        en_attente = [depart]
        while en_attente:
            courant = en_attente.pop(0)
            distance = distances[courant] + 1
            for voisin in self.lists[courant]:
                if not visites[voisin]:
                    en_attente.append(voisin)
                    visites[voisin] = True
                    predecesseurs[voisin] = courant
                    distances[voisin] = distance
        return predecesseurs, distances









