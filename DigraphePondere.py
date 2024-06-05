from DigrapheNonPondere import DigrapheNonPondere


class DigraphePondere(DigrapheNonPondere):
    def __init__(self, vertices=None, aretes_generalisees=None):
        if aretes_generalisees is not None:
            self.ponderations = {(s, d): p for (s, d, p) in aretes_generalisees}
            super().__init__(vertices, self.ponderations.keys())
        else:
            self.ponderations = None
            super().__init__(vertices, None)

    def _invariant(self):
        for s in self.num_vertices:
            for d in self.lists[s]:
                if (s, d) not in self.ponderations.keys():
                    return False
        for k in self.ponderations.keys():
            if not self.arete_existe(k[0], k[1]):
                return False
        return super()._invariant()

    def ajouter_arete(self, source, dest, pond=1.0):
        super().ajouter_arete(source, dest)
        self.ponderations[(source, dest)] = pond
        assert self._invariant()
