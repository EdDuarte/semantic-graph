
from inferencerule import InferenceRule

class ParentRule(InferenceRule):
    def getqueries(self):
        partner_enemy = [('?especie', 'is_type', 'Species'),
                          ('?especie', 'belongs_to', '?family'),
                          ('?family', 'is_type', 'Family'),
                          ('?family', 'belongs_to', '?order'),
                          ('?order', 'is_type', 'Order'),
                          ('?order', 'belongs_to', '?className'),
                          ('?className', 'is_type', 'Class')]
        return [partner_enemy]

    def _maketriples(self, family, order, className, especie):
        return [(especie, 'belongs_to_class', className)]