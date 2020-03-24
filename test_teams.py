# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import argparse

parser = argparse.ArgumentParser()

### creates arguments to make use of in functions
parser.add_argument('season_id', help='Set the season (e.g. 20182019)')
parser.add_argument('game_id', help='Set the game (e.g. 20001)')

parser.add_argument('--teams', dest='teams', help='Can set to true', required=False)
parser.add_argument('--teams_stats', dest='teams_stats', help='Can set to true, period or situation', required=False)
parser.add_argument('--teams_charts', dest='teams_charts', help='Can set to true, gameflow, scatter, scatter_period or scatter_situation', required=False)

parser.add_argument('--images', dest='images', help='Setting to show will display images as they are generated', required=False)
parser.add_argument('--load_pbp', dest='load_pbp', help='Setting to true will load a stored play-by-play file', required=False)

args = parser.parse_args()


###
### TEAMS
###

#
# Stats
#

if args.teams == 'true' or args.teams_stats == 'true' or args.teams_stats == 'basic':    
    import stats_teams
    stats_teams.parse_ids(args.season_id, args.game_id)
    stats_teams

if args.teams == 'true' or args.teams_stats == 'true' or args.teams_stats == 'period':    
    import stats_teams_period
    stats_teams_period.parse_ids(args.season_id, args.game_id)
    stats_teams_period

if args.teams == 'true' or args.teams_stats == 'true' or args.teams_stats == 'situation':    
    import stats_teams_situation
    stats_teams_situation.parse_ids(args.season_id, args.game_id)
    stats_teams_situation

#
# Charts
#
    
if args.teams == 'true' or args.teams_charts == 'true' or args.teams_charts == 'summary':    
    import chart_teams_summary
    chart_teams_summary.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_summary

if args.teams == 'true' or args.teams_charts == 'true' or args.teams_charts == 'gameflow_shots':    
    import chart_teams_gameflow_shots
    chart_teams_gameflow_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_gameflow_shots

if args.teams == 'true' or args.teams_charts == 'true' or args.teams_charts == 'gameflow_xg':    
    import chart_teams_gameflow_xg
    chart_teams_gameflow_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_gameflow_xg

if args.teams == 'true' or args.teams_charts == 'true' or args.teams_charts == 'scatter':    
    import chart_teams_shots_scatter
    chart_teams_shots_scatter.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_scatter

if args.teams == 'true' or args.teams_charts == 'true' or args.teams_charts == 'scatter_period':    
    import chart_teams_shots_scatter_period
    chart_teams_shots_scatter_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_scatter_period

if args.teams == 'true' or args.teams_charts == 'true' or args.teams_charts == 'scatter_situation':    
    import chart_teams_shots_scatter_situation
    chart_teams_shots_scatter_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_scatter_situation

if args.teams == 'true' or args.teams_charts == 'true' or args.teams_charts == 'density':    
    import chart_teams_shots_density
    chart_teams_shots_density.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_density