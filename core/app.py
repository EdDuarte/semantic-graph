from grafo import Grafo
from rules import *
import os.path
import webbrowser

class App:
    def __init__(self):
        self.grafo = Grafo()

    def load_data(self, filename):
        self.grafo.load(filename)

    def save_data(self, filename):
        self.grafo.save(filename)

    def set_inference(self, rule):
        self.grafo.apply_inference(rule)

    def search(self, subject, predicate, obj):
        result = self.grafo.triples(subject, predicate, obj)
        self.grafo.create_graph(result)
        webbrowser.open('file://' + os.path.realpath("graph.png"))
        return result


def getMainMenu():
    return (
        '1 - Load data\n'
        '2 - Save data"\n'
        '3 - Apply Inference Rule "specie belongs to class"\n'
        '4 - Apply Inference Rule "specie belongs to order"\n'
        '5 - Apply Inference Rule "family belongs to class"\n'
        '6 - Search & show graph\n'
        '0 - Exit'
    )

def isBlank(s):
    if s and s.strip():
        return False
    return True

app = App()
option = -1

while True:
    print(getMainMenu())
    try:
        option = input("Select your option: ")
    except KeyboardInterrupt:
        print("\nExiting application...")

    if isBlank(option):
        print("ERROR: Option is empty! Please choose an option...")

    else:
        try:
            intOption = int(option)
            if intOption == 1:
                fileName = input("File name (deixar vazio para utilizar"
                                 " o ficheiro 'taxon.csv'): ")
                if isBlank(fileName):
                    fileName = 'taxon.csv'

                fileName = os.path.realpath(fileName)
                print("Attempting to load " + fileName)
                if os.path.isfile(fileName):
                    app.load_data(fileName)
                else:
                    print("ERROR: File does not exist! Try again!")

            elif intOption == 2:
                fileName = input(
                    "File name of output: ")

                if isBlank(fileName):
                    print('ERROR: Must not be empty! Try again!')
                else:
                    fileName = os.path.realpath(fileName)
                    app.save_data(fileName)

            elif intOption == 3:
                app.set_inference(ClassInSpecieRule())

            elif intOption == 4:
                app.set_inference(OrderInSpecieRule())

            elif intOption == 5:
                app.set_inference(ClassInFamilyRule())

            elif intOption == 6:
                subject = input("Subject: ")
                if isBlank(subject):
                    subject = None

                predicate = input("Predicate: ")
                if isBlank(predicate):
                    predicate = None

                obj = input("Object: ")
                if isBlank(obj):
                    obj = None

                print(app.search(subject, predicate, obj))

            elif intOption == 0:
                break

            else:
                print("ERROR: Must be a number between 0 and 6")

        except ValueError:
            print("ERROR: Must be a number between 0 and 6")

