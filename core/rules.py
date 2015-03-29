
from inferencerule import InferenceRule

class TypeRule(InferenceRule):
    def getqueries(self):
        partner_enemy = [
            ('?typeId', 'name', 'Kingdom'),
            ('?kingdomId','type','?typeId'),
            ('?kingdomId', 'name', '?kingdomName'),
            ('?phylumId', 'belongs_to', '?kingdomId'),
            ('?classId', 'belongs_to', '?phylumId'),
            ('?orderId', 'belongs_to', '?classId'),
            ('?familyId', 'belongs_to', '?orderId'),
            ('?specieId', 'belongs_to', '?familyId')]
        return [partner_enemy]

    def _maketriples(self, typeId, kingdomId, kingdomName, phylumId, classId, orderId, familyId, specieId):
        if (kingdomName == 'Fungi'):
            kingdomName = 'Fungo'
        elif (kingdomName == 'Animalia'):
            kingdomName = 'Animal'
        elif (kingdomName == 'Chromista'):
            kingdomName = 'Alga'
        else:
            kingdomName = 'Planta'
        return [(specieId, 'is', kingdomName)]

class ParentSpeciesRule(InferenceRule):
    def getqueries(self):
        partner_enemy = [
            ('?typeId', 'name', 'Species'),
            ('?specieId','type','?typeId'),
            ('?specieId', 'belongs_to', '?familyId'),
            ('?specieParentId', 'belongs_to', '?familyId')]
        return [partner_enemy]

    def _maketriples(self, typeId, specieId, familyId, specieParentId):
        if specieId != specieParentId:
            return [(specieId, 'parent_of', specieParentId)]