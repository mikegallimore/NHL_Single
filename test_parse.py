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

parser.add_argument('--parse', dest='parse', help='Can set to true, rosters, shifts, pbp, toi, merge_pbp or xg', required=False)

parser.add_argument('--load_pbp', dest='load_pbp', help='Setting to true will load a stored play-by-play file', required=False)

args = parser.parse_args()


###
### PARSE FILES
###

if args.parse == 'true' or args.parse == 'rosters':    
    import files_parse_rosters
    files_parse_rosters.parse_ids(args.season_id, args.game_id)
    files_parse_rosters

if args.parse == 'true' or args.parse == 'shifts':       
    import files_parse_shifts
    files_parse_shifts.parse_ids(args.season_id, args.game_id)
    files_parse_shifts

if args.parse == 'true' or args.parse == 'pbp':    
    import files_parse_pbp
    files_parse_pbp.parse_ids(args.season_id, args.game_id, args.load_pbp)
    files_parse_pbp

if args.parse == 'true' or args.parse == 'toi':    
    import files_parse_TOI
    files_parse_TOI.parse_ids(args.season_id, args.game_id, args.load_pbp)
    files_parse_TOI

if args.parse == 'true' or args.parse == 'merge_pbp': 
    import files_parse_merge_pbp
    files_parse_merge_pbp.parse_ids(args.season_id, args.game_id, args.load_pbp)
    files_parse_merge_pbp

if args.parse == 'true' or args.parse == 'xg': 
    import files_parse_xg
    files_parse_xg.parse_ids(args.season_id, args.game_id)
    files_parse_xg