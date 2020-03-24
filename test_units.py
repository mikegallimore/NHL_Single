# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import argparse

parser = argparse.ArgumentParser()

### creates arguments to make use of in functions
parser.add_argument('season_id', help='Set the season (e.g. 20182019)')
parser.add_argument('game_id', help='Set the game (e.g. 20001)')

parser.add_argument('--units', dest='units', help='Can set to true', required=False)
parser.add_argument('--units_stats', dest='units_stats', help='Can set to true', required=False)
parser.add_argument('--units_stats_lines', dest='units_stats_lines', help='Can set to true, matchups, matchups_lines, matchups_pairings or teammates', required=False)
parser.add_argument('--units_stats_pairings', dest='units_stats_pairings', help='Can set to true, matchups, matchups_lines, matchups_pairings or teammates', required=False)
parser.add_argument('--units_stats_pk', dest='units_stats_pk', help='Can set to true', required=False)
parser.add_argument('--units_stats_pp', dest='units_stats_pp', help='Can set to true', required=False)
parser.add_argument('--units_charts', dest='units_charts', help='Can set to true or combined', required=False)
parser.add_argument('--units_charts_lines', dest='units_charts_lines', help='Can set to true, matchups, matchups_lines, matchups_lines_shots, matchups_pairings, matchups_pairings_shots, teammates or teammates_shots', required=False)
parser.add_argument('--units_charts_pairings', dest='units_charts_pairings', help='Can set to true, matchups, matchups_lines, matchups_lines_shots, matchups_pairings, matchups_pairings_shots, teammates or teammates_shots', required=False)
parser.add_argument('--units_charts_pk', dest='units_charts_pk', help='Can set to true', required=False)
parser.add_argument('--units_charts_pp', dest='units_charts_pp', help='Can set to true', required=False)

parser.add_argument('--images', dest='images', help='Setting to show will display images as they are generated', required=False)
parser.add_argument('--load_pbp', dest='load_pbp', help='Setting to true will load a stored play-by-play file', required=False)

args = parser.parse_args()


###
### UNITS
###

#
# Stats
#

# Lines
if args.units == 'true' or args.units_stats == 'true' or args.units_stats_lines == 'true' or args.units_stats_lines == 'basic':
    import stats_units_lines
    stats_units_lines.parse_ids(args.season_id, args.game_id)
    stats_units_lines

if args.units == 'true' or args.units_stats == 'true' or args.units_stats_lines == 'true' or args.units_stats_lines == 'matchups' or args.units_stats_lines == 'matchups_lines':
    import stats_units_lines_matchups_lines
    stats_units_lines_matchups_lines.parse_ids(args.season_id, args.game_id)
    stats_units_lines_matchups_lines

if args.units == 'true' or args.units_stats == 'true' or args.units_stats_lines == 'true' or args.units_stats_lines == 'matchups' or args.units_stats_lines == 'matchups_pairings':    
    import stats_units_lines_matchups_pairings
    stats_units_lines_matchups_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_lines_matchups_pairings

if args.units == 'true' or args.units_stats == 'true' or args.units_stats_lines == 'true' or args.units_stats_lines == 'teammates':        
    import stats_units_lines_teammates_pairings
    stats_units_lines_teammates_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_lines_teammates_pairings

# Pairings
if args.units == 'true' or args.units_stats == 'true' or args.units_stats_pairings == 'true' or args.units_stats_pairings == 'basic':
    import stats_units_pairings
    stats_units_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_pairings

if args.units == 'true' or args.units_stats == 'true' or args.units_stats_pairings == 'true' or args.units_stats_pairings == 'matchups' or args.units_stats_pairings == 'matchups_lines':
    import stats_units_pairings_matchups_lines
    stats_units_pairings_matchups_lines.parse_ids(args.season_id, args.game_id)
    stats_units_pairings_matchups_lines

if args.units == 'true' or args.units_stats == 'true' or args.units_stats_pairings == 'true' or args.units_stats_pairings == 'matchups' or args.units_stats_pairings == 'matchups_pairings':    
    import stats_units_pairings_matchups_pairings
    stats_units_pairings_matchups_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_pairings_matchups_pairings

if args.units == 'true' or args.units_stats == 'true' or args.units_stats_pairings == 'true' or args.units_stats_pairings == 'teammates':
    import stats_units_pairings_teammates_lines
    stats_units_pairings_teammates_lines.parse_ids(args.season_id, args.game_id)
    stats_units_pairings_teammates_lines

# PP
if args.units == 'true' or args.units_stats_pp == 'true':
    import stats_units_pp
    stats_units_pp.parse_ids(args.season_id, args.game_id)
    stats_units_pp

# PK
if args.units == 'true' or args.units_stats_pk == 'true':
    import stats_units_pk
    stats_units_pk.parse_ids(args.season_id, args.game_id)
    stats_units_pk

#
# Charts
#

if args.units == 'true' or args.units_charts == 'true' or args.units == 'chart_shots' or args.units_charts == 'shots':
    import chart_units_onice_shots
    chart_units_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_onice_shots
if args.units == 'true' or args.units_charts == 'true' or args.units == 'chart_xg' or args.units_charts == 'xg':
    import chart_units_onice_xg
    chart_units_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_onice_xg

# Lines
if args.units == 'true' or args.units_charts == 'true' or args.units_charts_lines == 'true' or args.units_charts_lines == 'shots':    
    import chart_units_lines_onice_shots
    chart_units_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_onice_shots

if args.units == 'true' or args.units_charts == 'true' or args.units_charts_lines == 'true' or args.units_charts_lines == 'xg':    
    import chart_units_lines_onice_xg
    chart_units_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_onice_xg

if args.units == 'true' or args.units_charts == 'true' or args.units_charts_lines == 'true' or args.units_charts_lines == 'matchups' or args.units_charts_lines == 'matchups_lines' or args.units_charts_lines == 'matchups_lines_shots':
    import chart_units_lines_matchups_lines_onice_shots
    chart_units_lines_matchups_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_lines_onice_shots

if args.units == 'true' or args.units_charts == 'true' or args.units_charts_lines == 'true' or args.units_charts_lines == 'matchups' or args.units_charts_lines == 'matchups_lines' or args.units_charts_lines == 'matchups_lines_xg':
    import chart_units_lines_matchups_lines_onice_xg
    chart_units_lines_matchups_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_lines_onice_xg
 
if args.units == 'true' or args.units_charts == 'true' or args.units_charts_lines == 'true' or args.units_charts_lines == 'matchups' or args.units_charts_lines == 'matchups_pairings' or args.units_charts_lines == 'matchups_pairings_shots':
    import chart_units_lines_matchups_pairings_onice_shots
    chart_units_lines_matchups_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_pairings_onice_shots

if args.units == 'true' or args.units_charts == 'true' or args.units_charts_lines == 'true' or args.units_charts_lines == 'matchups' or args.units_charts_lines == 'matchups_pairings' or args.units_charts_lines == 'matchups_pairings_xg':
    import chart_units_lines_matchups_pairings_onice_xg
    chart_units_lines_matchups_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_pairings_onice_xg

if args.units == 'true' or args.units_charts == 'true' or args.units_charts_lines == 'true' or args.units_charts_lines == 'teammates' or args.units_charts_lines == 'teammates_shots':
    import chart_units_lines_teammates_pairings_onice_shots
    chart_units_lines_teammates_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_teammates_pairings_onice_shots

if args.units == 'true' or args.units_charts == 'true' or args.units_charts_lines == 'true' or args.units_charts_lines == 'teammates' or args.units_charts_lines == 'teammates_xg':
    import chart_units_lines_teammates_pairings_onice_xg
    chart_units_lines_teammates_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_teammates_pairings_onice_xg

# Pairings
if args.units == 'true' or args.units_charts == 'true' or args.units_charts_pairings == 'true' or args.units_charts_pairings == 'shots':
    import chart_units_pairings_onice_shots
    chart_units_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_onice_shots
    
if args.units == 'true' or args.units_charts == 'true' or args.units_charts_pairings == 'true' or args.units_charts_pairings == 'xg':
    import chart_units_pairings_onice_xg
    chart_units_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_onice_xg

if args.units == 'true' or args.units_charts == 'true' or args.units_charts_pairings == 'true' or args.units_charts_pairings == 'matchups' or args.units_charts_pairings == 'matchups_lines' or args.units == 'matchups_lines_shots':
    import chart_units_pairings_matchups_lines_onice_shots
    chart_units_pairings_matchups_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_lines_onice_shots

if args.units == 'true' or args.units_charts == 'true' or args.units_charts_pairings == 'true' or args.units_charts_pairings == 'matchups' or args.units_charts_pairings == 'matchups_lines' or args.units == 'matchups_lines_xg':
    import chart_units_pairings_matchups_lines_onice_xg
    chart_units_pairings_matchups_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_lines_onice_xg

if args.units == 'true' or args.units_charts == 'true' or args.units_charts_pairings == 'true' or args.units_charts_pairings == 'matchups' or args.units_charts_pairings == 'matchups_pairings' or args.units == 'matchups_pairings_shots':    
    import chart_units_pairings_matchups_pairings_onice_shots
    chart_units_pairings_matchups_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_pairings_onice_shots
    
if args.units == 'true' or args.units_charts == 'true' or args.units_charts_pairings == 'true' or args.units_charts_pairings == 'matchups' or args.units_charts_pairings == 'matchups_pairings' or args.units == 'matchups_pairings_xg':    
    import chart_units_pairings_matchups_pairings_onice_xg
    chart_units_pairings_matchups_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_pairings_onice_xg

if args.units == 'true' or args.units_charts == 'true' or args.units_charts_pairings == 'true' or args.units_charts_pairings == 'teammates' or args.units_charts_pairings == 'teammates_shots':
    import chart_units_pairings_teammates_lines_onice_shots
    chart_units_pairings_teammates_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_teammates_lines_onice_shots

if args.units == 'true' or args.units_charts == 'true' or args.units_charts_pairings == 'true' or args.units_charts_pairings == 'teammates' or args.units_charts_pairings == 'teammates_xg':
    import chart_units_pairings_teammates_lines_onice_xg
    chart_units_pairings_teammates_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_teammates_lines_onice_xg