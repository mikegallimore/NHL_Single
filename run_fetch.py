# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import argparse

parser = argparse.ArgumentParser()


###
### COMMAND LINE ARGUMENTS
###

parser.add_argument('season_id', help='Set the season (e.g. 20182019)')
parser.add_argument('game_id', help='Set the game (e.g. 20001)')

parser.add_argument('--fetch', dest='fetch', help='Can set to true', required=False)


args = parser.parse_args()


###
### FETCH FILES
###

import files_fetch
files_fetch.parse_ids(args.season_id, args.game_id)
files_fetch