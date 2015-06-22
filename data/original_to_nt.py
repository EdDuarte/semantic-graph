__author__ = 'Ed Duarte'
__email__ = "edmiguelduarte@gmail.com"
__copyright__ = "Copyright 2015, Ed Duarte"
__credits__ = ["Ed Duarte"]

__license__ = "Apache License 2.0"
__version__ = "2.0.0"
__maintainer__ = "Ed Duarte"
__status__ = "Prototype"

import csv

doc = open("original.csv", "r")
reader = csv.reader(doc)

kingdom = dict()
phylum = dict()
classes = dict()
order = dict()
family = dict()
species = dict()
common = dict()
state = dict()

index = 1
isFirstLine = True

triples = list()

for column in reader:
    if isFirstLine:
        isFirstLine = False
        continue

    if column[0] not in kingdom.keys():
        kingdom.update({column[0]: "<http://www.semanticweb.prv/taxonomy/" + str(index) + ">"})
        index += 1
    if column[1] not in phylum.keys():
        phylum.update({column[1]: "<http://www.semanticweb.prv/taxonomy/" + str(index) + ">"})
        index += 1
    if column[2] not in classes.keys():
        classes.update({column[2]: "<http://www.semanticweb.prv/taxonomy/" + str(index) + ">"})
        index += 1
    if column[3] not in order.keys():
        order.update({column[3]: "<http://www.semanticweb.prv/taxonomy/" + str(index) + ">"})
        index += 1
    if column[4] not in family.keys():
        family.update({column[4]: "<http://www.semanticweb.prv/taxonomy/" + str(index) + ">"})
        index += 1
    if column[5] not in species.keys():
        species.update({column[5]: "<http://www.semanticweb.prv/taxonomy/" + str(index) + ">"})
        index += 1

    if (index == 7):
        triples.append(
            str(kingdom.get(column[0])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                0] + '" .')
        triples.append(
            str(phylum.get(column[1])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                1] + '" .')
        triples.append(
            str(classes.get(column[2])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                2] + '" .')
        triples.append(
            str(order.get(column[3])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                3] + '" .')
        triples.append(
            str(family.get(column[4])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                4] + '" .')
        triples.append(
            str(species.get(column[5])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                5] + '" .')
    else:
        triples.append(
            str(kingdom.get(column[0])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                0] + '" .')
        triples.append(str(kingdom.get(
            column[0])) + ' rdf:type <http://www.semanticweb.prv/taxonomy#Kingdom>.')

        triples.append(
            str(phylum.get(column[1])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                1] + '" .')
        triples.append(str(phylum.get(
            column[1])) + ' rdf:type <http://www.semanticweb.prv/taxonomy#Phylum>.')
        triples.append(
            str(phylum.get(column[1])) + ' owl:belongsTo ' + str(
                kingdom.get(column[0])) + '.')

        triples.append(
            str(classes.get(column[2])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                2] + '" .')
        triples.append(str(classes.get(
            column[2])) + ' rdf:type <http://www.semanticweb.prv/taxonomy#Class>.')
        triples.append(str(
            classes.get(column[2])) + ' owl:belongsTo ' + str(
            phylum.get(column[1])) + '.')

        triples.append(
            str(order.get(column[3])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                3] + '" .')
        triples.append(str(order.get(
            column[3])) + ' rdf:type <http://www.semanticweb.prv/taxonomy#Order>.')
        triples.append(
            str(order.get(column[3])) + ' owl:belongsTo ' + str(
                classes.get(column[2])) + '.')

        triples.append(
            str(family.get(column[4])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                4] + '" .')
        triples.append(str(family.get(
            column[4])) + ' rdf:type <http://www.semanticweb.prv/taxonomy#Family>.')
        triples.append(
            str(family.get(column[4])) + ' owl:belongsTo ' + str(
                order.get(column[3])) + '.')

        triples.append(
            str(species.get(column[5])) + ' <http://www.semanticweb.prv/taxonomy/name> "' + column[
                5] + '" .')
        triples.append(str(species.get(
            column[5])) + ' rdf:type <http://www.semanticweb.prv/taxonomy#Species>.')
        triples.append(str(
            species.get(column[5])) + ' owl:belongsTo ' + str(
            family.get(column[4])) + '.')

doc.close()

fp = open("data.nt", "w")

for t in triples:
    fp.write(t + '\n')

fp.close()