# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import argparse

parser = argparse.ArgumentParser()

### creates arguments to make use of in functions
parser.add_argument('season_id', help='Set the season (e.g. 20182019)')
parser.add_argument('game_id', help='Set the game (e.g. 20001)')

parser.add_argument('--focus', dest='focus', help='Can set to [teams, players, units, lines, pairings, pp, pk]', required=False)
parser.add_argument('--detail', dest='detail', help='Can set to [basic, period, situation] for teams, [basic, period, situation, opponents, teammates] for players, [basic, matchups, matchups_lines, matchups_pairings, teammates] for units', required=False)

args = parser.parse_args()


###
### TEAM STATS
###

if args.focus == 'teams' and args.detail is None or args.focus == 'teams' and args.detail == 'basic':    
    import stats_teams
    stats_teams.parse_ids(args.season_id, args.game_id)
    stats_teams

if args.focus == 'teams' and args.detail is None or args.focus == 'teams' and args.detail == 'period':    
    import stats_teams_period
    stats_teams_period.parse_ids(args.season_id, args.game_id)
    stats_teams_period

if args.focus == 'teams' and args.detail is None or args.focus == 'teams' and args.detail == 'situation':    
    import stats_teams_situation
    stats_teams_situation.parse_ids(args.season_id, args.game_id)
    stats_teams_situation


###
### PLAYER STATS
###

if args.focus == 'players' and args.detail is None or args.focus == 'players' and args.detail == 'basic':    
    import stats_players
    stats_players.parse_ids(args.season_id, args.game_id)
    stats_players

if args.focus == 'players' and args.detail is None or args.focus == 'players' and args.detail == 'period':    
    import stats_players_period
    stats_players_period.parse_ids(args.season_id, args.game_id)
    stats_players_period

if args.focus == 'players' and args.detail is None or args.focus == 'players' and args.detail == 'situation':    
    import stats_players_situation
    stats_players_situation.parse_ids(args.season_id, args.game_id)
    stats_players_situation

if args.focus == 'players' and args.detail is None or args.focus == 'players' and args.detail == 'opponents':    
    import stats_players_opponents
    stats_players_opponents.parse_ids(args.season_id, args.game_id)
    stats_players_opponents

if args.focus == 'players' and args.detail is None or args.focus == 'players' and args.detail == 'teammates':    
    import stats_players_teammates
    stats_players_teammates.parse_ids(args.season_id, args.game_id)
    stats_players_teammates


###
### UNIT STATS
###

##
## Lines
##
    
if args.focus == 'units' and args.detail is None or args.focus == 'units' and args.detail == 'basic' or args.focus == 'lines' and args.detail is None or args.focus == 'lines' and args.detail == 'basic':    
    import stats_units_lines
    stats_units_lines.parse_ids(args.season_id, args.game_id)
    stats_units_lines

if args.focus == 'units' and args.detail is None or args.focus == 'units' and args.detail == 'matchups' or args.focus == 'units' and args.detail == 'matchups_lines' or args.focus == 'lines' and args.detail is None or args.focus == 'lines' and args.detail == 'matchups' or args.focus == 'lines' and args.detail == 'matchups_lines':    
    import stats_units_lines_matchups_lines
    stats_units_lines_matchups_lines.parse_ids(args.season_id, args.game_id)
    stats_units_lines_matchups_lines

if args.focus == 'units' and args.detail is None or args.focus == 'units' and args.detail == 'matchups' or args.focus == 'units' and args.detail == 'matchups_pairings' or args.focus == 'lines' and args.detail is None or args.focus == 'lines' and args.detail == 'matchups' or args.focus == 'lines' and args.detail == 'matchups_pairings':    
    import stats_units_lines_matchups_pairings
    stats_units_lines_matchups_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_lines_matchups_pairings

if args.focus == 'units' and args.detail is None or args.focus == 'units' and args.detail == 'teammates' or args.focus == 'lines' and args.detail is None or args.focus == 'lines' and args.detail == 'teammates':    
    import stats_units_lines_teammates_pairings
    stats_units_lines_teammates_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_lines_teammates_pairings

##
## Pairings
##

if args.focus == 'units' and args.detail is None or args.focus == 'units' and args.detail == 'basic' or args.focus == 'pairings' and args.detail is None or args.focus == 'pairings' and args.detail == 'basic':    
    import stats_units_pairings
    stats_units_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_pairings

if args.focus == 'units' and args.detail is None or args.focus == 'units' and args.detail == 'matchups' or args.focus == 'units' and args.detail == 'matchups_lines' or args.focus == 'pairings' and args.detail is None or args.focus == 'pairings' and args.detail == 'matchups' or args.focus == 'pairings' and args.detail == 'matchups_lines':    
    import stats_units_pairings_matchups_lines
    stats_units_pairings_matchups_lines.parse_ids(args.season_id, args.game_id)
    stats_units_pairings_matchups_lines

if args.focus == 'units' and args.detail is None or args.focus == 'units' and args.detail == 'matchups' or args.focus == 'units' and args.detail == 'matchups_pairings' or args.focus == 'pairings' and args.detail is None or args.focus == 'pairings' and args.detail == 'matchups' or args.focus == 'pairings' and args.detail == 'matchups_pairings':    
    import stats_units_pairings_matchups_pairings
    stats_units_pairings_matchups_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_pairings_matchups_pairings

if args.focus == 'units' and args.detail is None or args.focus == 'units' and args.detail == 'teammates' or args.focus == 'pairings' and args.detail is None or args.focus == 'pairings' and args.detail == 'teammates':    
    import stats_units_pairings_teammates_lines
    stats_units_pairings_teammates_lines.parse_ids(args.season_id, args.game_id)
    stats_units_pairings_teammates_lines

##
## Power Play
##

if args.focus == 'units' and args.detail is None or args.focus == 'units' and args.detail == 'basic' or args.focus == 'pp' and args.detail is None or args.focus == 'pp' and args.detail == 'basic':
    import stats_units_pp
    stats_units_pp.parse_ids(args.season_id, args.game_id)
    stats_units_pp

##
## Penalty Kill
##
    
if args.focus == 'units' and args.detail is None or args.focus == 'units' and args.detail == 'basic' or args.focus == 'pk' and args.detail is None or args.focus == 'pk' and args.detail == 'basic':
    import stats_units_pk
    stats_units_pk.parse_ids(args.season_id, args.game_id)
    stats_units_pk