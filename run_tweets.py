# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import argparse

parser = argparse.ArgumentParser()


###
### COMMAND LINE ARGUMENTS
###

parser.add_argument('season_id', help='Set to [8-digit season number] (e.g. 20182019)')
parser.add_argument('game_id', help='Set to [5-digit game number] game (e.g. 20001)')

parser.add_argument('--teams', dest='teams', help='Set to [no] to bypass tweeting team charts', required=False)
parser.add_argument('--players', dest='players', help='Set to [no] to bypass tweeting all players charts', required=False)
parser.add_argument('--units', dest='units', help='Set to [no] to bypass tweeting all units charts', required=False)

parser.add_argument('--scope', dest='scope', help='Set to [more] to run additional scripts for teams, players and units', required=False)

args = parser.parse_args()


###
### Teams
###
    
if args.teams != 'no':
    import tweet_teams_gameflow
    tweet_teams_gameflow.parse_ids(args.season_id, args.game_id)
    tweet_teams_gameflow
   
    import tweet_teams_shotmaps
    tweet_teams_shotmaps.parse_ids(args.season_id, args.game_id)  
    tweet_teams_shotmaps


###
### Players
###
    
if args.players != 'no':    
    import tweet_players_gamescore
    tweet_players_gamescore.parse_ids(args.season_id, args.game_id)
    tweet_players_gamescore

    import tweet_players_individual
    tweet_players_individual.parse_ids(args.season_id, args.game_id)
    tweet_players_individual
  
    import tweet_players_onice
    tweet_players_onice.parse_ids(args.season_id, args.game_id)
    tweet_players_onice

    
###
### Units
###
    
if args.units != 'no':
    import tweet_units_onice
    tweet_units_onice.parse_ids(args.season_id, args.game_id)
    tweet_units_onice

if args.units != 'skip' and args.scope == 'more' and args.tweet != 'no':
    import tweet_units_lines_matchups_lines
    tweet_units_lines_matchups_lines.parse_ids(args.season_id, args.game_id)
    tweet_units_lines_matchups_lines
    
    import tweet_units_lines_matchups_pairings
    tweet_units_lines_matchups_pairings.parse_ids(args.season_id, args.game_id)
    tweet_units_lines_matchups_pairings
    
    import tweet_units_lines_teammates_pairings
    tweet_units_lines_teammates_pairings.parse_ids(args.season_id, args.game_id)
    tweet_units_lines_teammates_pairings