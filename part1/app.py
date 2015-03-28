#!/usr/bin/python
# -*- coding: utf-8 -*-

from core import Core
from rules import *


system = Core()
# Define the source file
system.setDataFilename('taxon.csv')

option = -1

while 1:
    print (system.getMainMenu())
    option = input("Option: ")
    if(int(option) == 1):
        # Load data into simplegraph system
        system.loadData()
    elif(int(option) == 2):
        system.setInference(ClassInSpecieRule())
    elif(int(option) == 3):
        system.setInference(OrderInSpecieRule())
    elif(int(option) == 4):
        system.setInference(ClassInFamilyRule())
    elif(int(option) == 5):
        print (system.getInferencedData('belongs_to_class'))
    elif(int(option) == 0):
        break
