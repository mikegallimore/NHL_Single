# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import argparse

parser = argparse.ArgumentParser()

### creates arguments to make use of in functions
parser.add_argument('season_id', help='Set the season (e.g. 20182019)')
parser.add_argument('game_id', help='Set the game (e.g. 20001)')

parser.add_argument('--fetch', dest='fetch', help='Can set to true', required=False)

parser.add_argument('--flush', dest='flush', help='Setting to true will remove all non-schedule files', required=False)

args = parser.parse_args()


###
### FLUSH FILES
###

if args.flush == 'true':
    import flush_charts
    import flush_files
    flush_charts
    flush_files


###
### FETCH FILES
###

if args.fetch == 'true':
    import files_fetch
    files_fetch.parse_ids(args.season_id, args.game_id)
    files_fetch