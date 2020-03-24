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

parser.add_argument('--teams', dest='teams', help='Can set to true', required=False)
parser.add_argument('--teams_stats', dest='teams_stats', help='Can set to true, period or situation', required=False)
parser.add_argument('--teams_charts', dest='teams_charts', help='Can set to true, gameflow, scatter, scatter_period or scatter_situation', required=False)

parser.add_argument('--players', dest='players', help='Can set to true', required=False)
parser.add_argument('--players_stats', dest='players_stats', help='Can set to true, period, situation, opponents or teammates', required=False)
parser.add_argument('--players_charts', dest='players_charts', help='Can set to true, gamescore or shots', required=False)

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
parser.add_argument('--flush', dest='flush', help='Setting to true will remove all non-schedule files', required=False)
parser.add_argument('--load_pbp', dest='load_pbp', help='Setting to true will load a stored play-by-play file', required=False)

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
    import files_parse_toi
    files_parse_toi.parse_ids(args.season_id, args.game_id, args.load_pbp)
    files_parse_toi

if args.parse == 'true' or args.parse == 'merge_pbp': 
    import files_parse_merge_pbp
    files_parse_merge_pbp.parse_ids(args.season_id, args.game_id, args.load_pbp)
    files_parse_merge_pbp

if args.parse == 'true' or args.parse == 'xg': 
    import files_parse_xg
    files_parse_xg.parse_ids(args.season_id, args.game_id)
    files_parse_xg


###
### TEAMS
###

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


###
### PLAYERS
###

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


###
### UNITS
###

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

if args.units == 'true' or args.units_stats_pp == 'true':
    import stats_units_pp
    stats_units_pp.parse_ids(args.season_id, args.game_id)
    stats_units_pp

if args.units == 'true' or args.units_stats_pk == 'true':
    import stats_units_pk
    stats_units_pk.parse_ids(args.season_id, args.game_id)
    stats_units_pk


if args.units == 'true' or args.units_charts == 'true' or args.units == 'chart_shots' or args.units_charts == 'shots':
    import chart_units_onice_shots
    chart_units_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_onice_shots
if args.units == 'true' or args.units_charts == 'true' or args.units == 'chart_xg' or args.units_charts == 'xg':
    import chart_units_onice_xg
    chart_units_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_onice_xg

  
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