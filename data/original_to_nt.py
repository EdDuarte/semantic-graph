__author__ = 'edduarte'

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

triples = list()

for column in reader:
    if column[0] not in kingdom.keys():
        kingdom.update({column[0]: "<http://taxonomy/"+str(index)+">"})
        index += 1
    if column[1] not in phylum.keys():
        phylum.update({column[1]: "<http://taxonomy/"+str(index)+">"})
        index += 1
    if column[2] not in classes.keys():
        classes.update({column[2]: "<http://taxonomy/"+str(index)+">"})
        index += 1
    if column[3] not in order.keys():
        order.update({column[3]: "<http://taxonomy/"+str(index)+">"})
        index += 1
    if column[4] not in family.keys():
        family.update({column[4]: "<http://taxonomy/"+str(index)+">"})
        index += 1
    if column[5] not in species.keys():
        species.update({column[5]: "<http://taxonomy/"+str(index)+">"})
        index += 1

    if(index == 7):
        triples.append(str(kingdom.get(column[0])) + ' <http://taxonomy/name> "' + column[0] + '" .')
        triples.append(str(phylum.get(column[1])) + ' <http://taxonomy/name> "' + column[1] + '" .')
        triples.append(str(classes.get(column[2])) + ' <http://taxonomy/name> "' + column[2] + '" .')
        triples.append(str(order.get(column[3])) + ' <http://taxonomy/name> "' + column[3] + '" .')
        triples.append(str(family.get(column[4])) + ' <http://taxonomy/name> "' + column[4] + '" .')
        triples.append(str(species.get(column[5])) + ' <http://taxonomy/name> "' + column[5] + '" .')
    else:
        triples.append(str(kingdom.get(column[0])) + ' <http://taxonomy/name> "' + column[0] + '" .')
        triples.append(str(kingdom.get(column[0])) + ' <http://taxonomy/type> <http://taxonomy/1>.')

        triples.append(str(phylum.get(column[1])) + ' <http://taxonomy/name> "' + column[1] + '" .')
        triples.append(str(phylum.get(column[1])) + ' <http://taxonomy/type> <http://taxonomy/2>.')
        triples.append(str(phylum.get(column[1])) + ' <http://taxonomy/belongs_to> ' + str(kingdom.get(column[0])) + '.')

        triples.append(str(classes.get(column[2])) + ' <http://taxonomy/name> "' + column[2] + '" .')
        triples.append(str(classes.get(column[2])) + ' <http://taxonomy/type> <http://taxonomy/3>.')
        triples.append(str(classes.get(column[2])) + ' <http://taxonomy/belongs_to> ' + str(phylum.get(column[1])) + '.')

        triples.append(str(order.get(column[3])) + ' <http://taxonomy/name> "' + column[3] + '" .')
        triples.append(str(order.get(column[3])) + ' <http://taxonomy/type> <http://taxonomy/4>.')
        triples.append(str(order.get(column[3])) + ' <http://taxonomy/belongs_to> ' + str(classes.get(column[2])) + '.')

        triples.append(str(family.get(column[4])) + ' <http://taxonomy/name> "' + column[4] + '" .')
        triples.append(str(family.get(column[4])) + ' <http://taxonomy/type> <http://taxonomy/5>.')
        triples.append(str(family.get(column[4])) + ' <http://taxonomy/belongs_to> ' + str(order.get(column[3])) + '.')

        triples.append(str(species.get(column[5])) + ' <http://taxonomy/name> "' + column[5] + '" .')
        triples.append(str(species.get(column[5])) + ' <http://taxonomy/type> <http://taxonomy/6>.')
        triples.append(str(species.get(column[5])) + ' <http://taxonomy/belongs_to> ' + str(family.get(column[4])) + '.')

doc.close()

fp = open("data.nt", "w")

for t in triples:
    fp.write(t + '\n')

fp.close()