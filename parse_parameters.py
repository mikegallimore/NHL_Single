# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 20:40:14 2017

@author: @mikegallimore
"""
import parameters
import argparse

parser = argparse.ArgumentParser()

### creates arguments to make use of in functions
parser.add_argument("--season_id", dest="season_id", required=False)
parser.add_argument("--game_id", dest="game_id", required=False)

args = parser.parse_args()

### passes the arguments through to parameters.py
parameters.parse_parameters(args.season_id, args.game_id)