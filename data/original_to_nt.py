__author__ = 'edduarte'

import csv

doc = open("original-data.csv", "r")
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

for row in reader:
    if row[0] not in kingdom.keys():
        kingdom.update({row[0]: "<http://taxonomy/"+str(index)+">"})
        index += 1
    if row[1] not in phylum.keys():
        phylum.update({row[1]: "<http://taxonomy/"+str(index)+">"})
        index += 1
    if row[2] not in classes.keys():
        classes.update({row[2]: "<http://taxonomy/"+str(index)+">"})
        index += 1
    if row[3] not in order.keys():
        order.update({row[3]: "<http://taxonomy/"+str(index)+">"})
        index += 1
    if row[4] not in family.keys():
        family.update({row[4]: "<http://taxonomy/"+str(index)+">"})
        index += 1
    if row[5] not in species.keys():
        species.update({row[5]: "<http://taxonomy/"+str(index)+">"})
        index += 1

    if(index == 7):
        triples.append(str(kingdom.get(row[0])) + ' <http://taxonomy/name> "' + row[0] + '" .')
        triples.append(str(phylum.get(row[1])) + ' <http://taxonomy/name> "' + row[1] + '" .')
        triples.append(str(classes.get(row[2])) + ' <http://taxonomy/name> "' + row[2] + '" .')
        triples.append(str(order.get(row[3])) + ' <http://taxonomy/name> "' + row[3] + '" .')
        triples.append(str(family.get(row[4])) + ' <http://taxonomy/name> "' + row[4] + '" .')
        triples.append(str(species.get(row[5])) + ' <http://taxonomy/name> "' + row[5] + '" .')
    else:
        triples.append(str(kingdom.get(row[0])) + ' <http://taxonomy/name> "' + row[0] + '" .')
        triples.append(str(kingdom.get(row[0])) + ' <http://taxonomy/type> <http://taxonomy/1>.')

        triples.append(str(phylum.get(row[1])) + ' <http://taxonomy/name> "' + row[1] + '" .')
        triples.append(str(phylum.get(row[1])) + ' <http://taxonomy/type> <http://taxonomy/2>.')
        triples.append(str(phylum.get(row[1])) + ' <http://taxonomy/belongs_to> ' + str(kingdom.get(row[0])) + '.')

        triples.append(str(classes.get(row[2])) + ' <http://taxonomy/name> "' + row[2] + '" .')
        triples.append(str(classes.get(row[2])) + ' <http://taxonomy/type> <http://taxonomy/3>.')
        triples.append(str(classes.get(row[2])) + ' <http://taxonomy/belongs_to> ' + str(phylum.get(row[1])) + '.')

        triples.append(str(order.get(row[3])) + ' <http://taxonomy/name> "' + row[3] + '" .')
        triples.append(str(order.get(row[3])) + ' <http://taxonomy/type> <http://taxonomy/4>.')
        triples.append(str(order.get(row[3])) + ' <http://taxonomy/belongs_to> ' + str(classes.get(row[2])) + '.')

        triples.append(str(family.get(row[4])) + ' <http://taxonomy/name> "' + row[4] + '" .')
        triples.append(str(family.get(row[4])) + ' <http://taxonomy/type> <http://taxonomy/5>.')
        triples.append(str(family.get(row[4])) + ' <http://taxonomy/belongs_to> ' + str(order.get(row[3])) + '.')

        triples.append(str(species.get(row[5])) + ' <http://taxonomy/name> "' + row[5] + '" .')
        triples.append(str(species.get(row[5])) + ' <http://taxonomy/type> <http://taxonomy/6>.')
        triples.append(str(species.get(row[5])) + ' <http://taxonomy/belongs_to> ' + str(family.get(row[4])) + '.')

doc.close()

fp = open("nt-data.nt", "w")

for t in triples:
    fp.write(t + '\n')

fp.close()