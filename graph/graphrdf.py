#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'edduarte'

import os.path
import sys
import time
import rdflib
from rdflib import plugin, store
from rdflib import ConjunctiveGraph
# from inferencerule import *


class GraphRdf():

    typeFileRead = 'n3'

    # Create Graph
    def __init__(self):
        self.graph = ConjunctiveGraph('SQLite')
        try:
            self.graph.open('./taxonomy.db', create=True)
        except:
            self.graph.open('./taxonomy.db', create=False)

    def add(self, sub, pre, obj):
        """
        Add Method
        """
        try:
            start = time.clock()
            sub = 'http://taxonomy/' + sub
            pre = 'http://taxonomy/' + pre
            obj = 'http://taxonomy/' + obj
            self.graph.add((sub, pre, obj))
            elapsed = (time.clock() - start)
            print("Elapsed addition time: %ss" % elapsed)
            # self.applyInferences()
        except KeyError:
            pass

    def remove(self, sub, pre, obj):
        """
        Remove Method
        """
        try:
            start = time.clock()
            self.graph.remove((sub, pre, obj))
            elapsed = (time.clock() - start)
            print("Elapsed removal time: %ss" % elapsed)
            # self.applyInferences()
        except KeyError:
            pass

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

    def triples(self, sub, pre, obj):
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
        return self.graph.triples((s, p, o))


    # Load graph from file
    def load(self, filename, file_format):
        start = time.clock()
        if filename != '':
            if file_format == "sqlite3":
                bd = plugin.get('SQLite', store.Store)(filename)
                try:
                    bd.open(filename, create=True)
                except:
                    bd.open(filename, create=False)
                g = ConjunctiveGraph(bd)
                self.graph += g

            else:
                self.graph.parse(filename, format=file_format)
                # self.applyInferences()

        elapsed = (time.clock() - start)
        print("Elapsed file read time: %ss" % elapsed)

    def predicates(self):
        return list(set(self.graph.predicates()))

    def save(self, filename, file_format):
        start = time.clock()
        print(filename)
        if filename != '':
            if file_format == "sqlite3":
                g = ConjunctiveGraph('SQLite')
                try:
                    g.open(filename, create=True)
                except:
                    g.open(filename, create=False)
                for t in self.triples(None, None, None):
                    g.add(t)
                g.commit()
            else:
                of = open(filename, "wb")
                of.write(self.graph.serialize(format=file_format))
                of.close()
        elapsed = (time.clock() - start)
        print("Elapsed file write time: %ss" % elapsed)


    def query(self, q, pre):
        """
        Query Method
        """
        print("QUERY")
        print("q:" + q)
        print("pre:" + pre)
        try:
            start = time.clock()
            query = '''
                PREFIX tax: <http://taxonomy/>
                SELECT ?name
                WHERE{
                ?id1 tax:name \'''' + q + '''\' .
                ?id1 tax:''' + pre + ''' ?id2 .
                ?id2 tax:name ?name .
                }'''

            result = self.graph.query(query)

            # self.resultQuery.config(state=NORMAL)
            # self.resultQuery.delete(1.0, END)
            # elapsed = (time.clock() - start)
            # print "Time QUERY: %ss" % elapsed
            # if len(result) == 0:
            #     self.resultQuery.insert(INSERT, "Não existe correspondência.")
            #     self.resultQuery.insert(INSERT, "\n")
            # else:
            #     title = q + " " + pre + ":"
            #     self.resultQuery.insert(INSERT, title)
            #     self.resultQuery.insert(INSERT, "\n")
            #     for [n] in result:
            #         self.resultQuery.insert(INSERT, n)
            #         self.resultQuery.insert(INSERT, "\n")
            # self.resultQuery.config(state=DISABLED)
            # self.cleanFieldsQuery()
        except KeyError:
            pass

    def apply_inference(self,rule):
        query_text = rule.getqueries()
        print(query_text)
        query_result = self.graph.query(query_text)

        for r in query_result:
            new_triples = rule.maketriples(r)
            for t in new_triples:
                self.graph.add(t)
