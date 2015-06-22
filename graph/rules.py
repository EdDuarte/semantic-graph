__author__ = 'Ed Duarte'
__email__ = "edmiguelduarte@gmail.com"
__copyright__ = "Copyright 2015, Ed Duarte"
__credits__ = ["Ed Duarte"]

__license__ = "Apache License 2.0"
__version__ = "2.0.0"
__maintainer__ = "Ed Duarte"
__status__ = "Prototype"

from graph.inferencerule import InferenceRule


class TypeRule(InferenceRule):
    def getqueries(self):
        q = '''
        PREFIX txn: <http://www.semanticweb.prv/taxonomy/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        CONSTRUCT {
            ?specie_id txn:isA ?kingdom_name
        }
        WHERE {
            ?kingdom_id rdf:type <http://www.semanticweb.prv/taxonomy#Kingdom> .
            ?kingdom_id <http://www.semanticweb.prv/taxonomy/name> ?kingdom_name .
            ?phylum_id owl:belongsTo ?kingdom_id .
            ?class_id owl:belongsTo ?phylum_id .
            ?order_id owl:belongsTo ?class_id .
            ?family_id owl:belongsTo ?order_id .
            ?specie_id owl:belongsTo ?family_id .
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


class ParentSpeciesRule(InferenceRule):
    def getqueries(self):
        q = '''
        PREFIX txn: <http://www.semanticweb.prv/taxonomy/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        CONSTRUCT {
            ?specie_id txn:isParent ?specie_parent_id
        }
        WHERE {
            ?specie_id rdf:type <http://www.semanticweb.prv/taxonomy#Species> .
            ?specie_id owl:belongsTo ?family_id .
            ?specie_parent_id owl:belongsTo ?family_id .
            FILTER (?specie_parent_id != ?specie_id)
        }
        '''
        # [
        #     ('?type_id', 'name', 'Species'),
        #     ('?specie_id','type','?type_id'),
        #     ('?specie_id', 'belongs_to', '?family_id'),
        #     ('?specie_parent_id', 'belongs_to', '?family_id')
        # ]
        return q
