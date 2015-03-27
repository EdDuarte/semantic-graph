#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from PIL import Image
import pydot


class grafo:
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

    def triplestodotOp(self):
        print ("triplestodot")
        out = file("graph.dot", 'wb')
        out.write('digraph "Trabalho Prático - Web Semântica" {\n')
        out.write('\tlabelloc="t"\n'
                  '\tlabel="Trabalho Prático - Web Semântica"\n')
        for sub, pre, obj in self.triples((None, None, None)):
            if pre == "name":
                out.write('\t%s [shape=circle, color="#FF4040"]\n' % (obj.encode('utf-8')))
                out.write('\t%s -> %s [label="%s"]\n' % (sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))
            elif pre == "is_son":
                out.write('\t%s -> %s [label="%s", color="#0090FF"]\n' % (
                    sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))
            elif pre == "is_parent":
                out.write('\t%s -> %s [label="%s", color="#F58735"]\n' % (
                    sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))
            elif pre == "is_grandparent":
                out.write('\t%s -> %s [label="%s", color="#21988C"]\n' % (
                    sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))
            elif pre == "is_great_grandparent":
                out.write('\t%s -> %s [label="%s", color="#8D430C"]\n' % (
                    sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))
            elif pre == "is_grandchildren":
                out.write('\t%s -> %s [label="%s", color="#AB754E"]\n' % (
                    sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))
            elif pre == "is_brother":
                out.write('\t%s -> %s [label="%s", color="#8727A2"]\n' % (
                    sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))
            elif pre == "is_couple":
                out.write('\t%s -> %s [label="%s", color="#F5E635"]\n' % (
                    sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))
            elif pre == "is_cousin":
                out.write('\t%s -> %s [label="%s", color="#4A095D"]\n' % (
                    sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))
            elif pre == "is_uncle":
                out.write('\t%s -> %s [label="%s", color="#8D0F0C"]\n' % (
                    sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))
            elif pre == "is_nephew":
                out.write('\t%s -> %s [label="%s", color="#AB5E4E"]\n' % (
                    sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))
            else:
                out.write('\t%s -> %s [label="%s"]\n' % (sub.encode('utf-8'), obj.encode('utf-8'), pre.encode('utf-8')))

        out.write('\t{'
                  '\t\trank = sink;\n'
                  '\t\tLegend [shape=none, margin=0, label=<\n'
                  '\t\t<table BORDER="0" cellborder="1" cellspacing="0" cellpadding="4">\n'
                  '\t\t\t<tr>\n'
                  '\t\t\t\t<td colspan="2">\n'
                  '\t\t\t\t\t<b>Legend</b>\n'
                  '\t\t\t\t</td>\n'
                  '\t\t\t</tr>\n'
                  '\t\t\t<tr>\n'
                  '\t\t\t\t<td>is_son</td>\n'
                  '\t\t\t\t<td bgcolor="#0090FF"></td>\n'
                  '\t\t\t</tr>\n'
                  '\t\t\t<tr>\n'
                  '\t\t\t\t<td>is_parent</td>\n'
                  '\t\t\t\t<td bgcolor="#F58735"></td>\n'
                  '\t\t\t</tr>\n'
                  '\t\t\t<tr>\n'
                  '\t\t\t\t<td>is_grandparent</td>\n'
                  '\t\t\t\t<td bgcolor="#21988C"></td>\n'
                  '\t\t\t</tr>\n'
                  '\t\t\t<tr>\n'
                  '\t\t\t\t<td>is_great_grandparent</td>\n'
                  '\t\t\t\t<td bgcolor="#8D430C"></td>\n'
                  '\t\t\t</tr>\n'
                  '\t\t\t<tr>\n'
                  '\t\t\t\t<td>is_grandchildren</td>\n'
                  '\t\t\t\t<td bgcolor="#AB754E"></td>\n'
                  '\t\t\t</tr>\n'
                  '\t\t\t<tr>\n'
                  '\t\t\t\t<td>is_brother</td>\n'
                  '\t\t\t\t<td bgcolor="#8727A2"></td>\n'
                  '\t\t\t</tr>\n'
                  '\t\t\t<tr>\n'
                  '\t\t\t\t<td>is_couple</td>\n'
                  '\t\t\t\t<td bgcolor="#F5E635"></td>\n'
                  '\t\t\t</tr>\n'
                  '\t\t\t<tr>\n'
                  '\t\t\t\t<td>is_cousin</td>\n'
                  '\t\t\t\t<td bgcolor="#4A095D"></td>\n'
                  '\t\t\t</tr>\n'
                  '\t\t\t<tr>\n'
                  '\t\t\t\t<td>is_uncle</td>\n'
                  '\t\t\t\t<td bgcolor="#8D0F0C"></td>\n'
                  '\t\t\t</tr>\n'
                  '\t\t\t<tr>\n'
                  '\t\t\t\t<td>is_nephew</td>\n'
                  '\t\t\t\t<td bgcolor="#AB5E4E"></td>\n'
                  '\t\t\t</tr>\n'
                  '\t\t</table>\n'
                  '\t\t>];\n'
                  '\t}')
        out.write('}\n')
        out.close()


    def triplestodot(self):
        print ("triplestodot")

        graph = pydot.Dot(graph_type='digraph', labelloc='t', label='Trabalho Prático - Web Semântica')
        for sub, pre, obj in self.triples(None, None, None):
            if pre == "is_parent" or pre == "is_grandparent" or pre == "is_great_grandparent" or pre == "is_grandchildren" or pre == "is_brother" or pre == "is_couple" or pre == "is_cousin" or pre == "is_uncle" or pre == "is_nephew":
                color = "#FF4040"
            else:
                color = "#000000"
            node_a = pydot.Node(sub.encode('utf-8'), shape="circle")
            graph.add_node(node_a)
            node_b = pydot.Node(obj.encode('utf-8'), shape="circle")
            graph.add_node(node_b)
            graph.add_edge(pydot.Edge(node_a, node_b, label=pre.encode('utf-8'), color=color))

        graph.write_png('graph.png')
        graph.write('graph.dot')
        im1 = Image.open("graph.png")
        im1.show()

    #pesquisa de um triplo
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
                                        result.append(retSub, retPre, obj)
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
        doc = open(filename, "r")
        reader = csv.reader(doc)
        for sub, pre, obj in reader:
            self.add(sub, pre, obj)
        doc.close()

    # guarda o conteudo num ficheiro .csv
    def save(self, filename):
        doc = open(filename, "wb")
        writer = csv.writer(doc)
        print (self.triples((None, None, None)))

        for sub, pre, obj in self.triples((None, None, None)):
            writer.writerow([sub, pre, obj])
        doc.close()

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
                    qc.append(None)          # adiciona o valor None à lista de elementos a pssar ao método triples
                    #bpos[x] = pos            # guarda a posição da variável no triplo (0,1 ou 2)
                    bpos[x[
                         1:]] = pos          # linha de cima re-escrita porque é necessário guardar o nome da variável, mas sem o ponto de interrogação (?)
                else:
                    qc.append(x)             # adiciona o valor dado à lista de elementos a pssar ao método triples

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
                # Retira da lista dicionários, aqueles que
                newb = []                    # cria nova lista a devolver
                for binding in bindings:     # para cada dicionario da lista de dicionarios
                    for row in rows:         # para cada triplo resultado
                        validmatch = True    # começa por assumir que o dicionario serve
                        tempbinding = binding.copy() # faz copia temporaria do dicionario
                        for var, pos in bpos.items(): # para cada variavel em sua posição
                            if var in tempbinding: # caso a variavel esteja presente no dicionario
                                if tempbinding[var] != row[
                                    pos]: # se o valor da variavel diferente do valor na sua posicao no triplo
                                    validmatch = False # o dicionário não serve
                            else:
                                tempbinding[var] = row[
                                    pos] # associa à variável o valor do elemento do triplo na sua posição
                        if validmatch:
                            newb.append(tempbinding) # se dicionario serve, inclui-o na nova lista
                bindings = newb              # sbstituiu lista por nova
        return bindings

    def applyInferenceParent(self, rule):
        graph = grafo()
        queries = rule.getQueries()
        bindings = []
        for query in queries:
            bindings += self.query(query)
        for b in bindings:
            pai = b.get('idPai')
            filho = b.get('idFilho')
            new_triples = rule.makeTriples(pai, filho)
            for triple in new_triples:
                if triple[0] == None:
                    print ('error')
                elif triple[1] == None:
                    print ('error')
                elif triple[2] == None:
                    print ('error')
                else:
                    graph.add((triple[0], triple[1], triple[2]))
        graph.save('Inferences/Parent.csv')

    def applyInferenceGrandParent(self, rule):
        graph = grafo()
        queries = rule.getQueries()
        bindings = []
        for query in queries:
            bindings += self.query(query)
        for b in bindings:
            avo = b.get('idAvo')
            neto = b.get('idNeto')
            new_triples = rule.makeTriples(avo, neto)
            for triple in new_triples:
                if triple[0] == None:
                    print ('error')
                elif triple[1] == None:
                    print ('error')
                elif triple[2] == None:
                    print ('error')
                else:
                    graph.add((triple[0], triple[1], triple[2]))

        graph.save('Inferences/GrandParent.csv')

    def applyInferenceGreatGrandParent(self, rule):
        graph = grafo()
        queries = rule.getQueries()
        bindings = []
        for query in queries:
            bindings += self.query(query)
        for b in bindings:
            bisavo = b.get('idBisAvo')
            neto = b.get('idNeto')
            new_triples = rule.makeTriples(bisavo, neto)
            for triple in new_triples:
                if triple[0] == None:
                    print ('error')
                elif triple[1] == None:
                    print ('error')
                elif triple[2] == None:
                    print ('error')
                else:
                    graph.add((triple[0], triple[1], triple[2]))

        graph.save('Inferences/GreatGrandParent.csv')

    def applyInferenceGrandChildren(self, rule):
        graph = grafo()
        queries = rule.getQueries()
        bindings = []
        for query in queries:
            bindings += self.query(query)
        for b in bindings:
            avo = b.get('idAvo')
            neto = b.get('idNeto')
            new_triples = rule.makeTriples(avo, neto)
            for triple in new_triples:
                if triple[0] == None:
                    print ('error')
                elif triple[1] == None:
                    print ('error')
                elif triple[2] == None:
                    print ('error')
                else:
                    graph.add((triple[0], triple[1], triple[2]))

        graph.save('Inferences/GrandChildren.csv')

    def applyInferenceBrother(self, rule):
        graph = grafo()
        queries = rule.getQueries()
        bindings = []
        for query in queries:
            bindings += self.query(query)
        for b in bindings:
            irmao1 = b.get('idIrmao1')
            irmao2 = b.get('idIrmao2')
            if (irmao1 != irmao2):
                new_triples = rule.makeTriples(irmao1, irmao2)
                for triple in new_triples:
                    if triple[0] == None:
                        print ('error')
                    elif triple[1] == None:
                        print ('error')
                    elif triple[2] == None:
                        print ('error')
                    else:
                        graph.add((triple[0], triple[1], triple[2]))

        graph.save('Inferences/Brother.csv')

    def applyInferenceCouple(self, rule):
        graph = grafo()
        queries = rule.getQueries()
        bindings = []
        for query in queries:
            bindings += self.query(query)
        for b in bindings:
            pessoa1 = b.get('idCouple1')
            pessoa2 = b.get('idCouple2')
            new_triples = rule.makeTriples(pessoa1, pessoa2)
            for triple in new_triples:
                if triple[0] == None:
                    print ('error')
                elif triple[1] == None:
                    print ('error')
                elif triple[2] == None:
                    print ('error')
                else:
                    graph.add((triple[0], triple[1], triple[2]))

        graph.save('Inferences/Couple.csv')

    def applyInferenceCousin(self, rule):
        graph = grafo()
        queries = rule.getQueries()
        bindings = []
        for query in queries:
            bindings += self.query(query)
        for b in bindings:
            primo1 = b.get('idPrimo1')
            primo2 = b.get('idPrimo2')
            new_triples = rule.makeTriples(primo1, primo2)
            for triple in new_triples:
                if triple[0] == None:
                    print ('error')
                elif triple[1] == None:
                    print ('error')
                elif triple[2] == None:
                    print ('error')
                else:
                    graph.add((triple[0], triple[1], triple[2]))

        graph.save('Inferences/Cousin.csv')

    def applyInferenceUncle(self, rule):
        graph = grafo()
        queries = rule.getQueries()
        bindings = []
        for query in queries:
            bindings += self.query(query)
        for b in bindings:
            tio = b.get('idTio')
            sobrinho = b.get('idSobrinho')
            new_triples = rule.makeTriples(tio, sobrinho)
            for triple in new_triples:
                if triple[0] == None:
                    print ('error')
                elif triple[1] == None:
                    print ('error')
                elif triple[2] == None:
                    print ('error')
                else:
                    graph.add((triple[0], triple[1], triple[2]))

        graph.save('Inferences/Uncle.csv')

    def applyInferenceNephew(self, rule):
        graph = grafo()
        queries = rule.getQueries()
        bindings = []
        for query in queries:
            bindings += self.query(query)
        for b in bindings:
            tio = b.get('idTio')
            sobrinho = b.get('idSobrinho')
            new_triples = rule.makeTriples(tio, sobrinho)
            for triple in new_triples:
                if triple[0] == None:
                    print ('error')
                elif triple[1] == None:
                    print ('error')
                elif triple[2] == None:
                    print ('error')
                else:
                    graph.add((triple[0], triple[1], triple[2]))

        graph.save('Inferences/Nephew.csv')