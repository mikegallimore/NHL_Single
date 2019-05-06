# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import os
import glob
from pathlib import Path
import parameters

### pull common variables from the parameters file
charts_root = parameters.charts_root

charts_players = parameters.charts_players

charts_teams = parameters.charts_teams
charts_teams_period = parameters.charts_teams_period
charts_teams_situation = parameters.charts_teams_situation

charts_units = parameters.charts_units

### make paths
players_path = Path(charts_players)

teams_path = Path(charts_teams)
teams_period_path = Path(charts_teams_period)
teams_situation_path = Path(charts_teams_situation)
teams_path = Path(charts_teams)

units_path = Path(charts_units)

### create lists of images in each charts folder
players_list = players_path.glob('*.PNG')

teams_list = teams_path.glob('*.PNG')
teams_period_list = teams_period_path.glob('*.PNG')
teams_situation_list = teams_situation_path.glob('*.PNG')

units_list = units_path.glob('*.PNG')

### iterate over each list in order to remove all images
for i in players_list:
    try:
        os.remove(i)
    except:
        print('Error while deleting file : ', i)

for i in teams_list:
    try:
        os.remove(i)

    except:
        print('Error while deleting file : ', i)

for i in teams_period_list:
    try:
        os.remove(i)
    except:
        print('Error while deleting file : ', i)

for i in teams_situation_list:
    try:
        os.remove(i)
    except:
        print('Error while deleting file : ', i)

for i in units_list:
    try:
        os.remove(i)
    except:
        print('Error while deleting file : ', i)

print('Flushed any preexisting charts.')