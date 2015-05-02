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

iterator = 1

lista = list()

for row in reader:
    if row[0] not in kingdom.keys():
        kingdom.update({row[0]: iterator})
        iterator += 1
    if row[1] not in phylum.keys():
        phylum.update({row[1]: iterator})
        iterator += 1
    if row[2] not in classes.keys():
        classes.update({row[2]: iterator})
        iterator += 1
    if row[3] not in order.keys():
        order.update({row[3]: iterator})
        iterator += 1
    if row[4] not in family.keys():
        family.update({row[4]: iterator})
        iterator += 1
    if row[5] not in species.keys():
        species.update({row[5]: iterator})
        iterator += 1
    # if row[6] not in common.keys():
    #     common.update({row[6]: iterator})
    #     iterator += 1
    # if row[7] not in state.keys():
    #     state.update({row[7]: iterator})
    #     iterator += 1
    if(iterator == 7):
        lista.append(str(kingdom.get(row[0])) + ',name,' + row[0])
        lista.append(str(phylum.get(row[1])) + ',name,' + row[1])
        lista.append(str(classes.get(row[2])) + ',name,' + row[2])
        lista.append(str(order.get(row[3])) + ',name,' + row[3])
        lista.append(str(family.get(row[4])) + ',name,' + row[4])
        lista.append(str(species.get(row[5])) + ',name,' + row[5])
        # lista.append(str(common.get(row[6])) + ',name,' + row[6])
        # lista.append(str(state.get(row[7])) + ',name,' + row[7])
    else:
        lista.append(str(kingdom.get(row[0])) + ',name,' + row[0])
        lista.append(str(kingdom.get(row[0])) + ',type,1')
        lista.append(str(phylum.get(row[1])) + ',name,' + row[1])
        lista.append(str(phylum.get(row[1])) + ',type,2')
        lista.append(str(phylum.get(row[1])) + ',belongs_to,' + str(kingdom.get(row[0])))
        lista.append(str(classes.get(row[2])) + ',name,' + row[2])
        lista.append(str(classes.get(row[2])) + ',type,3')
        lista.append(str(classes.get(row[2])) + ',belongs_to,' + str(phylum.get(row[1])))
        lista.append(str(order.get(row[3])) + ',name,' + row[3])
        lista.append(str(order.get(row[3])) + ',type,4')
        lista.append(str(order.get(row[3])) + ',belongs_to,' + str(classes.get(row[2])))
        lista.append(str(family.get(row[4])) + ',name,' + row[4])
        lista.append(str(family.get(row[4])) + ',type,5')
        lista.append(str(family.get(row[4])) + ',belongs_to,' + str(order.get(row[3])))
        lista.append(str(species.get(row[5])) + ',name,' + row[5])
        lista.append(str(species.get(row[5])) + ',type,6')
        lista.append(str(species.get(row[5])) + ',belongs_to,' + str(family.get(row[4])))
        # lista.append(str(common.get(row[6])) + ',name,' + row[6])
        # lista.append(str(common.get(row[6])) + ',type,7')
        # lista.append(str(common.get(row[6])) + ',belongs_to,' + str(species.get(row[5])))
        # lista.append(str(state.get(row[7])) + ',name,' + row[7])
        # lista.append(str(state.get(row[7])) + ',type,8')
        # lista.append(str(state.get(row[7])) + ',belongs_to,' + str(common.get(row[6])))

doc.close()

fp = open("triples-data.csv", "w")

for ele in lista:
    fp.write(ele + '\n')

fp.close()