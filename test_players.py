# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import argparse

parser = argparse.ArgumentParser()

### creates arguments to make use of in functions
parser.add_argument('season_id', help='Set the season (e.g. 20182019)')
parser.add_argument('game_id', help='Set the game (e.g. 20001)')

parser.add_argument('--players', dest='players', help='Can set to true', required=False)
parser.add_argument('--players_stats', dest='players_stats', help='Can set to true, period, situation, opponents or teammates', required=False)
parser.add_argument('--players_charts', dest='players_charts', help='Can set to true, gamescore or shots', required=False)

parser.add_argument('--images', dest='images', help='Setting to show will display images as they are generated', required=False)
parser.add_argument('--load_pbp', dest='load_pbp', help='Setting to true will load a stored play-by-play file', required=False)

args = parser.parse_args()


###
### PLAYERS
###

#
# Stats
#

if args.players == 'true' or args.players_stats == 'true' or args.players_stats == 'basic':
    import stats_players
    stats_players.parse_ids(args.season_id, args.game_id)
    stats_players

if args.players == 'true' or args.players_stats == 'true' or args.players_stats == 'period':
    import stats_players_period
    stats_players_period.parse_ids(args.season_id, args.game_id)
    stats_players_period

if args.players == 'true' or args.players_stats == 'true' or args.players_stats == 'situation':
    import stats_players_situation
    stats_players_situation.parse_ids(args.season_id, args.game_id)
    stats_players_situation

if args.players == 'true' or args.players_stats == 'true' or args.players_stats == 'opponents':
    import stats_players_opponents
    stats_players_opponents.parse_ids(args.season_id, args.game_id)
    stats_players_opponents

if args.players == 'true' or args.players_stats == 'true' or args.players_stats == 'teammates':
    import stats_players_teammates
    stats_players_teammates.parse_ids(args.season_id, args.game_id)
    stats_players_teammates

#
# Charts
#

if args.players == 'true' or args.players_charts == 'true' or args.players_charts == 'gamescore':    
    import chart_players_gamescore
    chart_players_gamescore.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_gamescore
    
if args.players == 'true' or args.players_charts == 'true' or args.players_charts == 'i_shots':    
    import chart_players_individual_shots
    chart_players_individual_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_shots

if args.players == 'true' or args.players_charts == 'true' or args.players_charts == 'i_xg':    
    import chart_players_individual_xg
    chart_players_individual_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_xg

if args.players == 'true' or args.players_charts == 'true' or args.players_charts == 'on_shots':    
    import chart_players_onice_shots
    chart_players_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_shots

if args.players == 'true' or args.players_charts == 'true' or args.players_charts == 'on_xg':    
    import chart_players_onice_xg
    chart_players_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_xg