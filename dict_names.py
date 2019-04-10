# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 00:10:44 2017

@author: @mikegallimore
"""
import csv

NAMES = {}

with open('dict_names.csv', 'r') as Roster_List:
        Roster_Reader = list(csv.reader(Roster_List))
        for row in Roster_Reader:
            NAMES[row[0]] = row[1]