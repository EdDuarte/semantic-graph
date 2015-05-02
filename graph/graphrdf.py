# #!/usr/bin/python
# # -*- coding: utf-8 -*-
#
# __author__ = 'edduarte'
#
# import csv
# import os.path
# import sys
# import time
# from rdflib import plugin, store
# from rdflib import ConjunctiveGraph
# # from inferencerule import *
#
#
# class GraphRdf():
#
#     options = ["name", "is_son", "is_parent", "is_grandparent", "is_great_grandparent", "is_grandchildren",
#                "is_brother", "is_couple", "is_cousin", "is_uncle", "is_nephew"]
#     optionsQuery = ["is_son", "is_parent", "is_grandparent", "is_great_grandparent", "is_grandchildren",
#                     "is_brother", "is_couple", "is_cousin", "is_uncle", "is_nephew"]
#     optionLoadSave = [("RDF/NT", 0), ("RDF/N3", 1), ("RDF/XML", 2), ("SQLITE", 3)]
#
#     typeFileRead = 'n3'
#
#     # Create Graph
#     def __init__(self):
#         self.graph = ConjunctiveGraph()
#
#     # Load graph from file
#     def load(self, filename, file_format):
#         # """
#         # load Method
#         # """
#         # print("LOAD")
#         # file_type = ("", "")
#         # file_format = ""
#         # if self.option.get() == 0:
#         #     file_type = ('text/nt', '*.nt')
#         #     file_format = "nt"
#         # elif self.option.get() == 1:
#         #     file_type = ('text/n3', '*.n3')
#         #     file_format = "n3"
#         # elif self.option.get() == 2:
#         #     file_type = ('application/rdf+xml', '*.rdf')
#         #     file_format = "xml"
#         # elif self.option.get() == 3:
#         #     file_type = ('file/sqlite3', '*.sqlite3')
#         #     file_format = "sqlite3"
#
#         start = time.clock()
#         if filename != '':
#             if file_format == "sqlite3":
#                 bd = plugin.get('SQLite', store.Store)(filename)
#                 bd.open(filename, create=False)
#                 g = ConjunctiveGraph(bd)
#                 self.graph += g
#
#             else:
#                 self.graph.parse(filename, format=file_format)
#                 self.applyInferences()
#
#         elapsed = (time.clock() - start)
#         print("Elapsed file loading time: %ss" % elapsed)
#
#
#     def save(self, filename, file_format):
#         # """
#         # Save Method
#         # """
#         # print("SAVE")
#         #
#         # filename = ""
#         # type_file = ""
#         # if self.option.get() == 0:
#         #     filename = tkFileDialog.asksaveasfilename(filetypes=[('text/plain', '*.nt')])
#         #     type_file = "nt"
#         # elif self.option.get() == 1:
#         #     filename = tkFileDialog.asksaveasfilename(filetypes=[('text/n3', '*.n3')])
#         #     type_file = "n3"
#         # elif self.option.get() == 2:
#         #     filename = tkFileDialog.asksaveasfilename(filetypes=[('application/rdf+xml', '*.rdf')])
#         #     type_file = "pretty-xml"
#         # elif self.option.get() == 3:
#         #     filename = tkFileDialog.asksaveasfilename(filetypes=[('file/sqlite3', '*.sqlite3')])
#         #     type_file = "sqlite3"
#
#         start = time.clock()
#         if filename != '':
#             if type_file == "sqlite3":
#                 bd = plugin.get('SQLite', store.Store)(filename)
#                 bd.open(filename, create=True)
#                 g = ConjunctiveGraph(bd)
#                 g += self.graph
#                 g.commit()
#             else:
#                 of = open(filename, "wb")
#                 print "type_file:", type_file
#                 of.write(self.graph.serialize(format=type_file))
#                 of.close()
#             tkMessageBox.showinfo("Save", "Ficheiro criado com sucesso")
#         elapsed = (time.clock() - start)
#         print "Time SAVE: %ss" % elapsed
#
#     ################### Edit ###################
#     def interfaceAdd(self):
#         """
#         Add Interface
#         """
#         print "interfaceAdd"
#         addInterface = Toplevel()
#         addInterface.title("Add Triple")
#         subjectFrame = Frame(addInterface)
#         self.subject = StringVar()
#         Label(subjectFrame, text="Subject:", width=8).pack(side=LEFT)
#         Entry(subjectFrame, textvariable=self.subject, width=20).pack()
#         subjectFrame.pack()
#
#         predicateFrame = Frame(addInterface)
#         self.predicate = StringVar()
#         Label(predicateFrame, text="Predicate:", width=8).pack(side=LEFT)
#         opMenu = OptionMenu(predicateFrame, self.predicate, *self.options)
#         opMenu["width"] = 20
#         opMenu.pack(side=LEFT)
#         predicateFrame.pack()
#
#         objectFrame = Frame(addInterface)
#         self.object = StringVar()
#         Label(objectFrame, text="Object:", width=8).pack(side=LEFT)
#         Entry(objectFrame, textvariable=self.object, width=20).pack()
#         objectFrame.pack()
#
#         buttonFrame = Frame(addInterface)
#         cancelButton = Button(buttonFrame, text="Cancel", command=addInterface.destroy)
#         addButton = Button(buttonFrame, text="Add", command=self.add)
#         cancelButton.pack(side=LEFT)
#         addButton.pack()
#         buttonFrame.pack()
#
#     def add(self, *args):
#         """
#         Add Method
#         """
#         print "ADD"
#         try:
#             sub = self.subject.get()
#             pre = self.predicate.get()
#             obj = self.object.get()
#
#             if sub != "" and pre != "" and obj != "":
#                 start = time.clock()
#                 sub = 'http://arvoregenealogica/' + sub
#                 pre = 'http://arvoregenealogica/' + pre
#                 obj = 'http://arvoregenealogica/' + obj
#                 self.graph.add((sub, pre, obj))
#                 elapsed = (time.clock() - start)
#                 print "Time ADD: %ss" % elapsed
#                 self.applyInferences()
#                 tkMessageBox.showinfo("Add", "Triplo Adicionado com sucesso")
#             else:
#                 tkMessageBox.showwarning("Add", "Preencha correctamente os campos")
#             self.cleanFields()
#         except KeyError:
#             tkMessageBox.showerror("Add", "ERROR: Não foi adicionado!")
#             pass
#
#     def interfaceRemove(self):
#         """
#         Remove Interface
#         """
#         print "interfaceRemove"
#         removeInterface = Toplevel()
#         removeInterface.title("Remove Triple")
#         subjectFrame = Frame(removeInterface)
#         self.subject = StringVar()
#         Label(subjectFrame, text="Subject:", width=8).pack(side=LEFT)
#         Entry(subjectFrame, textvariable=self.subject).pack()
#         subjectFrame.pack()
#
#         predicateFrame = Frame(removeInterface)
#         self.predicate = StringVar()
#         Label(predicateFrame, text="Predicate:", width=8).pack(side=LEFT)
#         opMenu = OptionMenu(predicateFrame, self.predicate, *self.options)
#         opMenu["width"] = 20
#         opMenu.pack(side=LEFT)
#         predicateFrame.pack()
#
#         objectFrame = Frame(removeInterface)
#         self.object = StringVar()
#         Label(objectFrame, text="Object:", width=8).pack(side=LEFT)
#         Entry(objectFrame, textvariable=self.object).pack()
#         objectFrame.pack()
#
#         buttonFrame = Frame(removeInterface)
#         cancelButton = Button(buttonFrame, text="Cancel", command=removeInterface.destroy)
#         addButton = Button(buttonFrame, text="Remove", command=self.remove)
#         cancelButton.pack(side=LEFT)
#         addButton.pack()
#         buttonFrame.pack()
#
#     def remove(self):
#         """
#         Remove Method
#         """
#         print "REMOVE"
#         sub = self.subject.get()
#         pre = self.predicate.get()
#         obj = self.object.get()
#
#         sub = 'http://arvoregenealogica/' + sub
#         pre = 'http://arvoregenealogica/' + pre
#         obj = 'http://arvoregenealogica/' + obj
#
#         try:
#             if sub != "" and pre != "" and obj != "":
#                 start = time.clock()
#                 self.graph.remove((sub, pre, obj))
#                 elapsed = (time.clock() - start)
#                 print "Time REMOVE: %ss" % elapsed
#                 self.applyInferences()
#                 tkMessageBox.showinfo("Remove", "Triplo Removido com sucesso")
#                 self.cleanFields()
#             else:
#                 tkMessageBox.showwarning("Remove", "Preencha correctamente os campos")
#         except KeyError:
#             tkMessageBox.showerror("Remove", "ERROR: Triplo inexistente!")
#             pass
#
#     def interfaceInference(self):
#         """
#         Inferences Interface
#         """
#         print "interfaceInference"
#         inferenceInterface = Toplevel()
#         inferenceInterface.title("Inference")
#         inferenceInterfaceFrame = Frame(inferenceInterface)
#         inferenceFrame = Frame(inferenceInterfaceFrame)
#
#         self.is_parent = IntVar()
#         self.is_grandparent = IntVar()
#         self.is_great_grandparent = IntVar()
#         self.is_grandchildren = IntVar()
#         self.is_brother = IntVar()
#         self.is_couple = IntVar()
#         self.is_cousin = IntVar()
#         self.is_uncle = IntVar()
#         self.is_nephew = IntVar()
#
#         Checkbutton(inferenceFrame, text="is_parent", variable=self.is_parent, width=20, justify=LEFT).pack()
#         Checkbutton(inferenceFrame, text="is_grandparent", variable=self.is_grandparent, width=20, justify=LEFT).pack()
#         Checkbutton(inferenceFrame, text="is_great_grandparent", variable=self.is_great_grandparent, width=20,
#                     justify=LEFT).pack()
#         Checkbutton(inferenceFrame, text="is_grandchildren", variable=self.is_grandchildren, width=20,
#                     justify=LEFT).pack()
#         Checkbutton(inferenceFrame, text="is_brother", variable=self.is_brother, width=20, justify=LEFT).pack()
#         Checkbutton(inferenceFrame, text="is_couple", variable=self.is_couple, width=20, justify=LEFT).pack()
#         Checkbutton(inferenceFrame, text="is_cousin", variable=self.is_cousin, width=20, justify=LEFT).pack()
#         Checkbutton(inferenceFrame, text="is_uncle", variable=self.is_uncle, width=20, justify=LEFT).pack()
#         Checkbutton(inferenceFrame, text="is_nephew", variable=self.is_nephew, width=20, justify=LEFT).pack()
#
#         inferenceFrame.pack(side=LEFT)
#         resultFrame = Frame(inferenceInterfaceFrame)
#         scrollbar = Scrollbar(resultFrame)
#         scrollbar.pack(side=RIGHT, fill=Y)
#         self.resultInference = Text(resultFrame, wrap=WORD, yscrollcommand=scrollbar.set, height=15, width=30)
#         self.resultInference.pack()
#         resultFrame.pack()
#         inferenceInterfaceFrame.pack()
#
#         buttonFrame = Frame(inferenceInterface)
#         Button(buttonFrame, text="Cancel", command=inferenceInterface.destroy).pack(side=LEFT)
#         Button(buttonFrame, text="Create", command=self.inference).pack()
#         buttonFrame.pack()
#
#     def inference(self):
#         """
#         Inferences Method
#         """
#         print "INFERENCE"
#         self.resultInference.config(state=NORMAL)
#         self.resultInference.delete(1.0, END)
#
#         if self.is_parent.get() == 1:
#             fileParent = "Inferences/Parent.n3"
#             self.graph.parse(fileParent, format=self.typeFileRead)
#             self.readInferences(fileParent)
#
#         if self.is_grandparent.get() == 1:
#             fileGrandParent = "Inferences/GrandParent.n3"
#             self.graph.parse(fileGrandParent, format=self.typeFileRead)
#             self.readInferences(fileGrandParent)
#
#         if self.is_great_grandparent.get() == 1:
#             fileGreatGrandParent = "Inferences/GreatGrandParent.n3"
#             self.graph.parse(fileGreatGrandParent, format=self.typeFileRead)
#             self.readInferences(fileGreatGrandParent)
#
#         if self.is_grandchildren.get() == 1:
#             fileGrandChildren = "Inferences/GrandChildren.n3"
#             self.graph.parse(fileGrandChildren, format=self.typeFileRead)
#             self.readInferences(fileGrandChildren)
#
#         if self.is_brother.get() == 1:
#             fileBrother = "Inferences/Brother.n3"
#             self.graph.parse(fileBrother, format=self.typeFileRead)
#             self.readInferences(fileBrother)
#
#         if self.is_couple.get() == 1:
#             fileCouple = "Inferences/Couple.n3"
#             self.graph.parse(fileCouple, format=self.typeFileRead)
#             self.readInferences(fileCouple)
#
#         if self.is_cousin.get() == 1:
#             fileCousin = "Inferences/Cousin.n3"
#             self.graph.parse(fileCousin, format=self.typeFileRead)
#             self.readInferences(fileCousin)
#
#         if self.is_uncle.get() == 1:
#             fileUncle = "Inferences/Uncle.n3"
#             self.graph.parse(fileUncle, format=self.typeFileRead)
#             self.readInferences(fileUncle)
#
#         if self.is_nephew.get() == 1:
#             fileNephew = "Inferences/Nephew.n3"
#             self.graph.parse(fileNephew, format=self.typeFileRead)
#             self.readInferences(fileNephew)
#
#         self.resultInference.config(state=DISABLED)
#
#     ################### Search ###################
#     def interfaceQuery(self):
#         """
#         Query Interface
#         """
#         print "interfaceQuery"
#         queryInterface = Toplevel()
#         queryInterface.title("Query")
#         subjectFrame = Frame(queryInterface)
#         self.q = StringVar()
#         Label(subjectFrame, text="Search:", width=10).pack(side=LEFT)
#         Entry(subjectFrame, textvariable=self.q).pack()
#         subjectFrame.pack()
#
#         predicateFrame = Frame(queryInterface)
#         self.predicate = StringVar()
#         Label(predicateFrame, text="Relationship:", width=10).pack(side=LEFT)
#         opMenu = OptionMenu(predicateFrame, self.predicate, *self.optionsQuery)
#         opMenu["width"] = 20
#         opMenu.pack(side=LEFT)
#         predicateFrame.pack()
#
#         buttonFrame = Frame(queryInterface)
#         cancelButton = Button(buttonFrame, text="Cancel", command=queryInterface.destroy)
#         addButton = Button(buttonFrame, text="Search", command=self.query)
#         cancelButton.pack(side=LEFT)
#         addButton.pack()
#         buttonFrame.pack()
#
#         scrollbar = Scrollbar(queryInterface)
#         scrollbar.pack(side=RIGHT, fill=Y)
#
#         self.resultQuery = Text(queryInterface, wrap=WORD, yscrollcommand=scrollbar.set, height=10, width=60)
#         self.resultQuery.pack()
#         self.resultQuery.config(state=DISABLED)
#         scrollbar.config(command=self.resultQuery.yview)
#
#     def query(self):
#         """
#         Query Method
#         """
#         print "QUERY"
#         q = self.q.get()
#         pre = self.predicate.get()
#         print "q:", q
#         print "pre:", pre
#         try:
#             if q != "" and pre != "":
#                 start = time.clock()
#                 query = '''
#                 PREFIX avr: <http://arvoregenealogica/>
#                 SELECT ?name
#                 WHERE{
#                 ?id1 avr:name \'''' + q + '''\' .
#                 ?id1 avr:''' + pre + ''' ?id2 .
#                 ?id2 avr:name ?name .
#                 }'''
#
#                 result = self.graph.query(query)
#
#                 self.resultQuery.config(state=NORMAL)
#                 self.resultQuery.delete(1.0, END)
#                 elapsed = (time.clock() - start)
#                 print "Time QUERY: %ss" % elapsed
#                 if len(result) == 0:
#                     self.resultQuery.insert(INSERT, "Não existe correspondência.")
#                     self.resultQuery.insert(INSERT, "\n")
#                 else:
#                     title = q + " " + pre + ":"
#                     self.resultQuery.insert(INSERT, title)
#                     self.resultQuery.insert(INSERT, "\n")
#                     for [n] in result:
#                         self.resultQuery.insert(INSERT, n)
#                         self.resultQuery.insert(INSERT, "\n")
#                 self.resultQuery.config(state=DISABLED)
#                 self.cleanFieldsQuery()
#             else:
#                 tkMessageBox.showwarning("Query", "Preencha correctamente os campos")
#         except KeyError:
#             tkMessageBox.showerror("Query", "ERROR: Triplo inexistente!")
#             pass
#
#     ################### View ###################
#     def interfaceGraph(self):
#         """
#         Graph Interface
#         """
#         print "interfaceGraph"
#         start = time.clock()
#         self.triplestodot()
#         elapsed = (time.clock() - start)
#         print "Time GRAPH: %ss" % elapsed
#
#
#     def triplestodot(self):
#         print "triplestodot"
#
#         graph = pydot.Dot(graph_type='digraph', labelloc='t', label='Trabalho Prático - Web Semântica')
#         for sub, pre, obj in self.graph.triples((None, None, None)):
#             sub = sub.replace('http://arvoregenealogica/', '')
#             pre = pre.replace('http://arvoregenealogica/', '')
#             obj = obj.replace('http://arvoregenealogica/', '')
#
#             if pre == "is_parent" or pre == "is_grandparent" or pre == "is_great_grandparent" or pre == "is_grandchildren" or pre == "is_brother" or pre == "is_couple" or pre == "is_cousin" or pre == "is_uncle" or pre == "is_nephew":
#                 color = "#FF4040"
#             else:
#                 color = "#000000"
#             node_a = pydot.Node(sub.encode('utf-8'), shape="circle")
#             graph.add_node(node_a)
#             node_b = pydot.Node(obj.encode('utf-8'), shape="circle")
#             graph.add_node(node_b)
#             graph.add_edge(pydot.Edge(node_a, node_b, label=pre.encode('utf-8'), color=color))
#
#         graph.write_png('graph.png')
#         graph.write('graph.dot')
#         im1 = Image.open("graph.png")
#         im1.show()
#
#
#     ################### Help ###################
#     def interfaceAbout(self):
#         """
#         About Interface
#         """
#         print "About"
#         tkMessageBox.showinfo("About", "Trabalho Prático 1\n"
#                                        "Web Semântica\n"
#                                        "Mestrado em Sistemas de Informação \n\n"
#                                        "Joana Coelho:\tjoana.coelho@ua.pt\n"
#                                        "Ricardo Mendes:\tricardo.mendes@ua.pt")
#
#     ################### Support ###################
#     def cleanFields(self):
#         """
#         Clean Fields in Form Add and Remove
#         """
#         self.subject.set("")
#         self.predicate.set("")
#         self.object.set("")
#
#     def cleanFieldsQuery(self):
#         """
#         Clean Fields in Form Query
#         """
#         self.q.set("")
#         self.predicate.set("")
#
#     def applyInferences(self):
#         """
#         Apply Inferences
#         """
#         start = time.clock()
#         self.Rules(BrotherRule(), "Inferences/Brother.n3")
#         self.graph.parse("Inferences/Brother.n3", format=self.typeFileRead)
#         self.Rules(ParentRule(), "Inferences/Parent.n3")
#         self.Rules(GrandParentRule(), "Inferences/GrandParent.n3")
#         self.Rules(GreatGrandParentRule(), "Inferences/GreatGrandParent.n3")
#         self.Rules(GrandChildrenRule(), "Inferences/GrandChildren.n3")
#         self.Rules(CoupleRule(), "Inferences/Couple.n3")
#         self.Rules(CousinRule(), "Inferences/Cousin.n3")
#         self.Rules(UncleRule(), "Inferences/Uncle.n3")
#         self.Rules(NephewRule(), "Inferences/Nephew.n3")
#         elapsed = (time.clock() - start)
#         print "Time Inferences: %ss" % elapsed
#
#     def Rules(self, rule, path):
#         graphAux = ConjunctiveGraph()
#         lista = rule.getQueries()
#         varQueries = self.graph.query(lista)
#
#         for b, b1 in varQueries:
#             new_triples = rule.makeTriples(b1, b)
#
#             for triple in new_triples:
#                 graphAux.add(triple)
#
#
#         ### QUERY PARA VER SE EXISTEM DADOS ###
#         # q = '''
#         # PREFIX avr: <http://arvoregenealogica/>
#         # SELECT ?id_irmao1 ?id_irmao2
#         # WHERE{
#         # ?id_irmao1 avr:is_brother ?id_irmao2\
#         # }
#         # '''
#         # listaL = self.graph.query(q)
#         # for a, b in listaL:
#         #     print "A:", a
#         #     print "B:", b
#         #     valorA = str(a).replace('http://arvoregenealogica/', '')
#         #     valorB = str(b).replace('http://arvoregenealogica/', '')
#         #     print valorA + ' irmao ' + valorB
#
#
#         # ### CONFIRMAR SE PREDICADO ADICIONADO ###
#         # lista = set(self.graph.predicates())
#         # for l in lista:
#         #     print "L:", l
#
#         of = open(path, "wb")
#         of.write(graphAux.serialize(format=self.typeFileRead))
#         of.close()
#
#
#     def readInferences(self, fileInference):
#         """
#         Open Inferences
#         """
#
#         reader = ConjunctiveGraph()
#         reader.parse(fileInference, format=self.typeFileRead)
#         read = reader.triples((None, None, None))
#         for sub, pre, obj in read:
#             sub = sub.replace('http://arvoregenealogica/', '')
#             pre = pre.replace('http://arvoregenealogica/', '')
#             obj = obj.replace('http://arvoregenealogica/', '')
#             result = sub + "," + pre + "," + obj
#             self.resultInference.insert(INSERT, result)
#             self.resultInference.insert(INSERT, "\n")
#
#
# if __name__ == '__main__':
#     GraphRdf()