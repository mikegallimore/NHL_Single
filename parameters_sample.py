# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 20:40:14 2017

@author: @mikegallimore
"""
import os
  
### set subfolder paths; check to see if they already exist and, if they don't, create them
files_root = '/yourpath/Files/'
charts_root = '/yourpath/Charts/'

charts_players = charts_root + 'Players/'

charts_teams = charts_root + 'Teams/'
charts_teams_period = charts_teams + 'Period/'
charts_teams_situation = charts_teams + 'Situation/'

charts_units = charts_root + 'Units/'

if not os.path.exists(files_root):
    os.makedirs(files_root)
    print('Created subfolder ' + files_root)  
if not os.path.exists(charts_root):
    os.makedirs(charts_root)
    print('Created subfolder ' + charts_root)

if not os.path.exists(charts_players):
    os.makedirs(charts_players)
    print('Created subfolder ' + charts_players)

if not os.path.exists(charts_players):
    os.makedirs(charts_players)
    print('Created subfolder ' + charts_players)

if not os.path.exists(charts_teams):
    os.makedirs(charts_teams)
    print('Created subfolder ' + charts_teams)
if not os.path.exists(charts_teams_period):
    os.makedirs(charts_teams_period)
    print('Created subfolder ' + charts_teams_period)
if not os.path.exists(charts_teams_situation):
    os.makedirs(charts_teams_situation)
    print('Created subfolder ' + charts_teams_situation)

if not os.path.exists(charts_units):
    os.makedirs(charts_units)
    print('Created subfolder ' + charts_units)