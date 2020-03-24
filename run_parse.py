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

parser.add_argument('--rosters', dest='rosters', help='Can set to true', required=False)
parser.add_argument('--shifts', dest='shifts', help='Can set to true', required=False)
parser.add_argument('--pbp', dest='pbp', help='Can set to true', required=False)
parser.add_argument('--toi', dest='toi', help='Can set to true', required=False)
parser.add_argument('--merge_pbp', dest='merge_pbp', help='Can set to true', required=False)
parser.add_argument('--xg', dest='xg', help='Can set to true', required=False)

# for use with the 20062007 season only
parser.add_argument('--load_pbp', dest='load_pbp', help='Setting to true will load a stored play-by-play file', required=False)

# for instances where players are recorded in the lineup at one position but actually playing another (e.g. Luke Witkowski listed as a D while playing F)
parser.add_argument('--switch_F2D', dest='switch_F2D', help='Set to player name (e.g. Luke_Witkowski)', required=False)
parser.add_argument('--switch_D2F', dest='switch_D2F', help='Set to player name (e.g. Luke_Witkowski)', required=False)

args = parser.parse_args()


###
### PARSE FILES
###

if args.rosters == 'true' or args.rosters is None and args.shifts is None and args.pbp is None and args.toi is None and args.merge_pbp is None and args.xg is None:    
    import files_parse_rosters
    files_parse_rosters.parse_ids(args.season_id, args.game_id, args.switch_F2D, args.switch_D2F)
    files_parse_rosters

if args.shifts == 'true' or args.rosters is None and args.shifts is None and args.pbp is None and args.toi is None and args.merge_pbp is None and args.xg is None:       
    import files_parse_shifts
    files_parse_shifts.parse_ids(args.season_id, args.game_id)
    files_parse_shifts

if args.pbp == 'true' or args.rosters is None and args.shifts is None and args.pbp is None and args.toi is None and args.merge_pbp is None and args.xg is None:    
    import files_parse_pbp
    files_parse_pbp.parse_ids(args.season_id, args.game_id, args.load_pbp)
    files_parse_pbp

if args.toi == 'true' or args.rosters is None and args.shifts is None and args.pbp is None and args.toi is None and args.merge_pbp is None and args.xg is None:    
    import files_parse_toi
    files_parse_toi.parse_ids(args.season_id, args.game_id, args.load_pbp)
    files_parse_toi

if args.merge_pbp == 'true' or args.rosters is None and args.shifts is None and args.pbp is None and args.toi is None and args.merge_pbp is None and args.xg is None: 
    import files_parse_merge_pbp
    files_parse_merge_pbp.parse_ids(args.season_id, args.game_id, args.load_pbp)
    files_parse_merge_pbp

if args.xg == 'true' or args.rosters is None and args.shifts is None and args.pbp is None and args.toi is None and args.merge_pbp is None and args.xg is None: 
    import files_parse_xg
    files_parse_xg.parse_ids(args.season_id, args.game_id)
    files_parse_xg