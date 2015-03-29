
from inferencerule import InferenceRule

class ParentsRule(InferenceRule):
    def getqueries(self):
        partner_enemy = [('?especie', 'is_type', 'Species')]
        return [partner_enemy]

    def _maketriples(self, family, order, className, especie):
        return [(especie, 'belongs_to_class', className)]

class OrderInSpecieRule(InferenceRule):
    def getqueries(self):
        partner_enemy = [('?especie', 'is_type', 'Species'),
                         ('?especie', 'belongs_to', '?family'),
                         ('?family', 'is_type', 'Family'),
                         ('?family', 'belongs_to', '?order'),
                         ('?order', 'is_type', 'Order')]
        return [partner_enemy]

    def _maketriples(self, family, order, especie):
        return [(especie, 'belongs_to_order', order)]

class ClassInFamilyRule(InferenceRule):
    def getqueries(self):
        partner_enemy = [('?family', 'is_type', 'Family'),
                         ('?family', 'belongs_to', '?order'),
                         ('?order', 'is_type', 'Order'),
                         ('?order', 'belongs_to', '?className'),
                         ('?className', 'is_type', 'Class')]
        return [partner_enemy]

    def _maketriples(self, family, order, className):
        return [(family, 'belongs_to_class', className)]