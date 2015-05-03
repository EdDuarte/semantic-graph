#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'edduarte'

import os.path
import sys
import time
import rdflib
from rdflib import plugin, store
from rdflib import ConjunctiveGraph

class Graph():

    # Create Graph
    def __init__(self):
        self.graph = ConjunctiveGraph('SQLite')
        try:
            self.graph.open('./taxonomy.db', create=True)
        except:
            self.graph.open('./taxonomy.db', create=False)

    # Adds a new triple as (sub, pre, obj)
    def add(self, sub, pre, obj):
        start = time.clock()
        t = self.parse_triple(sub, pre, obj)
        self.graph.add(t)
        elapsed = (time.clock() - start)
        print("Elapsed addition time: %ss" % elapsed)

    # Removes a triple that matches (sub, pre, obj)
    def remove(self, sub, pre, obj):
        start = time.clock()
        t = self.parse_triple(sub, pre, obj)
        self.graph.remove(t)
        elapsed = (time.clock() - start)
        print("Elapsed removal time: %ss" % elapsed)

    # Searches for triples that match (sub, pre, obj)
    def triples(self, sub, pre, obj):
        t = self.parse_triple(sub, pre, obj)
        return self.graph.triples(t)

    @staticmethod
    def parse_triple(sub, pre, obj):
        if sub is not None:
            if sub.startswith('http://taxonomy/'):
                s = rdflib.URIRef(sub)
            else:
                s = rdflib.Literal(sub)
        else:
            s = None
        if pre is not None:
            if pre.startswith('http://taxonomy/'):
                p = rdflib.URIRef(pre)
            else:
                p = rdflib.Literal(pre)
        else:
            p = None
        if obj is not None:
            if obj.startswith('http://taxonomy/'):
                o = rdflib.URIRef(obj)
            else:
                o = rdflib.Literal(obj)
        else:
            o = None
        return s, p, o

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
    def load(self, filename, file_format):
        start = time.clock()
        if filename != '':
            self.graph.parse(filename, format=file_format)
        elapsed = (time.clock() - start)
        print("Elapsed file read time: %ss" % elapsed)

    # Save graph to file
    def save(self, filename, file_format):
        start = time.clock()
        if filename != '':
            of = open(filename, "wb")
            of.write(self.graph.serialize(format=file_format))
            of.close()
        elapsed = (time.clock() - start)
        print("Elapsed file write time: %ss" % elapsed)

    # Return all unique predicates
    def predicates(self):
        return list(set(self.graph.predicates()))

    # Query the database (using SPARQL) with a rule and create new triples
    def apply_inference(self,rule):
        query_text = rule.getqueries()
        query_result = self.graph.query(query_text)
        for r in query_result:
            new_triples = rule.maketriples(r)
            if new_triples is not None:
                for t in new_triples:
                    self.graph.add(t)
