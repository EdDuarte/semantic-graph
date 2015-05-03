
from graph.inferencerule import InferenceRule
from rdflib import Namespace

class TypeRule(InferenceRule):
    def getqueries(self):
        q = '''
        PREFIX avr: <http://taxonomy/>
        SELECT ?type_id ?kingdom_id ?kingdom_name ?phylum_id ?class_id ?order_id ?family_id ?specie_id
        WHERE {
            ?type_id avr:name "Kingdom" .
            ?kingdom_id avr:type ?type_id .
            ?kingdom_id avr:name ?kingdom_name .
            ?phylum_id avr:belongs_to ?kingdom_id .
            ?class_id avr:belongs_to ?phylum_id .
            ?order_id avr:belongs_to ?class_id .
            ?family_id avr:belongs_to ?order_id .
            ?specie_id avr:belongs_to ?family_id .
        }
        '''
        # [
        #     ('?type_id', 'name', 'Kingdom'),
        #     ('?kingdom_id','type','?type_id'),
        #     ('?kingdom_id', 'name', '?kingdom_name'),
        #     ('?phylum_id', 'belongs_to', '?kingdom_id'),
        #     ('?class_id', 'belongs_to', '?phylum_id'),
        #     ('?order_id', 'belongs_to', '?class_id'),
        #     ('?family_id', 'belongs_to', '?order_id'),
        #     ('?specie_id', 'belongs_to', '?family_id')
        # ]
        return q

    def _maketriples(self, type_id, kingdom_id, kingdom_name, phylum_id, class_id, order_id, family_id, specie_id):
        avr = Namespace('http://taxonomy/')
        return [(specie_id, avr['is_a'], kingdom_name)]

class ParentSpeciesRule(InferenceRule):
    def getqueries(self):
        q = '''
        PREFIX avr: <http://taxonomy/>
        SELECT ?type_id ?specie_id ?family_id ?specie_parent_id
        WHERE {
            ?type_id avr:name "Species" .
            ?specie_id avr:type ?type_id .
            ?specie_id avr:belongs_to ?family_id .
            ?specie_parent_id avr:belongs_to ?family_id
        }
        '''
        # [
        #     ('?type_id', 'name', 'Species'),
        #     ('?specie_id','type','?type_id'),
        #     ('?specie_id', 'belongs_to', '?family_id'),
        #     ('?specie_parent_id', 'belongs_to', '?family_id')
        # ]
        return q

    def _maketriples(self, type_id, specie_id, family_id, specie_parent_id):
        if specie_id != specie_parent_id:
            avr = Namespace('http://taxonomy/')
            return [(specie_id, avr['is_parent'], specie_parent_id)]
