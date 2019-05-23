# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

from bs4 import BeautifulSoup
import csv
import pandas as pd
import parameters
import dict_names

def parse_ids(season_id, game_id):

    ### pull common variables from the parameters file   
    files_root = parameters.files_root
    
    ### generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()
    
    ### establish file locations and destinations
    rosters_in = files_root + 'rosters.HTM'
    rosters_out = files_root + 'rosters.csv'
           
    ###
    ### ROSTERS (HTM)
    ###
    
    ### load the rosters (HTM) file and convert it to a BeautifulSoup object
    with open(rosters_in, 'r') as htm_rosters:
        roster_soup = BeautifulSoup(htm_rosters, 'html.parser')
    
        ### get full rosters for home and away teams and create a tuple (#, Pos, Name)
        home_roster = roster_soup.select('.border')[3].find_all('td')[3:]
        away_roster = roster_soup.select('.border')[2].find_all('td')[3:]
    
        home_roster = [i.string.strip() for i in home_roster]
        away_roster = [i.string.strip() for i in away_roster]
    
        home_roster = [list(h) for h in zip(home_roster[0::3], home_roster[1::3], home_roster[2::3])]
        away_roster = [list(a) for a in zip(away_roster[0::3], away_roster[1::3], away_roster[2::3])]
    
        ### remove (C) or (A) from the end of the names of captains and alternates
        for i in range(len(home_roster)-1):
            try:
                if (home_roster[i][2][-1] == ')'):
                    home_roster[i][2] = home_roster[i][2][:-5]
                if (away_roster[i][2][-1] == ')'):
                    away_roster[i][2] = away_roster[i][2][:-5]
            except:
                pass
    
        ### begin writing both rosters to one .csv; write column titles to a header row
        csvRows = [('SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'PLAYER_NO', 'PLAYER_NAME', 'PLAYER_POS')]
    
        ### loop through the away players
        for l in away_roster:
            try:
                away_player = l[2].upper().replace(' ', '.')
                away_player = dict_names.NAMES[away_player]
            except:
                pass
            csvRows += [(season_id, game_id, date, 'Away', away, l[0], away_player, l[1])]
    
        ### loop through the home players
        for l in home_roster:
            try:
                home_player = l[2].upper().replace(' ', '.')
                home_player = dict_names.NAMES[home_player]
            except:
                pass
            csvRows += [(season_id, game_id, date, 'Home', home, l[0], home_player, l[1])]
    
        ### trigger and write to the outfile
        with open(rosters_out, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(csvRows)
    
        ### create a dataframe using the newly-created outfile
        rosters_df = pd.read_csv(rosters_out)

        ### replace names for special name cases
        try:
            rosters_df.loc[(rosters_df.PLAYER_NAME == 'SEBASTIAN.AHO') & (rosters_df.TEAM == 'CAR'),['PLAYER_NAME']] = 'SEBASTIAN.A.AHO'; rosters_df
            rosters_df.loc[(rosters_df.PLAYER_NAME == 'SEBASTIAN.AHO') & (rosters_df.TEAM == 'NYI'),['PLAYER_NAME']] = 'SEBASTIAN.J.AHO'; rosters_df
        except:
            pass
        
        ### search for and change known instances of players whose positions are incorrectly classified
        try:
            rosters_df.loc[(rosters_df.PLAYER_NAME == 'LUKE.WITKOWSKI') & (rosters_df.PLAYER_POS != 'D'),['PLAYER_POS']] = 'D'; rosters_df
        except:
            pass
    
        ### add a new column to the dataframe that duplicates the player position values
        rosters_df['PLAYER_POS_DETAIL'] = rosters_df['PLAYER_POS']
    
        ###  change the 'C', 'R' or 'L' designations in the original player position column to 'F'
        rosters_df.loc[(rosters_df.PLAYER_POS != 'D') & (rosters_df.PLAYER_POS != 'G'),['PLAYER_POS']] = 'F'; rosters_df
        rosters_df.to_csv(rosters_out, index=False)
    
    
    print('Finished parsing NHL rosters from .HTM for ' + season_id + ' ' + game_id)