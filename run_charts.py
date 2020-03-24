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

parser.add_argument('--units_lines', dest='units_lines', help='Can set to true, matchups, matchups_lines, matchups_lines_shots, matchups_pairings, matchups_pairings_shots, teammates or teammates_shots', required=False)
parser.add_argument('--units_pairings', dest='units_pairings', help='Can set to true, matchups, matchups_lines, matchups_lines_shots, matchups_pairings, matchups_pairings_shots, teammates or teammates_shots', required=False)

parser.add_argument('--focus', dest='focus', help='Can set to [teams, players, units, lines, pairings, pp, pk]', required=False)
parser.add_argument('--type', dest='type', help='Can set to [summary, gameflow, gameflow_shots, gameflow_xg, scatter, density] for teams, [gamescore, i, i_shots, i_xg, on, on_shots, on_xg] for players, [i, i_shots, i_xg, on, on_shots, on_xg] for units', required=False)
parser.add_argument('--detail', dest='detail', help='Can set to [period, situation] for teams, [matchups, matchups_lines, matchups_pairings, teammates] for units', required=False)

parser.add_argument('--images', dest='images', help='Setting to show will display images as they are generated', required=False)

args = parser.parse_args()


###
### TEAM CHARTS
###

if args.focus == 'teams' and args.type is None or args.focus == 'teams' and args.type == 'gameflow' or args.focus == 'teams' and args.type == 'gameflow_shots':    
    import chart_teams_gameflow_shots
    chart_teams_gameflow_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_gameflow_shots

if args.focus == 'teams' and args.type is None or args.focus == 'teams' and args.type == 'gameflow' or args.focus == 'teams' and args.type == 'gameflow_xg':    
    import chart_teams_gameflow_xg
    chart_teams_gameflow_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_gameflow_xg

if args.focus == 'teams' and args.type is None and args.detail is None or args.focus == 'teams' and args.type == 'scatter' and args.detail is None:    
    import chart_teams_shots_scatter
    chart_teams_shots_scatter.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_scatter

if args.focus == 'teams' and args.type is None and args.detail is None or args.focus == 'teams' and args.type == 'scatter' and args.detail is None or args.focus == 'teams' and args.type is None and args.detail == 'period'  or args.focus == 'teams' and args.type == 'scatter' and args.detail == 'period':    
    import chart_teams_shots_scatter_period
    chart_teams_shots_scatter_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_scatter_period

if args.focus == 'teams' and args.type is None and args.detail is None or args.focus == 'teams' and args.type == 'scatter' and args.detail is None or args.focus == 'teams' and args.type is None and args.detail == 'situation'  or args.focus == 'teams' and args.type == 'scatter' and args.detail == 'situation':
    import chart_teams_shots_scatter_situation
    chart_teams_shots_scatter_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_scatter_situation

if args.focus == 'teams' and args.type is None and args.detail is None or args.focus == 'teams' and args.type == 'density' and args.detail is None:    
    import chart_teams_shots_density
    chart_teams_shots_density.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_density

if args.focus == 'teams' and args.type is None and args.detail is None or args.focus == 'teams' and args.type == 'density' and args.detail is None or args.focus == 'teams' and args.type is None and args.detail == 'period' or args.focus == 'teams' and args.type == 'density' and args.detail == 'period':    
    import chart_teams_shots_density_period
    chart_teams_shots_density_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_density_period

if args.focus == 'teams' and args.type is None and args.detail is None or args.focus == 'teams' and args.type == 'density' and args.detail is None or args.focus == 'teams' and args.type is None and args.detail == 'situation' or args.focus == 'teams' and args.type == 'density' and args.detail == 'situation':
    import chart_teams_shots_density_situation
    chart_teams_shots_density_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_density_situation


###
### PLAYER CHARTS
###

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'basic' or args.focus == 'players' and args.type == 'gamescore' and args.detail is None or args.focus == 'players' and args.type == 'gamescore' and args.detail == 'basic':    
    import chart_players_gamescore
    chart_players_gamescore.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_gamescore

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type == 'gamescore' and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'period' or args.focus == 'players' and args.type =='gamescore' and args.detail == 'period':    
    import chart_players_gamescore_period
    chart_players_gamescore_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_gamescore_period

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type == 'gamescore' and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'situation' or args.focus == 'players' and args.type =='gamescore' and args.detail == 'situation':    
    import chart_players_gamescore_situation
    chart_players_gamescore_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_gamescore_situation

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'basic' or args.focus == 'players' and args.type == 'i' and args.detail is None or args.focus == 'players' and args.type == 'i' and args.detail == 'basic' or args.focus == 'players' and args.type == 'shots' and args.detail is None or args.focus == 'players' and args.type == 'shots' and args.detail == 'basic' or args.focus == 'players' and args.type == 'i_shots' and args.detail is None or args.focus == 'players' and args.type == 'i_shots' and args.detail == 'basic':    
    import chart_players_individual_shots
    chart_players_individual_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_shots

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type == 'i' and args.detail is None or args.focus == 'players' and args.type == 'shots' and args.detail is None or args.focus == 'players' and args.type == 'i_shots' and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'period' or args.focus == 'players' and args.type =='i_shots' and args.detail == 'period':    
    import chart_players_individual_shots_period
    chart_players_individual_shots_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_shots_period

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type == 'i' and args.detail is None or args.focus == 'players' and args.type == 'shots' and args.detail is None or args.focus == 'players' and args.type == 'i_shots' and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'situation' or args.focus == 'players' and args.type =='i_shots' and args.detail == 'situation':    
    import chart_players_individual_shots_situation
    chart_players_individual_shots_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_shots_situation

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'basic' or args.focus == 'players' and args.type == 'i' and args.detail is None or args.focus == 'players' and args.type == 'i' and args.detail == 'basic' or args.focus == 'players' and args.type == 'xg' and args.detail is None or args.focus == 'players' and args.type == 'xg' and args.detail == 'basic' or args.focus == 'players' and args.type == 'i_xg' and args.detail is None or args.focus == 'players' and args.type == 'i_xg' and args.detail == 'basic':    
    import chart_players_individual_xg
    chart_players_individual_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_xg

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type == 'i' and args.detail is None or args.focus == 'players' and args.type == 'xg' and args.detail is None or args.focus == 'players' and args.type == 'i_xg' and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'period' or args.focus == 'players' and args.type =='i_xg' and args.detail == 'period':    
    import chart_players_individual_xg_period
    chart_players_individual_xg_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_xg_period

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type == 'i' and args.detail is None or args.focus == 'players' and args.type == 'xg' and args.detail is None or args.focus == 'players' and args.type == 'i_xg' and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'situation' or args.focus == 'players' and args.type =='i_xg' and args.detail == 'situation':    
    import chart_players_individual_xg_situation
    chart_players_individual_xg_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_xg_situation

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'basic' or args.focus == 'players' and args.type == 'on' and args.detail is None or args.focus == 'players' and args.type == 'on' and args.detail == 'basic' or args.focus == 'players' and args.type == 'shots' and args.detail is None or args.focus == 'players' and args.type == 'shots' and args.detail == 'basic' or args.focus == 'players' and args.type == 'on_shots' and args.detail is None or args.focus == 'players' and args.type == 'on_shots' and args.detail == 'basic':    
    import chart_players_onice_shots
    chart_players_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_shots

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type == 'on' and args.detail is None or args.focus == 'players' and args.type == 'shots' and args.detail is None or args.focus == 'players' and args.type == 'on_shots' and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'period' or args.focus == 'players' and args.type =='on' and args.detail == 'period' or args.focus == 'players' and args.type =='shots' and args.detail == 'period' or args.focus == 'players' and args.type =='on_shots' and args.detail == 'period':    
    import chart_players_onice_shots_period
    chart_players_onice_shots_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_shots_period

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type == 'on' and args.detail is None or args.focus == 'players' and args.type == 'shots' and args.detail is None or args.focus == 'players' and args.type == 'on_shots' and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'situation' or args.focus == 'players' and args.type =='on' and args.detail == 'situation' or args.focus == 'players' and args.type =='shots' and args.detail == 'situation' or args.focus == 'players' and args.type =='on_shots' and args.detail == 'situation':    
    import chart_players_onice_shots_situation
    chart_players_onice_shots_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_shots_situation

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'basic' or args.focus == 'players' and args.type == 'on' and args.detail is None or args.focus == 'players' and args.type == 'on' and args.detail == 'basic' or args.focus == 'players' and args.type == 'xg' and args.detail is None or args.focus == 'players' and args.type == 'xg' and args.detail == 'basic' or args.focus == 'players' and args.type == 'on_xg' and args.detail is None or args.focus == 'players' and args.type == 'on_xg' and args.detail == 'basic':    
    import chart_players_onice_xg
    chart_players_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_xg

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type == 'on' and args.detail is None or args.focus == 'players' and args.type == 'xg' and args.detail is None or args.focus == 'players' and args.type == 'on_xg' and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'period' or args.focus == 'players' and args.type =='on' and args.detail == 'period' or args.focus == 'players' and args.type =='xg' and args.detail == 'period' or args.focus == 'players' and args.type =='on_xg' and args.detail == 'period':    
    import chart_players_onice_xg_period
    chart_players_onice_xg_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_xg_period

if args.focus == 'players' and args.type is None and args.detail is None or args.focus == 'players' and args.type == 'on' and args.detail is None or args.focus == 'players' and args.type == 'xg' and args.detail is None or args.focus == 'players' and args.type == 'on_xg' and args.detail is None or args.focus == 'players' and args.type is None and args.detail == 'situation' or args.focus == 'players' and args.type =='on' and args.detail == 'situation' or args.focus == 'players' and args.type =='xg' and args.detail == 'situation' or args.focus == 'players' and args.type =='on_xg' and args.detail == 'situation':    
    import chart_players_onice_xg_situation
    chart_players_onice_xg_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_xg_situation


###
### UNIT CHARTS
###
    
##
## Combined
##

if args.focus == 'units' and args.type is None or args.focus == 'units' and args.type == 'on' or args.focus == 'units' and args.type == 'on_shots':    
    import chart_units_onice_shots
    chart_units_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_onice_shots
if args.focus == 'units' and args.type is None or args.focus == 'units' and args.type == 'on' or args.focus == 'units' and args.type == 'on_xg':    
    import chart_units_onice_xg
    chart_units_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_onice_xg

##
## Lines
##
    
if args.focus == 'units' and args.type is None or args.focus == 'units' and args.type == 'on' or args.focus == 'units' and args.type == 'on_shots' or args.focus == 'lines' and args.type is None or args.focus == 'lines' and args.type == 'on' or args.focus == 'lines' and args.type == 'on_shots':    
    import chart_units_lines_onice_shots
    chart_units_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_onice_shots

if args.focus == 'units' and args.type is None or args.focus == 'units' and args.type == 'on' or args.focus == 'units' and args.type == 'on_xg' or args.focus == 'lines' and args.type is None or args.focus == 'lines' and args.type == 'on' or args.focus == 'lines' and args.type == 'on_xg':    
    import chart_units_lines_onice_xg
    chart_units_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_onice_xg

if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'matchups' or args.focus == 'units' and args.type is None and args.detail == 'matchups_lines' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups_lines' or args.focus == 'units' and args.type == 'on_shots' and args.detail is None or args.focus == 'units' and args.type == 'on_shots' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on_shots' and args.detail == 'matchups_lines' or args.focus == 'lines' and args.type is None and args.detail is None or args.focus == 'lines' and args.type is None and args.detail == 'matchups' or args.focus == 'lines' and args.type is None and args.detail == 'matchups_lines' or args.focus == 'lines' and args.type == 'on' and args.detail is None or args.focus == 'lines' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'lines' and args.type == 'on' and args.detail == 'matchups_lines' or args.focus == 'lines' and args.type == 'on_shots' and args.detail is None or args.focus == 'lines' and args.type == 'on_shots' and args.detail == 'matchups' or args.focus == 'lines' and args.type == 'on_shots' and args.detail == 'matchups_lines':    
    import chart_units_lines_matchups_lines_onice_shots
    chart_units_lines_matchups_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_lines_onice_shots

if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'matchups' or args.focus == 'units' and args.type is None and args.detail == 'matchups_lines' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups_lines' or args.focus == 'units' and args.type == 'on_xg' and args.detail is None or args.focus == 'units' and args.type == 'on_xg' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on_xg' and args.detail == 'matchups_lines' or args.focus == 'lines' and args.type is None and args.detail is None or args.focus == 'lines' and args.type is None and args.detail == 'matchups' or args.focus == 'lines' and args.type is None and args.detail == 'matchups_lines' or args.focus == 'lines' and args.type == 'on' and args.detail is None or args.focus == 'lines' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'lines' and args.type == 'on' and args.detail == 'matchups_lines' or args.focus == 'lines' and args.type == 'on_xg' and args.detail is None or args.focus == 'lines' and args.type == 'on_xg' and args.detail == 'matchups' or args.focus == 'lines' and args.type == 'on_xg' and args.detail == 'matchups_lines':    
    import chart_units_lines_matchups_lines_onice_xg
    chart_units_lines_matchups_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_lines_onice_xg

if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'matchups' or args.focus == 'units' and args.type is None and args.detail == 'matchups_pairings' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups_pairings' or args.focus == 'units' and args.type == 'on_shots' and args.detail is None or args.focus == 'units' and args.type == 'on_shots' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on_shots' and args.detail == 'matchups_pairings' or args.focus == 'lines' and args.type is None and args.detail is None or args.focus == 'lines' and args.type is None and args.detail == 'matchups' or args.focus == 'lines' and args.type is None and args.detail == 'matchups_pairings' or args.focus == 'lines' and args.type == 'on' and args.detail is None or args.focus == 'lines' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'lines' and args.type == 'on' and args.detail == 'matchups_pairings' or args.focus == 'lines' and args.type == 'on_shots' and args.detail is None or args.focus == 'lines' and args.type == 'on_shots' and args.detail == 'matchups' or args.focus == 'lines' and args.type == 'on_shots' and args.detail == 'matchups_pairings':    
    import chart_units_lines_matchups_pairings_onice_shots
    chart_units_lines_matchups_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_pairings_onice_shots

if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'matchups' or args.focus == 'units' and args.type is None and args.detail == 'matchups_pairings' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups_pairings' or args.focus == 'units' and args.type == 'on_xg' and args.detail is None or args.focus == 'units' and args.type == 'on_xg' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on_xg' and args.detail == 'matchups_pairings' or args.focus == 'lines' and args.type is None and args.detail is None or args.focus == 'lines' and args.type is None and args.detail == 'matchups' or args.focus == 'lines' and args.type is None and args.detail == 'matchups_pairings' or args.focus == 'lines' and args.type == 'on' and args.detail is None or args.focus == 'lines' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'lines' and args.type == 'on' and args.detail == 'matchups_pairings' or args.focus == 'lines' and args.type == 'on_xg' and args.detail is None or args.focus == 'lines' and args.type == 'on_xg' and args.detail == 'matchups' or args.focus == 'lines' and args.type == 'on_xg' and args.detail == 'matchups_pairings':    
    import chart_units_lines_matchups_pairings_onice_xg
    chart_units_lines_matchups_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_pairings_onice_xg

if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'teammates' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'teammates' or args.focus == 'units' and args.type == 'on_shots' and args.detail is None or args.focus == 'units' and args.type == 'on_shots' and args.detail == 'teammates' or args.focus == 'lines' and args.type is None and args.detail is None or args.focus == 'lines' and args.type is None and args.detail == 'teammates' or args.focus == 'lines' and args.type == 'on' and args.detail is None or args.focus == 'lines' and args.type == 'on' and args.detail == 'teammates' or args.focus == 'lines' and args.type == 'on_shots' and args.detail is None or args.focus == 'lines' and args.type == 'on_shots' and args.detail == 'teammates':    
    import chart_units_lines_teammates_pairings_onice_shots
    chart_units_lines_teammates_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_teammates_pairings_onice_shots

if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'teammates' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'teammates' or args.focus == 'units' and args.type == 'on_xg' and args.detail is None or args.focus == 'units' and args.type == 'on_xg' and args.detail == 'teammates' or args.focus == 'lines' and args.type is None and args.detail is None or args.focus == 'lines' and args.type is None and args.detail == 'teammates' or args.focus == 'lines' and args.type == 'on' and args.detail is None or args.focus == 'lines' and args.type == 'on' and args.detail == 'teammates' or args.focus == 'lines' and args.type == 'on_xg' and args.detail is None or args.focus == 'lines' and args.type == 'on_xg' and args.detail == 'teammates':    
    import chart_units_lines_teammates_pairings_onice_xg
    chart_units_lines_teammates_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_teammates_pairings_onice_xg


##
## Pairings
##

if args.focus == 'units' and args.type is None or args.focus == 'units' and args.type == 'on' or args.focus == 'units' and args.type == 'on_shots' or args.focus == 'pairings' and args.type is None or args.focus == 'pairings' and args.type == 'on' or args.focus == 'pairings' and args.type == 'on_shots':    
    import chart_units_pairings_onice_shots
    chart_units_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_onice_shots
    
if args.focus == 'units' and args.type is None or args.focus == 'units' and args.type == 'on' or args.focus == 'units' and args.type == 'on_xg' or args.focus == 'lines' and args.type is None or args.focus == 'pairings' and args.type == 'on' or args.focus == 'pairings' and args.type == 'on_xg':    
    import chart_units_pairings_onice_xg
    chart_units_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_onice_xg

if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'matchups' or args.focus == 'units' and args.type is None and args.detail == 'matchups_lines' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups_lines' or args.focus == 'units' and args.type == 'on_shots' and args.detail is None or args.focus == 'units' and args.type == 'on_shots' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on_shots' and args.detail == 'matchups_lines' or args.focus == 'pairings' and args.type is None and args.detail is None or args.focus == 'pairings' and args.type is None and args.detail == 'matchups' or args.focus == 'pairings' and args.type is None and args.detail == 'matchups_lines' or args.focus == 'pairings' and args.type == 'on' and args.detail is None or args.focus == 'pairings' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'pairings' and args.type == 'on' and args.detail == 'matchups_lines' or args.focus == 'pairings' and args.type == 'on_shots' and args.detail is None or args.focus == 'pairings' and args.type == 'on_shots' and args.detail == 'matchups' or args.focus == 'pairings' and args.type == 'on_shots' and args.detail == 'matchups_lines':    
    import chart_units_pairings_matchups_lines_onice_shots
    chart_units_pairings_matchups_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_lines_onice_shots

if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'matchups' or args.focus == 'units' and args.type is None and args.detail == 'matchups_lines' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups_lines' or args.focus == 'units' and args.type == 'on_xg' and args.detail is None or args.focus == 'units' and args.type == 'on_xg' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on_xg' and args.detail == 'matchups_lines' or args.focus == 'pairings' and args.type is None and args.detail is None or args.focus == 'pairings' and args.type is None and args.detail == 'matchups' or args.focus == 'pairings' and args.type is None and args.detail == 'matchups_lines' or args.focus == 'pairings' and args.type == 'on' and args.detail is None or args.focus == 'pairings' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'pairings' and args.type == 'on' and args.detail == 'matchups_lines' or args.focus == 'pairings' and args.type == 'on_xg' and args.detail is None or args.focus == 'pairings' and args.type == 'on_xg' and args.detail == 'matchups' or args.focus == 'pairings' and args.type == 'on_xg' and args.detail == 'matchups_lines':    
    import chart_units_pairings_matchups_lines_onice_xg
    chart_units_pairings_matchups_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_lines_onice_xg

if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'matchups' or args.focus == 'units' and args.type is None and args.detail == 'matchups_pairings' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups_pairings' or args.focus == 'units' and args.type == 'on_shots' and args.detail is None or args.focus == 'units' and args.type == 'on_shots' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on_shots' and args.detail == 'matchups_pairings' or args.focus == 'pairings' and args.type is None and args.detail is None or args.focus == 'pairings' and args.type is None and args.detail == 'matchups' or args.focus == 'pairings' and args.type is None and args.detail == 'matchups_pairings' or args.focus == 'pairings' and args.type == 'on' and args.detail is None or args.focus == 'pairings' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'pairings' and args.type == 'on' and args.detail == 'matchups_pairings' or args.focus == 'pairings' and args.type == 'on_shots' and args.detail is None or args.focus == 'pairings' and args.type == 'on_shots' and args.detail == 'matchups' or args.focus == 'pairings' and args.type == 'on_shots' and args.detail == 'matchups_pairings':    
    import chart_units_pairings_matchups_pairings_onice_shots
    chart_units_pairings_matchups_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_pairings_onice_shots
    
if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'matchups' or args.focus == 'units' and args.type is None and args.detail == 'matchups_pairings' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on' and args.detail == 'matchups_pairings' or args.focus == 'units' and args.type == 'on_xg' and args.detail is None or args.focus == 'units' and args.type == 'on_xg' and args.detail == 'matchups' or args.focus == 'units' and args.type == 'on_xg' and args.detail == 'matchups_pairings' or args.focus == 'pairings' and args.type is None and args.detail is None or args.focus == 'pairings' and args.type is None and args.detail == 'matchups' or args.focus == 'pairings' and args.type is None and args.detail == 'matchups_pairings' or args.focus == 'pairings' and args.type == 'on' and args.detail is None or args.focus == 'pairings' and args.type == 'on' and args.detail == 'matchups' or args.focus == 'pairings' and args.type == 'on' and args.detail == 'matchups_pairings' or args.focus == 'pairings' and args.type == 'on_xg' and args.detail is None or args.focus == 'pairings' and args.type == 'on_xg' and args.detail == 'matchups' or args.focus == 'pairings' and args.type == 'on_xg' and args.detail == 'matchups_pairings':    
    import chart_units_pairings_matchups_pairings_onice_xg
    chart_units_pairings_matchups_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_pairings_onice_xg

if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'teammates' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'teammates' or args.focus == 'units' and args.type == 'on_shots' and args.detail is None or args.focus == 'units' and args.type == 'on_shots' and args.detail == 'teammates' or args.focus == 'pairings' and args.type is None and args.detail is None or args.focus == 'pairings' and args.type is None and args.detail == 'teammates' or args.focus == 'pairings' and args.type == 'on' and args.detail is None or args.focus == 'pairings' and args.type == 'on' and args.detail == 'teammates' or args.focus == 'pairings' and args.type == 'on_shots' and args.detail is None or args.focus == 'pairings' and args.type == 'on_shots' and args.detail == 'teammates':    
    import chart_units_pairings_teammates_lines_onice_shots
    chart_units_pairings_teammates_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_teammates_lines_onice_shots

if args.focus == 'units' and args.type is None and args.detail is None or args.focus == 'units' and args.type is None and args.detail == 'teammates' or args.focus == 'units' and args.type == 'on' and args.detail is None or args.focus == 'units' and args.type == 'on' and args.detail == 'teammates' or args.focus == 'units' and args.type == 'on_xg' and args.detail is None or args.focus == 'units' and args.type == 'on_xg' and args.detail == 'teammates' or args.focus == 'pairings' and args.type is None and args.detail is None or args.focus == 'pairings' and args.type is None and args.detail == 'teammates' or args.focus == 'pairings' and args.type == 'on' and args.detail is None or args.focus == 'pairings' and args.type == 'on' and args.detail == 'teammates' or args.focus == 'pairings' and args.type == 'on_xg' and args.detail is None or args.focus == 'pairings' and args.type == 'on_xg' and args.detail == 'teammates':    
    import chart_units_pairings_teammates_lines_onice_xg
    chart_units_pairings_teammates_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_teammates_lines_onice_xg