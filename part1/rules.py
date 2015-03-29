
from inferencerule import InferenceRule

class ParentsRule(InferenceRule):
    def getqueries(self):
        partner_enemy = [('?especie', 'is_type', 'Species')]
        return [partner_enemy]

    def _maketriples(self, family, order, className, especie):
        return [(especie, 'belongs_to_class', className)]