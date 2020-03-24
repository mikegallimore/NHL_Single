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

parser.add_argument ('--flush', dest='flush', help='Set to no to avoid deleting prexisting charts and files', required=False)

parser.add_argument('--fetch', dest='fetch', help='Set to skip to bypass retrieving game files', required=False)
parser.add_argument('--parse', dest='parse', help='Set to skip to bypass parsing game files', required=False)

parser.add_argument('--teams', dest='teams', help='Set to skip to bypass running all scripts for teams', required=False)
parser.add_argument('--players', dest='players', help='Set to skip to bypass running all scripts for players', required=False)
parser.add_argument('--units', dest='units', help='Set to skip to bypass running all scripts for units', required=False)

parser.add_argument('--scope', dest='scope', help='Set to full to run additional scripts for teams, players and units', required=False)

parser.add_argument('--images', dest='images', help='Set to show will display images as they are generated', required=False)

parser.add_argument('--tweet', dest='tweet', help='Set to no to bypass sending autogenerated tweets', required=False)

### relevant for the 20062007 season only (explained in the 'Limitations' section of the README
parser.add_argument('--load_pbp', dest='load_pbp', help='Set to true to load a stored play-by-play file', required=False)

### relevant to instances where players are recorded as in the lineup at one position but really playing another (e.g. Luke Witkowski listed as a D while playing F)
parser.add_argument('--switch_F2D', dest='switch_F2D', help='Set to player name (e.g. Luke_Witkowski)', required=False)
parser.add_argument('--switch_D2F', dest='switch_D2F', help='Set to player name (e.g. Luke_Witkowski)', required=False)

args = parser.parse_args()


###
### FLUSH
###

if args.flush != 'no':
    import flush_charts
    flush_charts

    import flush_files
    flush_files.parse_ids(args.season_id, args.game_id)


###
### FETCH
###

if args.fetch != 'skip':
    import files_fetch
    files_fetch.parse_ids(args.season_id, args.game_id)
    files_fetch


###
### PARSE
###
    
if args.parse != 'skip':
    import files_parse_rosters
    files_parse_rosters.parse_ids(args.season_id, args.game_id, args.switch_F2D, args.switch_D2F)
    files_parse_rosters
    
    import files_parse_shifts
    files_parse_shifts.parse_ids(args.season_id, args.game_id)
    files_parse_shifts
    
    import files_parse_pbp
    files_parse_pbp.parse_ids(args.season_id, args.game_id, args.load_pbp)
    files_parse_pbp
    
    import files_parse_toi
    files_parse_toi.parse_ids(args.season_id, args.game_id, args.load_pbp)
    files_parse_toi

    import files_parse_merge_pbp
    files_parse_merge_pbp.parse_ids(args.season_id, args.game_id, args.load_pbp)
    files_parse_merge_pbp

    import files_parse_xg
    files_parse_xg.parse_ids(args.season_id, args.game_id)
    files_parse_xg


###
### Teams
###
    
if args.teams != 'skip':
    import stats_teams
    stats_teams.parse_ids(args.season_id, args.game_id)
    stats_teams


    import chart_teams_gameflow_shots
    chart_teams_gameflow_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_gameflow_shots

    import chart_teams_gameflow_xg
    chart_teams_gameflow_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_gameflow_xg

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

    
if args.teams != 'skip' and args.scope == 'full':
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

    import chart_teams_shots_density_period
    chart_teams_shots_density_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_density_period
    
    import chart_teams_shots_density_situation
    chart_teams_shots_density_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_teams_shots_density_situation


###
### Players
###
    
if args.players != 'skip':    
    import stats_players
    stats_players.parse_ids(args.season_id, args.game_id)
    stats_players


    import chart_players_gamescore
    chart_players_gamescore.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_gamescore

    import chart_players_individual_shots
    chart_players_individual_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_shots
    
    import chart_players_individual_xg
    chart_players_individual_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_xg

    import chart_players_onice_shots
    chart_players_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_shots
    
    import chart_players_onice_xg
    chart_players_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_xg


if args.players != 'skip' and args.tweet != 'no': 
    import tweet_players_gamescore
    tweet_players_gamescore.parse_ids(args.season_id, args.game_id)
    tweet_players_gamescore

    import tweet_players_individual
    tweet_players_individual.parse_ids(args.season_id, args.game_id)
    tweet_players_individual
  
    import tweet_players_onice
    tweet_players_onice.parse_ids(args.season_id, args.game_id)
    tweet_players_onice


if args.players != 'skip' and args.scope == 'full':    
    import stats_players_period
    stats_players_period.parse_ids(args.season_id, args.game_id)
    stats_players_period
    
    import stats_players_situation
    stats_players_situation.parse_ids(args.season_id, args.game_id)
    stats_players_situation

    import stats_players_teammates
    stats_players_teammates.parse_ids(args.season_id, args.game_id)
    stats_players_teammates
    
    import stats_players_opponents
    stats_players_opponents.parse_ids(args.season_id, args.game_id)
    stats_players_opponents


    import chart_players_gamescore_period
    chart_players_gamescore_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_gamescore_period

    import chart_players_gamescore_situation
    chart_players_gamescore_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_gamescore_situation

    import chart_players_individual_shots_period
    chart_players_individual_shots_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_shots_period

    import chart_players_individual_shots_situation
    chart_players_individual_shots_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_shots_situation
    
    import chart_players_individual_xg_period
    chart_players_individual_xg_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_xg_period

    import chart_players_individual_xg_situation
    chart_players_individual_xg_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_individual_xg_situation

    import chart_players_onice_shots_period
    chart_players_onice_shots_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_shots_period

    import chart_players_onice_shots_situation
    chart_players_onice_shots_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_shots_situation
    
    import chart_players_onice_xg_period
    chart_players_onice_xg_period.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_xg_period

    import chart_players_onice_xg_situation
    chart_players_onice_xg_situation.parse_ids(args.season_id, args.game_id, args.images)
    chart_players_onice_xg_situation
    
###
### Units
###
    
if args.units != 'skip':
    import stats_units_lines
    stats_units_lines.parse_ids(args.season_id, args.game_id)
    stats_units_lines

    import stats_units_pairings
    stats_units_pairings.parse_ids(args.season_id, args.game_id)
    stats_units_pairings

    import stats_units_pp
    stats_units_pp.parse_ids(args.season_id, args.game_id)
    stats_units_pp

    import stats_units_pk
    stats_units_pk.parse_ids(args.season_id, args.game_id)
    stats_units_pk

    
    import chart_units_onice_shots
    chart_units_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_onice_shots

    import chart_units_onice_xg
    chart_units_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_onice_xg
    
    import chart_units_lines_onice_shots
    chart_units_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_onice_shots

    import chart_units_lines_onice_xg
    chart_units_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_onice_xg
    
    import chart_units_pairings_onice_shots
    chart_units_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_onice_shots    

    import chart_units_pairings_onice_xg
    chart_units_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_onice_xg


if args.units != 'skip' and args.tweet != 'no': 
    import tweet_units_onice
    tweet_units_onice.parse_ids(args.season_id, args.game_id)
    tweet_units_onice


if args.units != 'skip' and args.scope == 'full':
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
    
    import chart_units_lines_matchups_lines_onice_shots
    chart_units_lines_matchups_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_lines_onice_shots

    import chart_units_lines_matchups_lines_onice_xg
    chart_units_lines_matchups_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_lines_onice_xg
    
    import chart_units_lines_matchups_pairings_onice_shots
    chart_units_lines_matchups_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_pairings_onice_shots

    import chart_units_lines_matchups_pairings_onice_xg
    chart_units_lines_matchups_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_matchups_pairings_onice_xg
    
    import chart_units_lines_teammates_pairings_onice_shots
    chart_units_lines_teammates_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_teammates_pairings_onice_shots

    import chart_units_lines_teammates_pairings_onice_xg
    chart_units_lines_teammates_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_lines_teammates_pairings_onice_xg

    import chart_units_pairings_matchups_lines_onice_shots
    chart_units_pairings_matchups_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_lines_onice_shots

    import chart_units_pairings_matchups_lines_onice_xg
    chart_units_pairings_matchups_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_lines_onice_xg
    
    import chart_units_pairings_matchups_pairings_onice_shots
    chart_units_pairings_matchups_pairings_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_pairings_onice_shots

    import chart_units_pairings_matchups_pairings_onice_xg
    chart_units_pairings_matchups_pairings_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_matchups_pairings_onice_xg
    
    import chart_units_pairings_teammates_lines_onice_shots
    chart_units_pairings_teammates_lines_onice_shots.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_teammates_lines_onice_shots
    
    import chart_units_pairings_teammates_lines_onice_xg
    chart_units_pairings_teammates_lines_onice_xg.parse_ids(args.season_id, args.game_id, args.images)
    chart_units_pairings_teammates_lines_onice_xg

if args.units != 'skip' and args.scope == 'full' and args.tweet != 'no':
    import tweet_units_lines_matchups_lines
    tweet_units_lines_matchups_lines.parse_ids(args.season_id, args.game_id)
    tweet_units_lines_matchups_lines
    
    import tweet_units_lines_matchups_pairings
    tweet_units_lines_matchups_pairings.parse_ids(args.season_id, args.game_id)
    tweet_units_lines_matchups_pairings
    
    import tweet_units_lines_teammates_pairings
    tweet_units_lines_teammates_pairings.parse_ids(args.season_id, args.game_id)
    tweet_units_lines_teammates_pairings