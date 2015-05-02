#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os.path
import sys

class Graph:
    # indice: [(sub, [(pred, set([obj]))])]
    def __init__(self):
        self._spo = []
        self._pos = []
        self._osp = []

    # adiciona o triplo a todos os indices
    def add(self, sub, pre, obj):
        self._addToIndex(self._spo, sub, pre, obj)
        self._addToIndex(self._pos, pre, obj, sub)
        self._addToIndex(self._osp, obj, sub, pre)

    # adiciona o triplo a um indice caso este ainda nao esteja presente
    def _addToIndex(self, index, a, b, c):
        if not self.exist(index, a):
            index.append((a, [(b, set([c]))]))
            return

        for tuple in index:
            if tuple[0] == a:
                if not self.exist(tuple[1], b):
                    tuple[1].append((b, set([c])))
                    return

        for tuple in index:
            if tuple[0] == a:
                for tuple2 in tuple[1]:
                    if tuple2[0] == b:
                        tuple2[1].add(c)

    def exist(self, index, x):
        result = False
        for tuple in index:
            if tuple[0] == x:
                result = True
        return result

    # remove o triplo de todos os indices
    def remove(self, sub, pre, obj):
        triples = list(self.triples(sub, pre, obj))

        for (delSub, delPre, delObj) in triples:
            self._removeFromIndex(self._spo, delSub, delPre, delObj)
            self._removeFromIndex(self._pos, delPre, delObj, delSub)
            self._removeFromIndex(self._osp, delObj, delSub, delPre)

    # percorre o indice e limpa-o na remocao do indice
    def _removeFromIndex(self, index, a, b, c):
        try:
            for tuple in index:
                if tuple[0] == a:
                    bset = tuple[1]

            for tuple in bset:
                if tuple[0] == b:
                    cset = tuple[1]

            if c in cset:
                cset.remove(c)

            if len(cset) == 0:
                for tuple in index:
                    if tuple[0] == a:
                        for tuple2 in tuple[1]:
                            if tuple2[0] == b:
                                tuple2[1].clear()

            if len(bset) == 0:
                for tuple in index:
                    if tuple[0] == a:
                        del tuple[1]
        except KeyError:
            pass

    def triples_to_dot(self, triples, filename):
        out = open(filename, 'w')
        out.write('graph "Graph" {\n')
        out.write('overlap = "scale";\n')
        for t in triples:
            out.write('"%s" -- "%s" [label="%s"]\n' % (t[0], t[2], t[1]))
        out.write('}\n')
        out.close()

    def create_graph(self, triples):
        graphFileName = 'graph.dot'
        if os.path.isfile(graphFileName):
            os.remove(graphFileName)

        self.triples_to_dot(triples, graphFileName)

        os.system("dot -Tpng graph.dot -o graph.png")

    # pesquisa de um triplo
    def triples(self, sub, pre, obj):
        result = list()
        try:
            if sub != None:
                if pre != None:
                    if obj != None:
                        # temos (sub, pre, obj)
                        for tuple in self._spo:
                            if tuple[0] == sub:
                                for tuple2 in tuple[1]:
                                    if tuple2[0] == pre:
                                        if obj in tuple2[1]:
                                            result.append((sub, pre, obj))
                    else:
                        # temos (sub, pre, None)
                        for tuple in self._spo:
                            if tuple[0] == sub:
                                for tuple2 in tuple[1]:
                                    if tuple2[0] == pre:
                                        for retObj in tuple2[1]:
                                            result.append((sub, pre, retObj))
                else:
                    if obj != None:
                        # temos (sub, Nome, obj)
                        for tuple in self._osp:
                            if tuple[0] == obj:
                                for tuple2 in tuple[1]:
                                    if tuple2[0] == sub:
                                        for retPre in tuple2[1]:
                                            result.append((sub, retPre, obj))
                    else:
                        # temos (sub, None, None)
                        for tuple in self._spo:
                            if tuple[0] == sub:
                                for retPre, tuple2 in tuple[1]:
                                    #for retObj in tuple2[1]:
                                    for retObj in tuple2:
                                        result.append((sub, retPre, retObj))
            else:
                if pre != None:
                    if obj != None:
                        # temos (None, pre, obj)
                        for tuple in self._pos:
                            if tuple[0] == pre:
                                for tuple2 in tuple[1]:
                                    if tuple2[0] == obj:
                                        for retSub in tuple2[1]:
                                            result.append((retSub, pre, obj))
                    else:
                        # temos (None, pre, None)
                        for tuple in self._pos:
                            if tuple[0] == pre:
                                for retObj, tuple2 in tuple[1]:
                                    for retSub in tuple2:
                                        result.append((retSub, pre, retObj))
                else:
                    if obj != None:
                        # temos (None, None, obj)
                        for tuple in self._osp:
                            if tuple[0] == obj:
                                for retSub, tuple2 in tuple[1]:
                                    #for retPre in tuple2[1]:
                                    for retPre in tuple2:
                                        result.append((retSub, retPre, obj))
                    else:
                        # temos (None, None, None)
                        for tuple in self._spo:
                            retSub = tuple[0]
                            for tuple2 in tuple[1]:
                                retPre = tuple2[0]
                                for retObj in tuple2[1]:
                                    result.append((retSub, retPre, retObj))
            return result
        except KeyError:
            pass

    # carrega o conteudo de um ficheiro .csv
    def load(self, filename):
        f = open(filename, "r")
        reader = csv.reader(f)

        for triple in reader:
            if len(triple) == 3:
                self.add(triple[0], triple[1], triple[2])

        f.close()
        print("Loaded!")

    # guarda o conteudo num ficheiro .csv
    def save(self, filename):
        if sys.version_info >= (3,0,0):
            f = open(filename, 'w', newline='')
        else:
            f = open(filename, 'wb')
        writer = csv.writer(f)

        for sub, pred, obj in self.triples(None, None, None):
            writer.writerow([sub, pred, obj])
        f.close()

    # faz um query ao grafo,
    # passando-lhe uma lista de tuples (triplos restrição)
    # devolve uma lista de dicionarios (var:valor)
    def query(self, clauses):
        bindings = None                      # resultado a devolver
        for clause in clauses:               # para cada triplo
            bpos = {}                        # dicionário que associa a variável à sua posição no triplo de pesquisa
            qc = []                          # lista de elementos a passar ao método triples
            for pos, x in enumerate(clause): # enumera o triplo, para poder ir buscar cada elemento e sua posição
                if x.startswith('?'):        # para as variáveis
                    qc.append(None)          # adiciona o valor None à lista de elementos a passar ao método triples
                    #bpos[x] = pos           # guarda a posição da variável no triplo (0,1 ou 2)
                    bpos[x[
                         1:]] = pos          # linha de cima re-escrita porque é necessário guardar o nome da variável, mas sem o ponto de interrogação (?)
                else:
                    qc.append(x)             # adiciona o valor dado à lista de elementos a passar ao método triples

            rows = list(self.triples(qc[0], qc[1], qc[2])) # faz a pesquisa com o triplo acabado de construir

            # primeiro triplo pesquisa, todos os resultados servem
            # para cada triplo resultado, cria um dicionario de variaveis (1 a 3 variaveis)
            # em cada dicionario, as variaveis tomam o valor devolvido pelo elemento na mesma posicao da variavel
            if bindings == None:
                bindings = []                # cria a lista a devolver
                for row in rows:             # para cada triplo resultado
                    binding = {}             # cria um dicionario
                    for var, pos in bpos.items(): # para cada variável e sua posição
                        binding[var] = row[pos] # associa à variável o valor do elemento do triplo na sua posição
                    bindings.append(binding) # adiciona o dicionario à lista

            else:                            # triplos pesquisa seguintes, eliminar resultados que não servem
                # In subsequent passes, eliminate bindings that don't work
                newb = []                    # cria nova lista a devolver
                for binding in bindings:     # para cada dicionario da lista de dicionarios
                    for row in rows:         # para cada triplo resultado
                        validmatch = True    # começa por assumir que o dicionario serve
                        tempbinding = binding.copy() # faz copia temporaria do dicionario
                        for var, pos in bpos.items(): # para cada variavel em sua posição
                            if var in tempbinding: # caso a variavel esteja presente no dicionario
                                if tempbinding[var] != row[pos]: # se o valor da variavel diferente do valor na sua posicao no triplo
                                    validmatch = False # o dicionário não serve
                            else:
                                tempbinding[var] = row[
                                    pos] # associa à variável o valor do elemento do triplo na sua posição
                        if validmatch:
                            newb.append(tempbinding) # se dicionario serve, inclui-o na nova lista
                bindings = newb              # sbstituiu lista por nova
        return bindings

    def apply_inference(self,rule):
        queries = rule.getqueries()
        bindings = []
        for query in queries:
            bindings += self.query(query)
        for b in bindings:
            new_triples = rule.maketriples(b)
            if new_triples is not None:
                for s, p, o in new_triples:
                    self.add(s, p, o)