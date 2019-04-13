# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 21:10:47 2017

@author: @mikegallimore
"""

import argparse

parser = argparse.ArgumentParser()

### creates arguments to make use of in functions
parser.add_argument("--season_id", dest="season_id", required=False)
parser.add_argument("--game_id", dest="game_id", required=False)

args = parser.parse_args()

### passes the arguments through to parameters.py
#import files_fetch
#files_fetch.parse_ids(args.season_id, args.game_id)
#files_fetch

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
import stats_teams
stats_teams.parse_ids(args.season_id, args.game_id)
stats_teams

import stats_teams_period
stats_teams_period.parse_ids(args.season_id, args.game_id)
stats_teams_period

import stats_teams_situation
stats_teams_situation.parse_ids(args.season_id, args.game_id)
stats_teams_situation

'''
import stats_teams_period
import stats_teams_situation
stats_teams
stats_teams_period
stats_teams_situation

import chart_teams_shots_scatter
import chart_teams_shots_scatter_period
import chart_teams_shots_scatter_situation
import chart_teams_shots_density
import chart_teams_shots_gameflow
chart_teams_shots_scatter
chart_teams_shots_scatter_period
chart_teams_shots_scatter_situation
chart_teams_shots_density
chart_teams_shots_gameflow

import tweet_teams_gameflow
import tweet_teams_shotmaps
tweet_teams_gameflow
tweet_teams_shotmaps


### Players
import stats_players
import stats_players_period
import stats_players_situation
stats_players
stats_players_period
stats_players_situation

import chart_players_onice_shots
chart_players_onice_shots

import tweet_players_onice_shots
tweet_players_onice_shots


### Units
import stats_units_lines
import stats_units_pairings
stats_units_lines
stats_units_pairings

import chart_units_onice_shots
chart_units_onice_shots

import tweet_units_onice_shots
tweet_units_onice_shots
'''