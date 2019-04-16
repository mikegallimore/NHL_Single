# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 21:10:47 2017

@author: @mikegallimore
"""

import argparse

parser = argparse.ArgumentParser()

### creates arguments to make use of in functions
parser.add_argument('--season_id', dest='season_id', required=False)
parser.add_argument('--game_id', dest='game_id', required=False)
parser.add_argument('--extent', dest='extent', required=False)
parser.add_argument('--fetch', dest='fetch', required=False)
parser.add_argument('--parse', dest='parse', required=False)
parser.add_argument('--teams', dest='teams', required=False)
parser.add_argument('--players', dest='players', required=False)
parser.add_argument('--units', dest='units', required=False)
parser.add_argument('--images', dest='images', required=False)
parser.add_argument('--tweet', dest='tweet', required=False)

args = parser.parse_args()

### fetch game files
if args.fetch != 'skip':
    import files_fetch
    files_fetch.parse_ids(args.season_id, args.game_id)
    files_fetch

### parse game files
if args.parse != 'skip':
    import files_parse_rosters
    files_parse_rosters.parse_ids(args.season_id, args.game_id)
    files_parse_rosters
    
    import files_parse_shifts
    files_parse_shifts.parse_ids(args.season_id, args.game_id)
    files_parse_shifts
    
    import files_parse_pbp
    files_parse_pbp.parse_ids(args.season_id, args.game_id)
    files_parse_pbp
    
    import files_parse_TOI
    files_parse_TOI.parse_ids(args.season_id, args.game_id)
    files_parse_TOI
    
    import files_parse_merge_pbp
    files_parse_merge_pbp.parse_ids(args.season_id, args.game_id)
    files_parse_merge_pbp


### Teams
if args.teams != 'skip':
    import stats_teams
    stats_teams.parse_ids(args.season_id, args.game_id)
    stats_teams
    
    import chart_teams_shots_gameflow
    chart_teams_shots_gameflow.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_gameflow

    import chart_teams_shots_scatter
    chart_teams_shots_scatter.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_scatter

    import chart_teams_shots_density
    chart_teams_shots_density.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_density    

if args.teams != 'skip' and args.tweet != 'no':
    import tweet_teams_gameflow
    tweet_teams_gameflow.parse_ids(args.season_id, args.game_id)
    tweet_teams_gameflow
   
    import tweet_teams_shotmaps
    tweet_teams_shotmaps.parse_ids(args.season_id, args.game_id)  
    tweet_teams_shotmaps
    
if args.teams != 'skip' and args.extent == 'full':
    import stats_teams_period
    stats_teams_period.parse_ids(args.season_id, args.game_id)
    stats_teams_period
    
    import stats_teams_situation
    stats_teams_situation.parse_ids(args.season_id, args.game_id)
    stats_teams_situation
 
    import chart_teams_shots_scatter_period
    chart_teams_shots_scatter_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_scatter_period
    
    import chart_teams_shots_scatter_situation
    chart_teams_shots_scatter_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_scatter_situation

### Players
if args.players != 'skip':    
    import stats_players
    stats_players.parse_ids(args.season_id, args.game_id)
    stats_players
    
    import stats_players_period
    stats_players_period.parse_ids(args.season_id, args.game_id)
    stats_players_period
    
    import stats_players_situation
    stats_players_situation.parse_ids(args.season_id, args.game_id)
    stats_players_situation

    import chart_players_onice_shots
    chart_players_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_shots

if args.players != 'skip' and args.tweet != 'no': 
    import tweet_players_onice_shots
    tweet_players_onice_shots.parse_ids(args.season_id, args.game_id)
    tweet_players_onice_shots

if args.players != 'skip' and args.extent == 'full':    
    import stats_players_teammates
    stats_players_teammates.parse_ids(args.season_id, args.game_id)
    stats_players_teammates
    
    import stats_players_opponents
    stats_players_opponents.parse_ids(args.season_id, args.game_id)
    stats_players_opponents
   

### Units
if args.units != 'skip':
    import stats_units_lines
    stats_units_lines.parse_ids(args.season_id, args.game_id)
    stats_units_lines

    import stats_units_pairings
    stats_units_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_pairings
    
    import chart_units_onice_shots
    chart_units_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_onice_shots

if args.units != 'skip' and args.tweet != 'no': 
    import tweet_units_onice_shots
    tweet_units_onice_shots.parse_ids(args.season_id, args.game_id)
    tweet_units_onice_shots

if args.units != 'skip' and args.extent == 'full':
    import stats_units_lines_matchups_lines
    stats_units_lines_matchups_lines.parse_ids(args.season_id, args.game_id)
    stats_units_lines_matchups_lines
    
    import stats_units_lines_matchups_pairings
    stats_units_lines_matchups_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_lines_matchups_pairings
    
    import stats_units_lines_teammates_pairings
    stats_units_lines_teammates_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_lines_teammates_pairings
    
    import stats_units_pairings_matchups_lines
    stats_units_pairings_matchups_lines.parse_ids(args.season_id, args.game_id)
    stats_units_pairings_matchups_lines
    
    import stats_units_pairings_matchups_pairings
    stats_units_pairings_matchups_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_pairings_matchups_pairings
    
    import stats_units_pairings_teammates_lines
    stats_units_pairings_teammates_lines.parse_ids(args.season_id, args.game_id)
    stats_units_pairings_teammates_lines