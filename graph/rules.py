__author__ = 'Ed Duarte'
__email__ = "edmiguelduarte@gmail.com"
__copyright__ = "Copyright 2015, Ed Duarte"
__credits__ = ["Ed Duarte"]

__license__ = "Apache License 2.0"
__version__ = "2.0.0"
__maintainer__ = "Ed Duarte"
__status__ = "Prototype"

from rdflib import Namespace

from graph.inferencerule import InferenceRule


class TypeRule(InferenceRule):
    def getqueries(self):
        q = '''
        PREFIX txn: <http://taxonomy/>
        SELECT ?type_id ?kingdom_id ?kingdom_name ?phylum_id ?class_id ?order_id ?family_id ?specie_id
        WHERE {
            ?type_id txn:name "Kingdom" .
            ?kingdom_id txn:type ?type_id .
            ?kingdom_id txn:name ?kingdom_name .
            ?phylum_id txn:belongs_to ?kingdom_id .
            ?class_id txn:belongs_to ?phylum_id .
            ?order_id txn:belongs_to ?class_id .
            ?family_id txn:belongs_to ?order_id .
            ?specie_id txn:belongs_to ?family_id .
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

    def _maketriples(self, type_id, kingdom_id, kingdom_name, phylum_id,
                     class_id, order_id, family_id, specie_id):
        txn = Namespace('http://taxonomy/')
        return [(specie_id, txn['is_a'], kingdom_name)]


class ParentSpeciesRule(InferenceRule):
    def getqueries(self):
        q = '''
        PREFIX txn: <http://taxonomy/>
        SELECT ?type_id ?specie_id ?family_id ?specie_parent_id
        WHERE {
            ?type_id txn:name "Species" .
            ?specie_id txn:type ?type_id .
            ?specie_id txn:belongs_to ?family_id .
            ?specie_parent_id txn:belongs_to ?family_id
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
            txn = Namespace('http://taxonomy/')
            return [(specie_id, txn['is_parent'], specie_parent_id)]
