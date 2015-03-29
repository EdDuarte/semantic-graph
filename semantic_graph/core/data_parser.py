import csv

doc = open("Dados.csv", "r")
reader = csv.reader(doc)

iterator = 0
data = list()

backup = reader
iterator = 0

for line in reader:
    if iterator == 0:
        data.append (str(iterator) + ',name,' + line[int(iterator)])
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator)])
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator)])
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator)])
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator)])
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator)])
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator)])
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator)])
        iterator += 1
    elif iterator > 7:
        data.append  (str(iterator) + ',name,' + line[int(iterator%8)])
        data.append  (str(iterator) + ',type,' + str(iterator%8))
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator%8)])
        data.append  (str(iterator) + ',type,' + str(iterator%8))
        data.append  (str(iterator) + ',belongs_to,' + str(iterator-1))
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator%8)])
        data.append  (str(iterator) + ',type,' + str(iterator%8))
        data.append  (str(iterator) + ',belongs_to,' + str(iterator-1))
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator%8)])
        data.append  (str(iterator) + ',type,' + str(iterator%8))
        data.append  (str(iterator) + ',belongs_to,' + str(iterator-1))
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator%8)])
        data.append  (str(iterator) + ',type,' + str(iterator%8))
        data.append  (str(iterator) + ',belongs_to,' + str(iterator-1))
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator%8)])
        data.append  (str(iterator) + ',type,' + str(iterator%8))
        data.append  (str(iterator) + ',belongs_to,' + str(iterator-1))
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator%8)])
        data.append  (str(iterator) + ',type,' + str(iterator%8))
        data.append  (str(iterator) + ',belongs_to,' + str(iterator-1))
        iterator += 1
        data.append  (str(iterator) + ',name,' + line[int(iterator%8)])
        data.append  (str(iterator) + ',type,' + str(iterator%8))
        data.append  (str(iterator) + ',belongs_to,' + str(iterator-1))
        iterator += 1

doc.close()


doc = open("triples.csv", "w")
for line in data:
    doc.write(str(line)+'\n')
doc.close()