#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Ed Duarte'
__email__ = "edmiguelduarte@gmail.com"
__copyright__ = "Copyright 2015, Ed Duarte"
__credits__ = ["Ed Duarte"]

__license__ = "Apache License 2.0"
__version__ = "2.0.0"
__maintainer__ = "Ed Duarte"
__status__ = "Prototype"

import os.path
import time
import json
import codecs

import rdflib
from rdflib.parser import StringInputSource
from graph.connection import Connection


class Graph():
    # Create Graph
    def __init__(self):
        self.conn = Connection("http://localhost:8080/openrdf-sesame/")
        self.repository = "taxonomy"

    # Adds a new triple as (sub, pre, obj)
    def add(self, sub, pre, obj):
        start = time.clock()
        t = self.parse_triple_string(sub, pre, obj)
        self.conn.add_data_no_context(self.repository, t)
        elapsed = (time.clock() - start)
        print("Elapsed addition time: %ss" % elapsed)

    # Removes a triple that matches (sub, pre, obj)
    def remove(self, sub, pre, obj):
        start = time.clock()
        t = self.parse_triple(sub, pre, obj)

        # create a new auxiliary graph
        graph = rdflib.ConjunctiveGraph()
        data = StringInputSource(self.conn.statements_default_graph(
            self.repository,
            'text/plain'
        ))
        graph.parse(data, format="nt")

        # remove all triples from the Sesame repository
        self.conn.remove_all_statements(self.repository)

        # remove desired triple from auxiliary graph
        graph.remove(t)

        # send all remaining triples to the Sesame repository
        self.conn.add_data_no_context(self.repository, graph.serialize(format="nt"))

        elapsed = (time.clock() - start)
        print("Elapsed removal time: %ss" % elapsed)

    # Searches for triples that match (sub, pre, obj)
    def triples(self, sub, pre, obj):
        graph = rdflib.ConjunctiveGraph()
        data = StringInputSource(self.conn.statements_default_graph(
            self.repository,
            'text/plain'
        ))
        graph.parse(data, format="nt")
        t = self.parse_triple(sub, pre, obj)
        return graph.triples(t)

    # # Searches for triples that match the provided entity
    def browse(self, entity):

        # parse entity
        if entity is not None:
            if entity.startswith('http://'):
                entity = "<" + entity + ">"
            else:
                entity = "\"" + entity + "\""

        # query and group results for the entity as a subject
        query_text1 = "CONSTRUCT { " + entity + " ?p ?o . } WHERE { " + entity + " ?p ?o . }"
        results1 = self.conn.query_post(self.repository, query_text1)
        results1 = json.loads(results1.decode("utf-8"))
        results1_string = ""
        for t in results1.keys():
            sub = t
            for y in results1[t].keys():
                pre = y
                for z in results1[t][y]:
                    obj = z['value']

                    if pre == "http://www.semanticweb.prv/taxonomy/name":
                        results1_string += "<p>named <b><span property=\"foaf:name\">" + obj + "</span></b></p>"

                    elif pre == "http://www.semanticweb.prv/taxonomy/isA":
                        results1_string += "<p>is a <b><span class=\"specie\">" + obj + "</span></b></p>"

                    elif pre == "http://www.semanticweb.prv/taxonomy/isParent":
                        results1_string += "<p>is parent of <b><span property=\"skos:topConceptOf\">" + obj + "</span></b></p>"

                    elif pre == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                        results1_string += "<p>is of concept <b><span property=\"skos:Concept\">" + obj + "</span></b></p>"

                    elif pre == "http://www.w3.org/2002/07/owl#belongsTo":
                        results1_string += "<p>has broader concept <b><span property=\"skos:broader\">" + obj + "</span></b></p>"

        # query and group results for the entity as an object
        query_text2 = "CONSTRUCT { ?s ?p " + entity + " . } WHERE { ?s ?p " + entity + " . }"
        results2 = self.conn.query_post(self.repository, query_text2)
        results2 = json.loads(results2.decode("utf-8"))
        results2_string = ""
        for t in results2.keys():
            sub = t
            for y in results2[t].keys():
                pre = y
                for z in results2[t][y]:
                    obj = z['value']

                    if pre == "http://www.semanticweb.prv/taxonomy/name":
                        results2_string += "<p>named <b><span property=\"foaf:name\">" + sub + "</span></b></p>"

                    elif pre == "http://www.semanticweb.prv/taxonomy/isA":
                        results2_string += "<p>is a <b><span class=\"specie\">" + sub + "</span></b></p>"

                    elif pre == "http://www.semanticweb.prv/taxonomy/isParent":
                        results2_string += "<p>is parent of <b><span property=\"skos:topConceptOf\">" + sub + "</span></b></p>"

                    elif pre == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                        results2_string += "<p>is of concept <b><span property=\"skos:Concept\">" + sub + "</span></b></p>"

                    elif pre == "http://www.w3.org/2002/07/owl#belongsTo":
                        results2_string += "<p>has broader concept <b><span property=\"skos:broader\">" + sub + "</span></b></p>"

        return results1_string, results2_string

    def has_triples(self):
        return len(list(self.triples(None, None, None))) != 0

    @staticmethod
    def parse_triple(sub, pre, obj):
        if sub is not None:
            if sub.startswith('http://'):
                s = rdflib.URIRef(sub)
            else:
                s = rdflib.Literal(sub)
        else:
            s = None
        if pre is not None:
            if pre.startswith('http://'):
                p = rdflib.URIRef(pre)
            else:
                p = rdflib.Literal(pre)
        else:
            p = None
        if obj is not None:
            if obj.startswith('http://'):
                o = rdflib.URIRef(obj)
            else:
                o = rdflib.Literal(obj)
        else:
            o = None
        return s, p, o

    @staticmethod
    def parse_triple_string(sub, pre, obj):
        if sub is not None:
            if sub.startswith('http://'):
                s = "<" + sub + ">"
            else:
                s = sub
        else:
            s = "?s"
        if pre is not None:
            if pre.startswith('http://'):
                p = "<" + pre + ">"
            else:
                p = pre
        else:
            p = "?p"
        if obj is not None:
            if obj.startswith('http://'):
                o = "<" + obj + ">"
            else:
                o = "\"" + obj + "\""
        else:
            o = "?o"
        return s + " " + p + " " + o + " ."

    # Draws a graph of the specified triples to the file "graph.png"
    def draw_graph(self, triples):
        filename = 'graph.dot'
        if os.path.isfile(filename):
            os.remove(filename)

        # convert graph into a dot file
        out = open(filename, 'w')
        out.write('graph "Graph" {\n')
        out.write('overlap = "scale";\n')
        for t in triples:
            out.write('"%s" -- "%s" [label="%s"]\n' % (t[0], t[2], t[1]))
        out.write('}\n')
        out.close()

        # convert dot file into a png file using dot app
        os.system("dot -Tpng graph.dot -o graph.png")

    # Load graph from file
    def load(self, file_content, file_format):
        start = time.clock()
        if file_format == "xml":
            error_msg = self.conn.replace_data(self.repository, file_content)
        else:
            error_msg = self.conn.add_data_no_context(self.repository, file_content)
        elapsed = (time.clock() - start)
        print("Elapsed file read time: %ss" % elapsed)
        if error_msg is not None:
            raise Exception(error_msg)

    # Save graph to file
    def save(self, filename, file_format):
        start = time.clock()
        if filename != '':
            of = open(filename, "wb")
            graph = rdflib.ConjunctiveGraph()
            data = StringInputSource(self.conn.statements_default_graph(
                self.repository,
                'text/plain'
            ))
            graph.parse(data, format="nt")
            of.write(graph.serialize(format=file_format))
            of.close()
        elapsed = (time.clock() - start)
        print("Elapsed file write time: %ss" % elapsed)

    # Return all unique predicates
    def predicates(self):
        predicates = set()
        for t in self.triples(None, None, None):
            predicates.add(t[1])
        return list(predicates)

    # Query the database (using SPARQL) with a rule and create new triples
    def apply_inference(self, rule):
        query_text = rule.getqueries()
        results = self.conn.query_post(self.repository, query_text)
        results = json.loads(results.decode("utf-8"))

        for t in results.keys():
            sub = t
            for y in results[t].keys():
                pred = y
                for z in results[t][y]:
                    if z["type"] == "literal":
                        obj = "\"" + z['value'] + "\""
                    else:
                        obj = "<" + z['value'] + ">"

                    update = "INSERT {<%s> <%s> %s} " \
                             "WHERE {?s ?p ?o}" % (sub, pred, obj)
                    self.conn.update_described(self.repository, update)