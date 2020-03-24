# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

from bs4 import BeautifulSoup
import json
import csv
import parameters
import requests
import pandas as pd
import os
import xml.etree.ElementTree as ET 
import dict_names
import dict_penalties
import dict_teams
import re

def escape_xml_illegal_chars(unicodeString, replaceWith=u'?'):
	return re.sub(u'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]', replaceWith, unicodeString)

def parse_ids(season_id, game_id, load_pbp):

    ### pull common variables from the parameters file
    files_root = parameters.files_root
    files_20062007 = parameters.files_20062007

    ### generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()

    ### establish file locations and destinations
    livefeed_source = files_root + 'livefeed.json'
    livefeed_outfile = files_root + 'livefeed.csv'
    pbp_source = files_root + 'pbp.HTM'
    pbp_outfile = files_root + 'pbp.csv'
    pbp_outfile_20062007 = files_20062007 + season_id + '_' + game_id + '_pbp.csv'
    pbp_temp = files_root + 'pbp_temp.csv'
 
    ### access the game's roster file in order to create team-specific dicts and lists
    rosters_csv = files_root + 'rosters.csv'
    
    rosters_df = pd.read_csv(rosters_csv)
    
    rosters_table = rosters_df[['TEAM','PLAYER_NO', 'PLAYER_NAME', 'PLAYER_POS']]
    
    homeROS_df = rosters_table.copy()
    homeROS_df = homeROS_df[(homeROS_df['TEAM'] == home)]
    homeROS_dict = homeROS_df[['PLAYER_NO', 'PLAYER_NAME']].set_index('PLAYER_NO').T.to_dict('list')
    homeROS_list = homeROS_df['PLAYER_NAME'].tolist()
    
    homeG_df = rosters_table.copy()
    homeG_df = homeG_df[(homeG_df.TEAM == home) & (homeG_df.PLAYER_POS == 'G')]
    homeG = homeG_df['PLAYER_NAME'].tolist()
    
    awayROS_df = rosters_table.copy()
    awayROS_df = awayROS_df[(awayROS_df['TEAM'] == away)]
    awayROS_dict = awayROS_df[['PLAYER_NO', 'PLAYER_NAME']].set_index('PLAYER_NO').T.to_dict('list')
    awayROS_list = awayROS_df['PLAYER_NAME'].tolist()
    
    awayG_df = rosters_table.copy()
    awayG_df = awayG_df[(awayG_df.TEAM == away) & (awayG_df.PLAYER_POS == 'G')]
    awayG = awayG_df['PLAYER_NAME'].tolist()
    
    ### open the game's livefeed (JSON) file to create a few shared variables
    with open(livefeed_source) as livefeed_json:
        livefeed_data = json.load(livefeed_json)
    
        try:
            game_status = livefeed_data["liveData"]["linescore"]["currentPeriodTimeRemaining"]
            currentperiod = livefeed_data["liveData"]["linescore"]["currentPeriod"]
    
            if game_status != 'Final' and currentperiod < 4:
                game_type = 'Regulation'
            elif game_status != 'Final' and currentperiod == 4:
                game_type = 'Overtime'
            elif game_status != 'Final' and currentperiod == 5:
                game_type = 'Shootout'
            elif game_status == 'Final' and currentperiod < 4:
                game_type = 'Regulation'
            elif game_status == 'Final' and currentperiod == 4:
                game_type = 'Overtime'
            elif game_status == 'Final' and currentperiod == 5:
                game_type = 'Shootout'
        except:
            game_type = ''
    
    ###
    ### NHL PLAY-BY-PLAY (HTM)
    ###
    
        ### trigger the files that will be read from and written to; write column titles to a header row
        with open(pbp_source, 'r') as HTM_pbp_source, open(pbp_outfile, 'w+', newline = '', encoding='utf-8') as HTM_pbp:
            
            if int(season_id) >= 20072008:
            
                csvWriter = csv.writer(HTM_pbp)
                
                if int(season_id) >= 20102011:
                    csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'SECONDS_GONE', 'TIME_LEFT', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
                elif int(season_id) <= 20092010:
                    csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'SECONDS_GONE', 'TIME_LEFT', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
                    
                csvRows = ([])
                
                ### create a BeautifulSoup object to parse the HTM pbp file
                pbpSoup = BeautifulSoup(HTM_pbp_source, 'html.parser')
            
                home_table = pbpSoup.find('table', id='Home')
                home_goals_row = home_table.find('td', attrs={'style':'font-size: 40px;font-weight:bold'})
                home_goals = int()
                for row in home_goals_row:
                    home_goals = row
            
                away_table = pbpSoup.find('table', id='Visitor')
                away_goals_row = away_table.find('td', attrs={'style':'font-size: 40px;font-weight:bold'})
                away_goals = int()
                for row in away_goals_row:
                    away_goals = row
            
                ### determine the home and away result
                home_result = str()
                away_result = str()

                if int(home_goals) > int(away_goals):
                    home_result = 'Win'
                    away_result = 'Loss'
                elif int(away_goals) > int(home_goals):
                    home_result = 'Loss'
                    away_result = 'Win'
            
                home_goals = int(0)
                away_goals = int(0)
                          
                ### 'zebra' striping of odd and even rows began in 2019 preseason
#                event_rows = pbpSoup.find_all('tr', attrs={'class':'evenColor'})
                event_rows = pbpSoup.find_all('tr', class_=['evenColor', 'oddColor'])
           
                ### loop through the event rows
                for row in range(len(event_rows)):
                    get_rows = event_rows[row]
                    get_tds = get_rows.find_all('td')

                    period = get_tds[1].string
            
                    time = get_tds[3].get_text()
                    time_index = time.find(':')
                    time_left = time[time_index+3:].replace('-', '')
                    time_gone = time[:time_index+3].replace('-', '')
               
                    convert_to_seconds = time_gone.split(':')
                    convert_minutes = int(convert_to_seconds[0]) * 60
                    convert_seconds = int(convert_to_seconds[1])
                    seconds_gone = convert_minutes + convert_seconds
                    if period == '1':
                        seconds_gone = seconds_gone
                    if period == '2':
                        seconds_gone = 1200 + seconds_gone
                    if period == '3':
                        seconds_gone = 2400 + seconds_gone
                    if period == '4':
                        seconds_gone = 3600 + seconds_gone
            
                    if period == '5':
                        seconds_gone = ''
                        time_left = ''
                        time_gone = ''
            
                    ### get the events and modify as needed
                    event = get_tds[4].string
            
                    if event == 'FAC':
                        event = 'Faceoff'
                    if event == 'GIVE':
                        event = 'Giveaway'
                    if event == 'HIT':
                        event = 'Hit'
                    if event == 'PEND':
                        event = 'Period.End'
                    if event == 'PENL':
                        event = 'Penalty'
                    if event == 'PSTR':
                        event = 'Period.Start'
                    if event == 'STOP':
                        event = 'Stoppage'
                    if event == 'TAKE':
                        event = 'Takeaway'

                    if event == 'GEND' or event == 'GOFF' or event == 'DELPEN':
                        continue

                    if seconds_gone == 0 and event == 'Stoppage':
                        continue

                    ### generate the shot event types
                    event_type = str()
                    if event == 'BLOCK':
                        event_type = 'Block'
                    if event == 'GOAL':
                        event_type = 'Goal'
                    if event == 'MISS':
                        event_type = 'Miss'
                    if event == 'SHOT':
                        event_type = 'Save'
            
                    ### change all references to a shot type in events to 'shot'
                    if event == 'BLOCK' or event == 'GOAL' or event == 'MISS' or event == 'SHOT':
                        event = 'Shot'
                                       
                    ### pull the description text
                    description = get_tds[5].get_text()
            
                    ### generate the stoppage event types and make modifications
                    if event == 'Stoppage':
                        event_type = description.replace(' ', '.')
                    if event_type == 'ICING':
                        event_type = 'Icing'
                    if event_type == 'OFFSIDE':
                        event_type = 'Offside'
                    if event_type == 'GOALIE.STOPPED':
                        event_type = 'Goalie'
                    if event == 'Stoppage' and event_type != 'Icing' and event_type != 'Offside' and event_type != 'Goalie':
                        event_type = ''
            
                    ### find the team credited with each registering each event
                    team = str()
                    try:
                        if event == 'Faceoff' or event == 'Giveaway' or event == 'Hit' or event == 'Penalty' or event == 'Shot' or event == 'Takeaway':
                            team = description[:3]
                            team = dict_teams.TRICODES[team]
                    except:
                        team = team
            
                    ### find the zone the event occurred in and generate home and away zone values
                    zone = str()
                    home_zone = str()
                    away_zone = str()
            
                    try:
                        if event == 'Faceoff' or event == 'Giveaway' or event == 'Hit' or event == 'Penalty' or event == 'Shot' or event == 'Takeaway':
                            zone = description
                            zone_index = description.find('Zone')
                            zone = zone[zone_index-5:]
                            zone = zone.split(' ')
                            zone = zone[0]
                        elif event == 'Period.End' or event == 'Period.Start' or event == 'Stoppage':
                            zone = ''
                    except:
                        zone = ''
            
                    if event_type == 'Block' and zone == 'Off.' and team == home:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Block' and zone == 'Def.' and team == home:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
                    elif event_type == 'Block' and zone == 'Off.' and team == away:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
                    elif event_type == 'Block' and zone == 'Def.' and team == away:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
            
                    if event_type == 'Faceoff' and zone == 'Off.' and team == home:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
                    elif event_type == 'Faceoff' and zone == 'Def.' and team == home:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Faceoff' and zone == 'Off.' and team == away:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Faceoff' and zone == 'Def.' and team == away:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
            
                    if event_type == 'Giveaway' and zone == 'Off.' and team == home:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
                    elif event_type == 'Giveaway' and zone == 'Def.' and team == home:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Giveaway' and zone == 'Off.' and team == away:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Giveaway' and zone == 'Def.' and team == away:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
            
                    if event_type == 'Goal' and zone == 'Off.' and team == home:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
                    elif event_type == 'Goal' and zone == 'Def.' and team == home:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Goal' and zone == 'Off.' and team == away:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Goal' and zone == 'Def.' and team == away:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
            
                    if event_type == 'Hit' and zone == 'Off.' and team == home:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
                    elif event_type == 'Hit' and zone == 'Def.' and team == home:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Hit' and zone == 'Off.' and team == away:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Hit' and zone == 'Def.' and team == away:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
            
                    if event_type == 'Miss' and zone == 'Off.' and team == home:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
                    elif event_type == 'Miss' and zone == 'Def.' and team == home:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Miss' and zone == 'Off.' and team == away:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Miss' and zone == 'Def.' and team == away:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
            
                    if event_type == 'Penalty' and zone == 'Off.' and team == home:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
                    elif event_type == 'Penalty' and zone == 'Def.' and team == home:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Penalty' and zone == 'Off.' and team == away:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Penalty' and zone == 'Def.' and team == away:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
            
                    if event_type == 'Save' and zone == 'Off.' and team == home:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
                    elif event_type == 'Save' and zone == 'Def.' and team == home:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Save' and zone == 'Off.' and team == away:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Save' and zone == 'Def.' and team == away:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
            
                    if event_type == 'Takeaway' and zone == 'Off.' and team == home:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
                    elif event_type == 'Takeaway' and zone == 'Def.' and team == home:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Takeaway' and zone == 'Off.' and team == away:
                        home_zone = 'Defensive'
                        away_zone = 'Offensive'
                    elif event_type == 'Takeaway' and zone == 'Def.' and team == away:
                        home_zone = 'Offensive'
                        away_zone = 'Defensive'
            
                    if zone == 'Neu.':
                        home_zone = 'Neutral'
                        away_zone = 'Neutral'
            
                    ### create and modify the detail for select events
                    event_detail = str()
                    try:
                        if event == 'Shot':
                            event_detail = description.split(',')
                            event_detail = event_detail[1].replace(' ', '')
                    except:
                        event_detail = ''
            
                    if event_detail == 'Deflected' or event_detail == 'Tip-In':
                            event_detail = 'Redirect'
                    
                    if event_detail == 'Wrap-around':
                        event_detail = 'Wraparound'
                    
                    try:
                        if event == 'Penalty':
                            event_type = description.split('\xa0')
                            event_type = event_type[1].replace(' (maj)', '')
                            event_type = event_type.split('(')
                            event_type = event_type[1].split(' ')
                            event_type = event_type[0].replace('2', 'Minor').replace('4', 'Double.Minor').replace('5', 'Major').replace('10', 'Misconduct')
                    except:
                        pass
            
                    try:
                        if event == 'Penalty':
                            event_detail = description.split('\xa0')
                            event_detail = event_detail[1].replace(' (maj)', '')
                            event_detail = event_detail.split('(')
                            event_detail = event_detail[0]
                            event_detail = dict_penalties.PENALTIES[event_detail]
                    except:
                        pass
            
                    ### get the player who was credited either with taking a shot, winning a faceoff, delivering a hit, giving up / taking away the puck or committing a penalty
                    player_A = str()
                    if int(season_id) == 20072008:
                        try:
                            if event == 'Giveaway' or event == 'Hit' or event == 'Penalty' or event == 'Takeaway':
                                player_A = description.split('#')
                                player_A = player_A[1][:2]
                            elif event == 'Shot' and event_type != 'Save':
                                player_A = description.split('#')
                                player_A = player_A[1][:2]
                            elif event == 'Shot' and event_type == 'Save':                                
                                player_A = description.split(' - ')
                                player_A = player_A[1][:2]
                            elif event == 'Faceoff' and team == away:
                                player_A = description.split('#')
                                player_A = player_A[1][:2]
                            elif event == 'Faceoff' and team == home:
                                player_A = description.split('#')
                                player_A = player_A[2][:2]
                            elif event == 'Period.End' or event == 'Period.Start' or event == 'Stoppage':
                                player_A = ''
                        except:
                            player_A = ''

                    if int(season_id) >= 20082009:
                        try:
                            if event == 'Giveaway' or event == 'Hit' or event == 'Penalty' or event == 'Shot' or event == 'Takeaway':
                                player_A = description.split('#')
                                player_A = player_A[1][:2]
                            elif event == 'Faceoff' and team == away:
                                player_A = description.split('#')
                                player_A = player_A[1][:2]
                            elif event == 'Faceoff' and team == home:
                                player_A = description.split('#')
                                player_A = player_A[2][:2]
                            elif event == 'Period.End' or event == 'Period.Start' or event == 'Stoppage':
                                player_A = ''
                        except:
                            player_A = ''

                    try:
                        if team == home and player_A != '':
                            player_A = homeROS_dict[int(player_A)][0]
                    except:
                        player_A = player_A
                    try:
                        if team == home and player_A != '':
                            player_A = awayROS_dict[int(player_A)][0]
                            team = away
                    except:
                        player_A = player_A
            
                    try:
                        if team == away and player_A != '':
                            player_A = awayROS_dict[int(player_A)][0]
                    except:
                        player_A = player_A
                    try:
                        if team == home and player_A != '':
                            player_A = homeROS_dict[int(player_A)][0]
                            team = home
                    except:
                        player_A = player_A
            
                    ### get the player who was credited either with a primary assist on a goal, blocking a shot, losing a faceoff, taking a hit or drawing a penalty
                    player_B = str()
                    try:
                        if event_type == 'Block' and team == away:
                            player_B = description.split('#')
                            player_B = player_B[2][:2]
                            player_B = homeROS_dict[int(player_B)][0]
                        elif event_type == 'Block' and team == home:
                            player_B = description.split('#')
                            player_B = player_B[2][:2]
                            player_B = awayROS_dict[int(player_B)][0]
                        elif event_type == 'Goal' and team == away:
                            player_B = description.split('#')
                            player_B = player_B[2][:2]
                            player_B = awayROS_dict[int(player_B)][0]
                        elif event_type == 'Goal' and team == home:
                            player_B = description.split('#')
                            player_B = player_B[2][:2]
                            player_B = homeROS_dict[int(player_B)][0]
                        elif event == 'Faceoff' and team == away:
                            player_B = description.split('#')
                            player_B = player_B[2][:2]
                            player_B = homeROS_dict[int(player_B)][0]
                        elif event == 'Faceoff' and team == home:
                            player_B = description.split('#')
                            player_B = player_B[1][:2]
                            player_B = awayROS_dict[int(player_B)][0]
                        elif event == 'Hit' and team == away:
                            player_B = description.split('#')
                            player_B = player_B[2][:2]
                            player_B = homeROS_dict[int(player_B)][0]
                        elif event == 'Hit' and team == home:
                            player_B = description.split('#')
                            player_B = player_B[2][:2]
                            player_B = awayROS_dict[int(player_B)][0]
                        elif event == 'Penalty' and team == away:
                            player_B = description.split('#')
                            player_B = player_B[2][:2]
                            player_B = homeROS_dict[int(player_B)][0]
                        elif event == 'Penalty' and team == home:
                            player_B = description.split('#')
                            player_B = player_B[2][:2]
                            player_B = awayROS_dict[int(player_B)][0]
                        elif event == 'Period.End' or event == 'Period.Start' or event == 'Stoppage':
                            player_B = ''
                    except:
                        player_B = ''
            
                    ### get the player who was credited either with a primary assist on a goal, blocking a shot, losing a faceoff, taking a hit or drawing a penalty
                    player_C = str()
                    try:
                        if event_type == 'Goal' and team == home:
                            player_C = description.split('#')
                            player_C = player_C[3][:2]
                            player_C = homeROS_dict[int(player_C)][0]
                        if event_type == 'Goal' and team == away:
                            player_C = description.split('#')
                            player_C = player_C[3][:2]
                            player_C = awayROS_dict[int(player_C)][0]
                        elif event == 'Period.End' or event == 'Period.Start' or event == 'Stoppage':
                            player_C = ''
                    except:
                        player_C = ''
            
                    ### get the number of goals scored by the home and away team
                    if period != '5' and event_type == 'Goal' and team == home:
                        home_goals += 1
            
                    if period != '5' and event_type == 'Goal' and team == away:
                        away_goals += 1
            
                    if period == '5':
                        home_goals = ''
                        away_goals = ''
            
                    # split the combined score state into distinct home and away goals scored differentials
                    home_scorediff = ''
                    away_scorediff = ''
            
                    if period != '5':
                        home_scorediff = int(home_goals) - int(away_goals)
                        away_scorediff = int(away_goals) - int(home_goals)
            
                    if period != '5' and event_type == 'Goal' and team == home:
                        home_scorediff = home_scorediff - 1
                        away_scorediff = away_scorediff + 1
            
                    if period != '5' and event_type == 'Goal' and team == away:
                        home_scorediff = home_scorediff + 1
                        away_scorediff = away_scorediff - 1
            
                    # determine the home and away score situations
                    if period != '5' and int(home_scorediff) == int(away_scorediff):
                        home_situation = 'Tied'
                        away_situation = 'Tied'
                    elif period != '5' and int(home_scorediff) > int(away_scorediff):
                        home_situation = 'Leading'
                        away_situation = 'Trailing'
                    elif period != '5' and int(home_scorediff) < int(away_scorediff):
                        home_situation = 'Trailing'
                        away_situation = 'Leading'
            
                    ### find all the rows with on-ice player information
                    get_players = get_rows.find_all('font')
            
                    ### formats the home players on-ice
                    try:
                        homeON_1 = get_players[6]['title'].replace(' ', '', 2).split('-', 1)
                        homeON_1 = homeON_1[1].replace(' ', '.')
                        if homeON_1[0] == '.':
                            homeON_1 = homeON_1.replace('.', '', 1)
                    except:
                        homeON_1 = ''
                    try:
                        homeON_1 = dict_names.NAMES[homeON_1]
                    except:
                        homeON_1 = homeON_1
            
                    try:
                        homeON_2 = get_players[7]['title'].replace(' ', '', 2).split('-', 1)
                        homeON_2 = homeON_2[1].replace(' ', '.')
                        if homeON_2[0] == '.':
                            homeON_2 = homeON_2.replace('.', '', 1)
                    except:
                        homeON_2 = ''
                    try:
                        homeON_2 = dict_names.NAMES[homeON_2]
                    except:
                        homeON_2 = homeON_2
            
                    try:
                        homeON_3 = get_players[8]['title'].replace(' ', '', 2).split('-', 1)
                        homeON_3 = homeON_3[1].replace(' ', '.')
                        if homeON_3[0] == '.':
                            homeON_3 = homeON_3.replace('.', '', 1)
                    except:
                        homeON_3 = ''
                    try:
                        homeON_3 = dict_names.NAMES[homeON_3]
                    except:
                        homeON_3 = homeON_3
            
                    try:
                        homeON_4 = get_players[9]['title'].replace(' ', '', 2).split('-', 1)
                        homeON_4 = homeON_4[1].replace(' ', '.')
                        if homeON_4[0] == '.':
                            homeON_4 = homeON_4.replace('.', '', 1)
                    except:
                        homeON_4 = ''
                    try:
                        homeON_4 = dict_names.NAMES[homeON_4]
                    except:
                        homeON_4 = homeON_4
            
                    try:
                        homeON_5 = get_players[10]['title'].replace(' ', '', 2).split('-', 1)
                        homeON_5 = homeON_5[1].replace(' ', '.')
                        if homeON_5[0] == '.':
                            homeON_5 = homeON_5.replace('.', '', 1)
                    except:
                        homeON_5 = ''
                    try:
                        homeON_5 = dict_names.NAMES[homeON_5]
                    except:
                        homeON_5 = homeON_5
            
                    try:
                        homeON_6 = get_players[11]['title'].replace(' ', '', 2).split('-', 1)
                        homeON_6 = homeON_6[1].replace(' ', '.')
                        if homeON_6[0] == '.':
                            homeON_6 = homeON_6.replace('.', '', 1)
                    except:
                        homeON_6 = ''
                    try:
                        homeON_6 = dict_names.NAMES[homeON_6]
                    except:
                        homeON_6 = homeON_6
            
            
                    homeON = [homeON_1, homeON_2, homeON_3, homeON_4, homeON_5, homeON_6]
            
                    ### format the away players on-ice
                    try:
                        awayON_1 = get_players[0]['title'].replace(' ', '', 2).split('-', 1)
                        awayON_1 = awayON_1[1].replace(' ', '.')
                        if awayON_1[0] == '.':
                            awayON_1 = awayON_1.replace('.', '', 1)
                    except:
                        awayON_1 = ''
                    try:
                        awayON_1 = dict_names.NAMES[awayON_1]
                    except:
                        awayON_1 = awayON_1
            
                    try:
                        awayON_2 = get_players[1]['title'].replace(' ', '', 2).split('-', 1)
                        awayON_2 = awayON_2[1].replace(' ', '.')
                        if awayON_2[0] == '.':
                            awayON_2 = awayON_2.replace('.', '', 1)
                    except:
                        awayON_2 = ''
                    try:
                        awayON_2 = dict_names.NAMES[awayON_2]
                    except:
                        awayON_2 = awayON_2
            
                    try:
                        awayON_3 = get_players[2]['title'].replace(' ', '', 2).split('-', 1)
                        awayON_3 = awayON_3[1].replace(' ', '.')
                        if awayON_3[0] == '.':
                            awayON_3 = awayON_3.replace('.', '', 1)
                    except:
                        awayON_3 = ''
                    try:
                        awayON_3 = dict_names.NAMES[awayON_3]
                    except:
                        awayON_3 = awayON_3
            
                    try:
                        awayON_4 = get_players[3]['title'].replace(' ', '', 2).split('-', 1)
                        awayON_4 = awayON_4[1].replace(' ', '.')
                        if awayON_4[0] == '.':
                            awayON_4 = awayON_4.replace('.', '', 1)
                    except:
                        awayON_4 = ''
                    try:
                        awayON_4 = dict_names.NAMES[awayON_4]
                    except:
                        awayON_4 = awayON_4
            
                    try:
                        awayON_5 = get_players[4]['title'].replace(' ', '', 2).split('-', 1)
                        awayON_5 = awayON_5[1].replace(' ', '.')
                        if awayON_5[0] == '.':
                            awayON_5 = awayON_5.replace('.', '', 1)
                    except:
                        awayON_5 = ''
                    try:
                        awayON_5 = dict_names.NAMES[awayON_5]
                    except:
                        awayON_5 = awayON_5
            
                    try:
                        awayON_6 = get_players[5]['title'].replace(' ', '', 2).split('-', 1)
                        awayON_6 = awayON_6[1].replace(' ', '.')
                        if awayON_6[0] == '.':
                            awayON_6 = awayON_6.replace('.', '', 1)
                    except:
                        awayON_6 = ''
                    try:
                        awayON_6 = dict_names.NAMES[awayON_6]
                    except:
                        awayON_6 = awayON_6
            
                    awayON = [awayON_1, awayON_2, awayON_3, awayON_4, awayON_5, awayON_6]
            
                    ### count the number of players on each side excluding goaltenders to determine each team's strength they are playing under
                    home_skaters = 0
                    home_goalie = 0
            
                    away_skaters = 0
                    away_goalie = 0
            
                    for player in homeON:
                        if player != homeG[0] and player != homeG[1] and player != '' and player not in awayROS_list:
                            home_skaters += 1
                        if player in awayROS_list:
                            away_skaters += 1
                        if player == homeG[0] or player == homeG[1]:
                            home_goalie += 1
            
                    for player in awayON:
                        if player != awayG[0] and player != awayG[1] and player != '' and player not in homeROS_list:
                            away_skaters += 1
                        if player in homeROS_list:
                            home_skaters += 1
                        if player == awayG[0] or player == awayG[1]:
                            away_goalie += 1
            
                    home_strength = str(home_skaters) + 'v' + str(away_skaters)
                    away_strength = str(away_skaters) + 'v' + str(home_skaters)
            
                    if period == '5' and team == away:
                        home_strength = '0v1'
                        away_strength = '1v0'
                    elif period == '5' and team == away:
                        home_strength = '1v0'
                        away_strength = '0v1'
            
                    ### use each team's number of skaters to determine the home and away state of play
                    home_compare = home_strength.split('v')[0]
                    away_compare = away_strength.split('v')[0]
                    home_state = ()
                    away_state = ()
            
                    if int(home_compare) == int(away_compare):
                        home_state = 'EV'
                        away_state = 'EV'
                    elif int(home_compare) > int(away_compare):
                        home_state = 'PP'
                        away_state = 'SH'
                    elif int(home_compare) < int(away_compare):
                        home_state = 'SH'
                        away_state = 'PP'
            
                    if home_goalie == 0 or away_goalie == 0:
                        home_state = 'EN'
                        away_state = 'EN'
            
                    if period == '5':
                        home_state = 'SO'
                        away_state = 'SO'
                    
                    home_zone = ''
                    away_zone = ''
                    
                    ### create a tuple of the information to be written and add to csvRows
                    if int(season_id) >= 20102011:
                        pbpTup = [(season_id, game_id, date, home, away, game_type, home_result, away_result, period, seconds_gone, time_left, time_gone, home_goals, away_goals, home_situation, away_situation, home_scorediff, away_scorediff, home_strength, away_strength, home_state, away_state, event, event_type, event_detail, team, player_A, player_B, player_C, homeON_1, homeON_2, homeON_3, homeON_4, homeON_5, homeON_6, awayON_1, awayON_2, awayON_3, awayON_4, awayON_5, awayON_6)]
                    elif int(season_id) <= 20092010:
                        pbpTup = [(season_id, game_id, date, home, away, game_type, home_result, away_result, period, seconds_gone, time_left, time_gone, home_goals, away_goals, home_situation, away_situation, home_scorediff, away_scorediff, home_strength, away_strength, home_state, away_state, event, event_type, event_detail, home_zone, away_zone, team, player_A, player_B, player_C, homeON_1, homeON_2, homeON_3, homeON_4, homeON_5, homeON_6, awayON_1, awayON_2, awayON_3, awayON_4, awayON_5, awayON_6)]
                    
                    csvRows += pbpTup
           
                ### write the rows to file
                csvWriter.writerows(csvRows)
            
                ### reload the newly minted csv file for some final touches in pandas
                pbp_df = pd.read_csv(pbp_outfile)
               
                ### delete rows with botched names
                pbp_df = pbp_df[(pbp_df.EVENT != 'PGEND') & (pbp_df.EVENT != 'PGSTR') & (pbp_df.EVENT != 'ANTHEM') & (pbp_df.EVENT != 'GEND') & (pbp_df.EVENT != 'SOC')]
                
                ### return the home goals or away goals to whatever the value was prior to when whichever team scores
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.TEAM == home), ['HOME_GOALS']] = pbp_df['HOME_GOALS'] - 1; pbp_df
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.TEAM == away), ['AWAY_GOALS']] = pbp_df['AWAY_GOALS'] - 1; pbp_df
                
                ### clean up instances where home players are listed in away player on-ice columns
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_6 == player), ['HOMEON_6']] = pbp_df['HOMEON_5']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_6 == player), ['HOMEON_5']] = pbp_df['HOMEON_4']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_6 == player), ['HOMEON_4']] = pbp_df['HOMEON_3']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_6 == player), ['HOMEON_3']] = pbp_df['HOMEON_2']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_6 == player), ['HOMEON_2']] = pbp_df['HOMEON_1']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_6 == player), ['HOMEON_1']] = pbp_df['AWAYON_6']; pbp_df
                
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_5 == player), ['HOMEON_6']] = pbp_df['HOMEON_5']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_5 == player), ['HOMEON_5']] = pbp_df['HOMEON_4']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_5 == player), ['HOMEON_4']] = pbp_df['HOMEON_3']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_5 == player), ['HOMEON_3']] = pbp_df['HOMEON_2']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_5 == player), ['HOMEON_2']] = pbp_df['HOMEON_1']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_5 == player), ['HOMEON_1']] = pbp_df['AWAYON_5']; pbp_df
                
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_4 == player), ['HOMEON_6']] = pbp_df['HOMEON_5']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_4 == player), ['HOMEON_5']] = pbp_df['HOMEON_4']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_4 == player), ['HOMEON_4']] = pbp_df['HOMEON_3']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_4 == player), ['HOMEON_3']] = pbp_df['HOMEON_2']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_4 == player), ['HOMEON_2']] = pbp_df['HOMEON_1']; pbp_df
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_4 == player), ['HOMEON_1']] = pbp_df['AWAYON_4']; pbp_df
                
                for player in homeROS_list:
                    pbp_df.loc[(pbp_df.AWAYON_4 == player), ['AWAYON_4']] = ''; pbp_df
                    pbp_df.loc[(pbp_df.AWAYON_5 == player), ['AWAYON_5']] = ''; pbp_df
                    pbp_df.loc[(pbp_df.AWAYON_6 == player), ['AWAYON_6']] = ''; pbp_df
                
                if game_status != 'Final' and currentperiod == 5:
                    for player in homeG:
                        pbp_df.loc[(pbp_df.AWAYON_2 == player) & (pbp_df.PERIOD == 5), ['HOMEON_1']] = player; pbp_df
                        pbp_df.loc[(pbp_df.AWAYON_2 == player) & (pbp_df.PERIOD == 5), ['AWAYON_2']] = ''; pbp_df
                elif game_status == 'Final' and currentperiod == 5:
                    for player in homeG:
                        pbp_df.loc[(pbp_df.AWAYON_2 == player) & (pbp_df.PERIOD == 5), ['HOMEON_1']] = player; pbp_df
                        pbp_df.loc[(pbp_df.AWAYON_2 == player) & (pbp_df.PERIOD == 5), ['AWAYON_2']] = ''; pbp_df
                
                ### save the adjusted csv file
                pbp_df.to_csv(pbp_outfile, index=False)
                
            if int(season_id) == 20062007:

                csvWriter = csv.writer(HTM_pbp, lineterminator='\n')     
                csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'SECONDS_GONE', 'TIME_LEFT', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE', 'HOME_STATE_DETAIL', 'AWAY_STATE_DETAIL', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6\r'])
           
                csvRows = ([])
                
                ### create a BeautifulSoup object to parse the HTM pbp file
                pbp_soup = BeautifulSoup(HTM_pbp_source, 'html.parser')

                ### filter for each team's goals scored as well as the play-by-play events; extract and format the text                                        
                pbp_table = pbp_soup.select('table')[1]

                goals_table = pbp_soup.select('table')[0]
                away_goals_td = goals_table.find_all('td')[1]
                away_goals = away_goals_td.find('font').get_text().strip()
                home_goals_td = goals_table.find_all('td')[5]
                home_goals = home_goals_td.find('font').get_text().strip() 
                
                ### determine the home and away result
                home_result = str()
                away_result = str()
                
                if int(home_goals) > int(away_goals):
                    home_result = 'Win'
                    away_result = 'Loss'
                elif int(away_goals) > int(home_goals):
                    home_result = 'Loss'
                    away_result = 'Win' 

                pbp_td = pbp_table.find('td')

                pbp_text = pbp_td.get_text().strip()

                pbp_text = pbp_text.replace('         ', '_').replace('        ', '_').replace('       ', '_').replace('      ', '_').replace('     ', '_').replace('    ', '_').replace('   ', '_').replace('  ', '_').replace(' ', '_')
                pbp_text = pbp_text.replace('#', '')
                pbp_text = pbp_text.replace(',', '')
                pbp_text = pbp_text.replace('_Shootout_', '-')
                pbp_text = pbp_text.replace('------------------------------------------', '_').replace('-----_', '_').replace('---', '--_').replace('_-_', '').replace('------', '--')
                pbp_text = pbp_text.replace('____', '_').replace('___', '_').replace('__', '_')
                pbp_text = pbp_text.replace('_(*)', '').replace('_(!)', '').replace('N/A', '').replace('_vs_', '_')
                pbp_text = pbp_text.replace('wondefensive_zone.', 'Defensive').replace('wonoffensive_zone.', 'Offensive').replace('wonneutral_zone.', 'Neutral')
                pbp_text = pbp_text.replace('FACE-OFF', 'Faceoff_$_$').replace('BLOCKED_SHOT', 'Shot_Block_$').replace('GIVEAWAY', 'Giveaway_$_$').replace('_GOALIE_', '_$_Empty-Net_$_').replace('GOAL', 'Shot_Goal_$').replace('_HIT_', '_Hit_$_$_').replace('MISSED_SHOT', 'Shot_Miss_$').replace('PENALTY', 'Penalty_$_$').replace('SHOT', 'Shot_Save_$').replace('STOPPAGE', 'Stoppage').replace('TAKEAWAY', 'Takeaway_$_$')
                pbp_text = pbp_text.replace('Goalie_Stopped', 'Goalie_$_$').replace('Hand_Pass', '$_$_$').replace('Ice_Problem', '$_$_$').replace('Icing', 'Icing_$_$').replace('Net_off_mooring', '$_$_$').replace('Net_off_Mooring', '$_$_$').replace('Net_off_moorings', '$_$_$').replace('Net_off_Moorings', '$_$_$').replace('Net_off_post', '$_$_$').replace('Net_off_Post', '$_$_$').replace('Offside', 'Offside_$_$').replace('Puck_in_Benches', '$_$_$').replace('Puck_in_Crowd', '$_$_$').replace('Puck_in_Netting', '$_$_$').replace('Puck_Frozen', '$_$_$').replace('Referee_or_Linesman', '$_$_$').replace('Rink_Repair', '$_$_$').replace('Time_OutAway', 'Timeout_$_$').replace('Time_OutHome', 'Timeout_$_$').replace('Time_OutVisitor', 'Timeout_$_$')
                pbp_text = pbp_text.replace('_A:_', '_')
                pbp_text = pbp_text.replace('_L.A', '_LAK').replace('_N.J', '_NJD').replace('_S.J', '_SJS').replace('_T.B', '_TBL')
                pbp_text = pbp_text.replace('_' + away + ':', '_$_$_$_Shot_Goal_$_' + away + '_$_$_$_$_$_$_$_$_$_$')
                pbp_text = pbp_text.replace('_' + home + ':', '_$_$_$_Shot_Goal_$_' + home + '_$_$_$_$_$_$_$_$_$_$')
                pbp_text = pbp_text.replace('$_'+ away, '$_' + away + '_').replace('$_'+ home, '$_' + home + '_')
                pbp_text = pbp_text.replace('_' + away + '__', '_' + away + '_').replace('_' + home + '__', '_' + home + '_')
                pbp_text = pbp_text.replace('_ST._', '_ST.').replace('_DE_VRIES', '_DE.VRIES').replace('_MEYER_IV', '_MEYER.IV').replace('_VAN_RYN', '_VAN.RYN')
                
                pbp_text = pbp_text.replace('2_min_', 'Minor_').replace('4_min_', 'Double-Minor_').replace('5_min_', 'Major_').replace('_(10_min)_10_min', '_10-minute').replace('_10_min', '_10-minute').replace('Game_Misconduct_', 'Misconduct_Game').replace('Match_Penalty', 'Misconduct_Game')
                pbp_text = pbp_text.replace('Abuse_of_officialsbench', 'Abuse of officials').replace('Abuse_of_officialsBench', 'Abuse of officials').replace('Abuse_of_Officialsbench', 'Abuse of Officials').replace('Abuse_of_OfficialsBench', 'Abuse of Officials').replace('Abusive_languagebench', 'Abusive language').replace('Abusive_languageBench', 'Abusive language').replace('Broken_stick', 'Broken stick').replace('Broken_Stick', 'Broken Stick').replace('Closing_hand_on_puck', 'Delay of game').replace('Cross_checking', 'Cross-checking').replace('Delaying_Game-Ill._play_goalie', 'Delay of Game').replace('Delaying_Game-Puck_over_glass', 'Delay of Game').replace('Delay_of_game', 'Delay of Game').replace('Delay_of_Game', 'Delay of Game').replace('Delaying_Game-Smothering_puck', 'Delay of game').replace('Delaying_the_game', 'Delay of game').replace('Delaying_the_Game', 'Delay of Game').replace('Game_misconduct', 'Game misconduct').replace('Game_misconduct', 'Game Misconduct').replace('High_Stick', 'High.Stick').replace('Holding_the_Stick', 'Holding').replace('Holding_the_stick', 'Holding').replace('InstigatorMisconduct_10_min', 'Misconduct_10-minute').replace('Interferencegoalkeeper', 'Goalie interference').replace('InterferenceGoalkeeper', 'Goalie interference').replace('Too_many_men/icebench', 'Too many men').replace('Unsportsmanlike_Conduct', 'Unsportsmanlike Conduct').replace('Unsportsmanlike_conduct', 'Unsportsmanlike conduct')
                pbp_text = pbp_text.replace('_(maj)', '')

                pbp_text = pbp_text.replace('\n\n', '</font>\n<font>')
              
                pbp_text = pbp_text.replace('<font></font>', '')
                pbp_text = pbp_text.replace('</font>', '$', 1)
                pbp_text = pbp_text.replace('</font>', '$', 1)
                pbp_text = pbp_text.replace('<font>_SO_', '<font>_$_5_$_')
                pbp_text = pbp_text.replace('_--</font>', '_--')
                pbp_text = pbp_text.replace('_Per_Time_Event_Team_Type_Description', '').replace('__$', '_$')
                pbp_text = pbp_text.replace('_Unassisted', '_$_$_$_$')
                
                pbp_text = pbp_text.replace('<font>', '$', 1).replace('<font>_--', '_--').replace('_--', '')
                pbp_text = pbp_text.replace('_</font>', '</font>')

                pbp_text = pbp_text.replace('<font>_', '<font>')

                ### combine the text with html tags; write the reformatted text and html additions to file
                pbp_html = '<html>\n<head>\n</head>\n<body>\n<table>\n<tr>\n<td>\n' + pbp_text + '</td>\n</td>\n</tr>\n</table>\n</body>\n</html>'
                pbp_html = pbp_html.replace('</td>', '</font>', 1).replace('<font></font>', '')
                pbp_html = pbp_html.replace('$\n$$\n<font>', '<font>')
                
                pbp_html = pbp_html.replace('<td>\n$\n$\n$\n\n', '<td>\n')
                
                pbp_html = pbp_html.replace('<font>\n</font>\n</td>', '</td>')
                
                pbp_soup = BeautifulSoup(pbp_html, 'html.parser')
               
                ### filter for the play-by-play events; extract and format the text
                pbp_table = pbp_soup.select('table')
                pbp_font = pbp_soup.find_all('font')

                home_goals = int(0)
                away_goals = int(0)

                ### loop through and pull specific event information from each font tag
                for i in pbp_font:                 
                    pbp_events = i.get_text()

                    pbp_events = pbp_events.split('_')

                    period = int()
                    try:
                        period = int(pbp_events[1])
                    except:
                        pass
                    
                    time_gone = pbp_events[2]
                    try:
                        time_gone_minutes = int(time_gone.split(':')[0])
                        time_gone_seconds = int(time_gone.split(':')[1])                       
                        if time_gone_minutes < 10:
                            time_gone = time_gone_minutes[1] + ':' + time_gone_seconds
                        elif time_gone_minutes >= 10:
                            time_gone = time_gone_minutes + ':' + time_gone_seconds
                    except:
                        time_gone = time_gone

                    seconds_gone = int()
                    try:                            
                        convert_to_seconds = time_gone.split(':')
                        convert_minutes = int(convert_to_seconds[0]) * 60
                        convert_seconds = int(convert_to_seconds[1])
                        seconds_gone = convert_minutes + convert_seconds
                    except:
                        seconds_gone = '$'

                    if period == 1:
                        seconds_gone = seconds_gone
                    if period == 2:
                        seconds_gone = 1200 + seconds_gone
                    if period == 3:
                        seconds_gone = 2400 + seconds_gone
                    if period == 4:
                        seconds_gone = 3600 + seconds_gone

                    try:
                        if period < 4 and time_gone_minutes < 20 and time_gone_seconds < 51:
                            time_left_minutes = 19 - time_gone_minutes
                            time_left_seconds = 60 - time_gone_seconds
                            time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
                        elif period < 4 and time_gone_minutes < 20 and time_gone_seconds > 50:
                            time_left_minutes = 19 - time_gone_minutes
                            time_left_seconds = 60 - time_gone_seconds
                            time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)
                        elif period < 4 and time_gone_minutes == 20 and time_gone_seconds < 51:
                            time_left_minutes = 20 - time_gone_minutes
                            time_left_seconds = 60 - time_gone_seconds
                            time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
                        elif period < 4 and time_gone_minutes == 20 and time_gone_seconds > 50:
                            time_left_minutes = 20 - time_gone_minutes
                            time_left_seconds = 60 - time_gone_seconds
                            time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)
                    except:
                        pass

                    if period == 4 and time_gone_minutes < 5 and time_gone_seconds < 51:
                        time_left_minutes = 4 - time_gone_minutes
                        time_left_seconds = 60 - time_gone_seconds
                        time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
                    elif period == 4 and time_gone_minutes < 5 and time_gone_seconds > 50:
                        time_left_minutes = 4 - time_gone_minutes
                        time_left_seconds = 60 - time_gone_seconds
                        time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)
                    elif period == 4 and time_gone_minutes == 5 and time_gone_seconds < 51:
                        time_left_minutes = 5 - time_gone_minutes
                        time_left_seconds = 60 - time_gone_seconds
                        time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
                    elif period == 4 and time_gone_minutes == 5 and time_gone_seconds > 50:
                        time_left_minutes = 5 - time_gone_minutes
                        time_left_seconds = 60 - time_gone_seconds
                        time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)

                    if time_gone == '00:00' and period < 4:
                        time_left = '20:00'
                    if time_gone == '00:00' and period == 4:
                        time_left = '5:00'
                    if time_gone == '01:00' and period < 4:
                        time_left = '19:00'
                    if time_gone == '01:00' and period == 4:
                        time_left = '4:00'                        
                    if time_gone == '02:00' and period < 4:
                        time_left = '18:00'
                    if time_gone == '02:00' and period == 4:
                        time_left = '3:00'                        
                    if time_gone == '03:00' and period < 4:
                        time_left = '17:00'
                    if time_gone == '03:00' and period == 4:
                        time_left = '12:00'
                    if time_gone == '04:00' and period < 4:
                        time_left = '16:00'
                    if time_gone == '04:00' and period == 4:
                        time_left = '1:00'
                    if time_gone == '05:00' and period < 4:
                        time_left = '15:00'
                    if time_gone == '05:00' and period == 4:
                        time_left = '0:00'
                    if time_gone == '06:00':
                        time_left = '14:00'
                    if time_gone == '07:00':
                        time_left = '13:00'
                    if time_gone == '08:00':
                        time_left = '12:00'
                    if time_gone == '09:00':
                        time_left = '11:00'
                    if time_gone == '10:00':
                        time_left = '10:00'
                    if time_gone == '11:00':
                        time_left = '9:00'
                    if time_gone == '12:00':
                        time_left = '8:00'
                    if time_gone == '13:00':
                        time_left = '7:00'
                    if time_gone == '14:00':
                        time_left = '6:00'
                    if time_gone == '15:00':
                        time_left = '5:00'
                    if time_gone == '16:00':
                        time_left = '4:00'
                    if time_gone == '17:00':
                        time_left = '3:00'
                    if time_gone == '18:00':
                        time_left = '2:00'
                    if time_gone == '19:00':
                        time_left = '1:00'
                    if time_gone == '20:00':
                        time_left = '0:00'                      
                    
                    if period == 5:
                        seconds_gone = '$'
                        time_left = '$'
                        time_gone = '$'

                    home_result = home_result
                    away_result = away_result

                    event = pbp_events[3]
                    event_type = pbp_events[4]
                    event_detail = '$'
                    try:
                        event_detail = pbp_events[5]
                    except:
                        event_detail = event_detail
                    
                    try:
                        team = pbp_events[6]
                    except:
                        team = '$'
                        
                    home_zone = '$'
                    away_zone = '$'
                    
                    if event == 'Faceoff' and team == away:
                        away_zone = pbp_events[7]
                        if away_zone == 'Defensive':
                            home_zone = 'Offensive'
                        elif away_zone == 'Neutral':
                            home_zone = 'Neutral'
                        elif away_zone == 'Offensive':
                            home_zone = 'Defensive'
                    elif event == 'Faceoff' and team == home:
                        home_zone = pbp_events[7]
                        if home_zone == 'Defensive':
                            away_zone = 'Offensive'
                        elif home_zone == 'Neutral':
                            away_zone = 'Neutral'
                        elif home_zone == 'Offensive':
                            away_zone = 'Defensive'                       
                    
                    player_A_no = '$'
                    player_A = '$'
                    player_B_no = '$'
                    player_B = '$'
                    player_C_no = '$'
                    player_C = '$'

                    if event == 'Faceoff' and team == away:
                        player_A_no = pbp_events[9]
                        player_A = awayROS_dict[int(player_A_no)][0]
                        player_B_no = pbp_events[12]
                        player_B = homeROS_dict[int(player_B_no)][0]
                    elif event == 'Faceoff' and team == home:
                        player_A_no = pbp_events[12]
                        player_A = homeROS_dict[int(player_A_no)][0]
                        player_B_no = pbp_events[9]
                        player_B = awayROS_dict[int(player_B_no)][0]
                            
                    if period < 5 and event == 'Shot' and event_type != 'Block' and team == away:
                        try:
                            player_A_no = pbp_events[8]
                            player_A = awayROS_dict[int(player_A_no)][0]
                        except:
                            player_A_no = '$'
                            player_A = '$'                    
                    elif period < 5 and event == 'Shot' and event_type != 'Block' and team == home:
                        try:
                            player_A_no = pbp_events[8]
                            player_A = homeROS_dict[int(player_A_no)][0]
                        except:
                            player_A_no = '$'
                            player_A = '$' 

                    if period == 5 and event == 'Shot' and team == away:
                        try:
                            player_A_no = pbp_events[7]
                            player_A = awayROS_dict[int(player_A_no)][0]
                        except:
                            player_A_no = '$'
                            player_A = '$'
                        try:
                            if event_type != 'Miss':
                                event_detail = pbp_events[9] 
                        except:
                            event_detail = '$'
                    elif period == 5 and event == 'Shot' and team == home:
                        try:
                            player_A_no = pbp_events[7]
                            player_A = homeROS_dict[int(player_A_no)][0]
                        except:
                            player_A_no = '$'
                            player_A = '$'
                        try:
                            if event_type != 'Miss':
                                event_detail = pbp_events[9] 
                        except:
                            event_detail = '$'

                    if period < 5 and event == 'Shot' and event_type == 'Block' and team == away:
                        team = home
                        player_A_no = '$'
                        player_A = '$'
                        try:
                            player_B_no = pbp_events[8]
                            player_B = awayROS_dict[int(player_B_no)][0]
                        except:
                            player_B_no = '$'
                            player_B = '$'
                    elif period < 5 and event == 'Shot' and event_type == 'Block' and team == home:
                        team = away
                        player_A_no = '$'
                        player_A = '$'
                        try:
                            player_B_no = pbp_events[8]
                            player_B = homeROS_dict[int(player_B_no)][0]
                        except:
                            player_B_no = '$'
                            player_B = '$' 
                        
                    if period < 5 and event_type == 'Goal' and team == away:
                        try:
                            player_B_no = pbp_events[10]
                            player_B = awayROS_dict[int(player_B_no)][0]
                        except:
                            player_B_no = '$'
                            player_B = '$'
                        try:
                            player_C_no = pbp_events[12]
                            player_C = awayROS_dict[int(player_C_no)][0]
                        except:
                            player_C_no = '$'
                            player_C = '$'
                        try:
                            if pbp_events[16] == 'Backhand' or pbp_events[16] == 'Redirect' or pbp_events[16] == 'Slap' or pbp_events[16] == 'Snap' or pbp_events[16] == 'Wraparound' or pbp_events[16] == 'Wrist':
                                event_detail = pbp_events[16] 
                            if pbp_events[14] == 'Backhand' or pbp_events[14] == 'Redirect' or pbp_events[14] == 'Slap' or pbp_events[14] == 'Snap' or pbp_events[14] == 'Wraparound' or pbp_events[14] == 'Wrist':
                                event_detail = pbp_events[14]
                            if pbp_events[12] == 'Backhand' or pbp_events[12] == 'Redirect' or pbp_events[12] == 'Slap' or pbp_events[12] == 'Snap' or pbp_events[12] == 'Wraparound' or pbp_events[12] == 'Wrist':
                                event_detail = pbp_events[12]
                        except:
                            event_detail = '$'
                    elif period < 5 and event_type == 'Goal' and team == home:
                        try:
                            player_B_no = pbp_events[10]
                            player_B = homeROS_dict[int(player_B_no)][0]
                        except:
                            player_B_no = '$'
                            player_B = '$'
                        try:
                            player_C_no = pbp_events[12]
                            player_C = homeROS_dict[int(player_C_no)][0]
                        except:
                            player_C_no = '$'
                            player_C = '$'
                        try:
                            if pbp_events[16] == 'Backhand' or pbp_events[16] == 'Redirect' or pbp_events[16] == 'Slap' or pbp_events[16] == 'Snap' or pbp_events[16] == 'Wraparound' or pbp_events[16] == 'Wrist':
                                event_detail = pbp_events[16]
                            if pbp_events[14] == 'Backhand' or pbp_events[14] == 'Redirect' or pbp_events[14] == 'Slap' or pbp_events[14] == 'Snap' or pbp_events[14] == 'Wraparound' or pbp_events[14] == 'Wrist':
                                event_detail = pbp_events[14]
                            if pbp_events[12] == 'Backhand' or pbp_events[12] == 'Redirect' or pbp_events[12] == 'Slap' or pbp_events[12] == 'Snap' or pbp_events[12] == 'Wraparound' or pbp_events[12] == 'Wrist':
                                event_detail = pbp_events[12]
                        except:
                            event_detail = '$'

                    if period < 5 and event_type == 'Save':
                        try:
                            event_detail = pbp_events[10]
                        except:
                            event_detail = '$'

                    if period == 5 and event == 'Shot' and team == away:
                        try:
                            player_A_no = pbp_events[7]
                            player_A = awayROS_dict[int(player_A_no)][0]
                        except:
                            player_A_no = '$'
                            player_A = '$'                        
                    elif period == 5 and event == 'Shot' and team == home:
                        try:
                            player_A_no = pbp_events[7]
                            player_A = homeROS_dict[int(player_A_no)][0]
                        except:
                            player_A_no = '$'
                            player_A = '$'    

                    if event == 'Penalty' and team == away:
                        try:
                            player_A_no = pbp_events[7]
                            player_A = awayROS_dict[int(player_A_no)][0]
                        except:
                            player_A_no = '$'
                            player_A = '$'
                        try:
                            event_type = pbp_events[10]
                        except:
                            event_type = '$'
                        try:
                            event_detail = dict_penalties.PENALTIES[pbp_events[9]]
                        except:
                            event_detail = pbp_events[9]
                    elif event == 'Penalty' and team == home:
                        try:
                            player_A_no = pbp_events[7]
                            player_A = homeROS_dict[int(player_A_no)][0]
                        except:
                            player_A_no = '$'
                            player_A = '$'
                        try:
                            event_type = pbp_events[10]
                        except:
                            event_type = '$'
                        try:
                            event_detail = dict_penalties.PENALTIES[pbp_events[9]]
                        except:
                            event_detail = pbp_events[9]                       

                    if event == 'Hit' and team == away or event == 'Giveaway' and team == away or event == 'Takeaway' and team == away:
                        try:
                            player_A_no = pbp_events[8]
                            player_A = awayROS_dict[int(player_A_no)][0]
                        except:
                            player_A_no = '$'
                            player_A = '$'
                    elif event == 'Hit' and team == home or event == 'Giveaway' and team == home or event == 'Takeaway' and team == home:
                        try:
                            player_A_no = pbp_events[8]
                            player_A = homeROS_dict[int(player_A_no)][0]
                        except:
                            player_A_no = '$'
                            player_A = '$'

                    if period != 5 and event_type == 'Goal' and team == home and player_A != '$':
                        home_goals += 1               
                    elif period != 5 and event_type == 'Goal' and team == away and player_A != '$':
                        away_goals += 1                
                    elif period == int(5):
                        home_goals = home_goals
                        away_goals = home_goals
            
                    home_scorediff = int(home_goals) - int(away_goals)
                    away_scorediff = int(away_goals) - int(home_goals)
            
                    if period != 5 and event_type == 'Goal' and team == home:
                        home_scorediff = home_scorediff - 1
                        away_scorediff = away_scorediff + 1
            
                    if period != 5 and event_type == 'Goal' and team == away:
                        home_scorediff = home_scorediff + 1
                        away_scorediff = away_scorediff - 1
                        
                    if period == 5:
                        home_scorediff = home_scorediff
                        away_scorediff = away_scorediff
            
                    if period != 5 and int(home_scorediff) == int(away_scorediff):
                        home_situation = 'Tied'
                        away_situation = 'Tied'
                    elif period != 5 and int(home_scorediff) > int(away_scorediff):
                        home_situation = 'Leading'
                        away_situation = 'Trailing'
                    elif period != 5 and int(home_scorediff) < int(away_scorediff):
                        home_situation = 'Trailing'
                        away_situation = 'Leading'                        
                    
                    home_strength = '$'
                    away_strength = '$'
                    
                    home_state = '$'
                    away_state = '$'
                    
                    if event == 'Goal' and player_A == '$':
                        seconds_gone = '$'
                        time_gone = '$'
                        home_situation = '$'
                        away_situation = '$'
                        home_scorediff = '$'
                        away_scorediff = '$'

                    homeon_1_no = '$'
                    homeon_2_no = '$'
                    homeon_3_no = '$'
                    homeon_4_no = '$'
                    homeon_5_no = '$'
                    homeon_6_no = '$'
                    homeon_1 = '$'
                    homeon_2 = '$'
                    homeon_3 = '$'
                    homeon_4 = '$'
                    homeon_5 = '$'
                    homeon_6 = '$'                        
                    
                    if period < 5 and event_type == 'Goal' and team == home and player_A == '$':
                        try:
                            homeon_1_no = pbp_events[17]
                            homeon_1 = homeROS_dict[int(homeon_1_no)][0]
                        except:
                            pass
                        try:
                            homeon_2_no = pbp_events[19]
                            homeon_2 = homeROS_dict[int(homeon_2_no)][0]
                        except:
                            pass
                        try:
                            homeon_3_no = pbp_events[21]
                            homeon_3 = homeROS_dict[int(homeon_3_no)][0]                          
                        except:
                            pass
                        try:
                            homeon_4_no = pbp_events[23]
                            homeon_4 = homeROS_dict[int(homeon_4_no)][0]
                        except:
                            pass
                        try:
                            homeon_5_no = pbp_events[25]
                            homeon_5 = homeROS_dict[int(homeon_5_no)][0]
                        except:
                            pass
                        try:
                            homeon_6_no = pbp_events[27]
                            homeon_6 = homeROS_dict[int(homeon_6_no)][0]
                        except:
                            pass

                    awayon_1_no = '$'
                    awayon_2_no = '$'
                    awayon_3_no = '$'
                    awayon_4_no = '$'
                    awayon_5_no = '$'
                    awayon_6_no = '$'
                    awayon_1 = '$'
                    awayon_2 = '$'
                    awayon_3 = '$'
                    awayon_4 = '$'
                    awayon_5 = '$'
                    awayon_6 = '$'                        
                    
                    if period < 5 and event_type == 'Goal' and team == away and player_A == '$':
                        try:
                            awayon_1_no = pbp_events[17]
                            awayon_1 = awayROS_dict[int(awayon_1_no)][0]
                        except:
                            pass
                        try:
                            awayon_2_no = pbp_events[19]
                            awayon_2 = awayROS_dict[int(awayon_2_no)][0]
                        except:
                            pass
                        try:
                            awayon_3_no = pbp_events[21]
                            awayon_3 = awayROS_dict[int(awayon_3_no)][0]                          
                        except:
                            pass
                        try:
                            awayon_4_no = pbp_events[23]
                            awayon_4 = awayROS_dict[int(awayon_4_no)][0]
                        except:
                            pass
                        try:
                            awayon_5_no = pbp_events[25]
                            awayon_5 = awayROS_dict[int(awayon_5_no)][0]
                        except:
                            pass
                        awayon_6 = awayon_6.strip()
                        try:
                            awayon_6_no = pbp_events[27]
                            awayon_6 = awayROS_dict[int(awayon_6_no)][0]
                        except:
                            awayon_6 = awayon_6
                                        
                    if event_detail == 'Deflected' or event_detail == 'Deflection' or event_detail == 'Tip-In' or event_detail == 'Tipped':
                        event_detail = 'Redirect'

                    if event_detail == 'Wrap-around':
                        event_detail = 'Wraparound'

                    home_state_detail = '$'
                    away_state_detail = '$'
                    
                    if event == 'Giveaway' and pbp_events[7] == 'EV' or event == 'Hit' and pbp_events[7] == 'EV' or event == 'Shot' and pbp_events[7] == 'EV' or event == 'Takeaway' and pbp_events[7] == 'EV':
                        away_state_detail = 'EV'
                        home_state_detail = 'EV'
                    elif event == 'Giveaway' and team == away and pbp_events[7] == 'PP' or event == 'Hit' and team == away and pbp_events[7] == 'PP' or event == 'Shot' and event_type != 'Block' and team == away and pbp_events[7] == 'PP' or event == 'Takeaway' and team == away and pbp_events[7] == 'PP':
                        away_state_detail = 'PP'
                        home_state_detail = 'SH'
                    elif event == 'Giveaway' and team == home and pbp_events[7] == 'PP' or event == 'Hit' and team == home and pbp_events[7] == 'PP' or event == 'Shot' and event_type != 'Block' and team == home and pbp_events[7] == 'PP' or event == 'Takeaway' and team == home and pbp_events[7] == 'PP':
                        away_state_detail = 'SH'
                        home_state_detail = 'PP'
                    elif event == 'Giveaway' and team == away and pbp_events[7] == 'SH' or event == 'Hit' and team == away and pbp_events[7] == 'SH' or event == 'Shot' and event_type != 'Block' and team == away and pbp_events[7] == 'SH' or event == 'Takeaway' and team == away and pbp_events[7] == 'SH':
                        away_state_detail = 'SH'
                        home_state_detail = 'PP'
                    elif event == 'Giveaway' and team == home and pbp_events[7] == 'SH' or event == 'Hit' and team == home and pbp_events[7] == 'SH' or event == 'Shot' and event_type != 'Block' and team == home and pbp_events[7] == 'SH' or event == 'Takeaway' and team == home and pbp_events[7] == 'SH':
                        away_state_detail = 'PP'
                        home_state_detail = 'SH'

                    if event_type == 'Block' and team == away and pbp_events[7] == 'PP':
                        away_state_detail = 'SH'
                        home_state_detail = 'PP'
                    elif event_type == 'Block' and team == home and pbp_events[7] == 'PP':
                        away_state_detail = 'PP'
                        home_state_detail = 'SH'
                    elif event_type == 'Block' and team == away and pbp_events[7] == 'SH':
                        away_state_detail = 'PP'
                        home_state_detail = 'SH'
                    elif event_type == 'Block' and team == home and pbp_events[7] == 'SH':
                        away_state_detail = 'SH'
                        home_state_detail = 'PP'

                    if pbp_events[0] == 'F':
                        period = '5'
                        seconds_gone = '$'
                        time_left = '$'
                        time_gone = '$'
                        home_goals = home_goals
                        away_goals = away_goals
                        home_situation = home_situation
                        away_situation = away_situation
                        home_scorediff = home_scorediff
                        away_scorediff = away_scorediff
                        home_strength = '$'
                        away_strength = '$'
                        home_state = '$'
                        away_state = '$'
                        home_state_detail = '$'
                        away_state_detail = '$'
                        event = pbp_events[1]
                        event_type = pbp_events[2]
                        event_detail = pbp_events[7]
                        home_zone = '$'
                        away_zone = '$'
                        if pbp_events[4] == away:
                            team = away
                            player_A_no = pbp_events[5]
                            player_A = awayROS_dict[int(player_A_no)][0]
                        elif pbp_events[4] == home:
                            team = home
                            player_A_no = pbp_events[5]
                            player_A = homeROS_dict[int(player_A_no)][0]                        

                    try:
                        special_states = pbp_events[17]
                        if special_states == 'EN' or special_states == 'PS':
                            home_state_detail = special_states
                            away_state_detail = special_states
                    except:
                        pass

                    try:
                        if pbp_events[10] == 'I' or pbp_events[10] == 'II' or pbp_events[10] == 'III' or pbp_events[10] == 'IV':
                            event_detail == pbp_events[11]
                    except:
                        pass
                    
                    pbp_tup = [(season_id, game_id, date, home, away, game_type, home_result, away_result, period, seconds_gone, time_left, time_gone, home_goals, away_goals, home_situation, away_situation, home_scorediff, away_scorediff, home_strength, away_strength, home_state, away_state, home_state_detail, away_state_detail, event, event_type, event_detail, home_zone, away_zone, team, player_A, player_B, player_C, homeon_1, homeon_2, homeon_3, homeon_4, homeon_5, homeon_6, awayon_1, awayon_2, awayon_3, awayon_4, awayon_5, awayon_6)]

                    csvRows += pbp_tup
                    
                ### write the rows to file
                csvWriter.writerows(csvRows)                          
                
                if load_pbp != 'true':
                    ### reload the play-by-play file for some touch-up in pandas
                    pbp_df = pd.read_csv(pbp_outfile, encoding='utf-8')              

                    ### remove instances where the goalie was recorded as being pulled (recoded as 'Empty-Net' in the event column)
                    pbp_df = pbp_df[(pbp_df['EVENT_TYPE'] != 'Empty-Net')]

                    ### return the home goals or away goals to whatever the value was prior to when whichever team scores
                    pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.TEAM == home), ['HOME_GOALS']] = pbp_df['HOME_GOALS'] - 1; pbp_df
                    pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.TEAM == away), ['AWAY_GOALS']] = pbp_df['AWAY_GOALS'] - 1; pbp_df
    
                    ### make a separate dataframe with just goals for events; manipulate the on-ice players; save to file
                    goals_df = pbp_df[(pbp_df['EVENT_TYPE'] == 'Goal')]
    
                    home_goals_df = goals_df.copy()
                    home_goals_df = home_goals_df[(home_goals_df['PERIOD'] < 5) & (home_goals_df['TEAM'] == home) & (home_goals_df['TIME_GONE'] == '$')]
                    home_goals_df = home_goals_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'SECONDS_GONE', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE',  'HOME_STATE_DETAIL', 'AWAY_STATE_DETAIL', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
    
                    away_goals_df = goals_df.copy()
                    away_goals_df = away_goals_df[(away_goals_df['PERIOD'] < 5) & (away_goals_df['TEAM'] == away) & (away_goals_df['TIME_GONE'] == '$')]
                    away_goals_df = away_goals_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'SECONDS_GONE', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE',  'HOME_STATE_DETAIL', 'AWAY_STATE_DETAIL', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6'])
    
                    goals_df = goals_df[(goals_df['TIME_GONE'] != '$')]
                    goals_df = goals_df.drop(columns=['HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
    
                    goals_df = pd.merge(goals_df, home_goals_df, on='TIME_LEFT', how='left')
                    goals_df = pd.merge(goals_df, away_goals_df, on='TIME_LEFT', how='left')
    
                    goals_df = goals_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'SECONDS_GONE', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE', 'HOME_STATE_DETAIL', 'AWAY_STATE_DETAIL', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C'])
    
                    ### remove the rows following goals that only contained the home and away on-ice players; add the home and away on-ice players for goals from the goals dataframe
                    pbp_df = pbp_df[(pbp_df['PERIOD'] < 5) & (pbp_df['TIME_GONE'] != '$')]
    
                    pbp_df = pbp_df.drop(columns=['HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
    
                    pbp_df = pd.merge(pbp_df, goals_df, how='left', on=['PERIOD', 'TIME_LEFT'])
    
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.HOMEON_1 != '$'),['HOMEON_1']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.HOMEON_2 != '$'),['HOMEON_2']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.HOMEON_3 != '$'),['HOMEON_3']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.HOMEON_4 != '$'),['HOMEON_4']] = '$'; pbp_df                
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.HOMEON_5 != '$'),['HOMEON_5']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.HOMEON_6 != '$'),['HOMEON_6']] = '$'; pbp_df
    
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.AWAYON_1 != '$'),['AWAYON_1']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.AWAYON_2 != '$'),['AWAYON_2']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.AWAYON_3 != '$'),['AWAYON_3']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.AWAYON_4 != '$'),['AWAYON_4']] = '$'; pbp_df                
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.AWAYON_5 != '$'),['AWAYON_5']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.AWAYON_6 != '$'),['AWAYON_6']] = '$'; pbp_df

                    ### save the adjusted csv file
                    pbp_df.to_csv(pbp_outfile, index = False)
                        
                if load_pbp == 'true':
                    ### load the play-by-play file with NUL bytes already manually removed for some more cleaning in pandas
                    pbp_df = pd.read_csv(pbp_outfile_20062007, encoding='utf-8')
                    
                    ### replace any NaNs
                    pbp_df = pbp_df.fillna('$')

                    ### remove instances where the goalie was recorded as being pulled (recoded as 'Empty-Net' in the event column)
                    pbp_df = pbp_df[(pbp_df['EVENT_TYPE'] != 'Empty-Net')]

                    ### return, for previously unprocessed rows (prior to the shootout) only, the home goals or away goals to whatever the value was prior to when whichever team scores
                    pbp_df.loc[(pbp_df.PERIOD != 5) & (pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.TEAM == home), ['HOME_GOALS']] = pbp_df['HOME_GOALS'] - 1; pbp_df
                    pbp_df.loc[(pbp_df.PERIOD != 5) & (pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.TEAM == away), ['AWAY_GOALS']] = pbp_df['AWAY_GOALS'] - 1; pbp_df
    
                    ### make a separate dataframe containing just the time remaining and on-ice information for goals already processed
                    old_goals_df = pbp_df[(pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['SECONDS_GONE'] != '$') & (pbp_df['HOMEON_1'] != '$')]
                    old_goals_df = old_goals_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'SECONDS_GONE', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE',  'HOME_STATE_DETAIL', 'AWAY_STATE_DETAIL', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C'])
                   
                    ### make, for previously unprocessed rows only, a separate dataframe with just goals for events; manipulate the on-ice players; save to file
                    new_goals_df = pbp_df[(pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['SECONDS_GONE'] != '$') & (pbp_df['HOMEON_1'] == '$') | (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['SECONDS_GONE'] == '$') & (pbp_df['HOMEON_1'] != '$') | (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['SECONDS_GONE'] == '$') & (pbp_df['AWAYON_1'] != '$')]

                    new_home_goals_df = new_goals_df.copy()
                    new_home_goals_df = new_home_goals_df[(new_home_goals_df['PERIOD'] < 5) & (new_home_goals_df['TEAM'] == home) & (new_home_goals_df['TIME_GONE'] == '$')]
                    new_home_goals_df = new_home_goals_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'SECONDS_GONE', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE',  'HOME_STATE_DETAIL', 'AWAY_STATE_DETAIL', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
    
                    new_away_goals_df = new_goals_df.copy()
                    new_away_goals_df = new_away_goals_df[(new_away_goals_df['PERIOD'] < 5) & (new_away_goals_df['TEAM'] == away) & (new_away_goals_df['TIME_GONE'] == '$')]
                    new_away_goals_df = new_away_goals_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'SECONDS_GONE', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE',  'HOME_STATE_DETAIL', 'AWAY_STATE_DETAIL', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6'])
    
                    new_goals_df = new_goals_df[(new_goals_df['TIME_GONE'] != '$')]
                    new_goals_df = new_goals_df.drop(columns=['HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
    
                    new_goals_df = pd.merge(new_goals_df, new_away_goals_df, on='TIME_LEFT', how='left')
                    new_goals_df = pd.merge(new_goals_df, new_home_goals_df, on='TIME_LEFT', how='left')
    
                    ### combine the on-ice info for goals previously and newly processed; filter out columns before merging with the main play-by-play dataframe
                    goals_df = pd.concat([old_goals_df, new_goals_df], sort=True)
                    goals_df = goals_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'SECONDS_GONE', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE', 'HOME_STATE_DETAIL', 'AWAY_STATE_DETAIL', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C'])

                    ### create a separate dataframe for any shootout events
                    shootout_df = pbp_df.copy()
                    shootout_df = shootout_df[(shootout_df['PERIOD'] == 5)]
                    shootout_df.loc[(shootout_df.SECONDS_GONE == '$'),['SECONDS_GONE']] = 3901; shootout_df

                    ### remove the rows following goals that only contained the home and away on-ice players; add the home and away on-ice players for goals from the goals dataframe   
                    pbp_df = pbp_df[(pbp_df['PERIOD'] < 5) & (pbp_df['PERIOD'] != 0)]

                    pbp_df = pbp_df.drop(columns=['HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
    
                    pbp_df = pd.merge(pbp_df, goals_df, how='left', on=['PERIOD', 'TIME_LEFT'])  

                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.HOMEON_1 != '$'),['HOMEON_1']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.HOMEON_2 != '$'),['HOMEON_2']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.HOMEON_3 != '$'),['HOMEON_3']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.HOMEON_4 != '$'),['HOMEON_4']] = '$'; pbp_df                
                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.HOMEON_5 != '$'),['HOMEON_5']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.HOMEON_6 != '$'),['HOMEON_6']] = '$'; pbp_df
    
                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.AWAYON_1 != '$'),['AWAYON_1']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.AWAYON_2 != '$'),['AWAYON_2']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.AWAYON_3 != '$'),['AWAYON_3']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.AWAYON_4 != '$'),['AWAYON_4']] = '$'; pbp_df                
                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.AWAYON_5 != '$'),['AWAYON_5']] = '$'; pbp_df
                    pbp_df.loc[(pbp_df.EVENT_TYPE != 'Goal') & (pbp_df.AWAYON_6 != '$'),['AWAYON_6']] = '$'; pbp_df

                    ### tacl any shootout events back onto the end of the play-by-play dataframe
                    pbp_df = pd.concat([pbp_df, shootout_df], sort=False)

                    ### save the adjusted csv file
                    pbp_df.to_csv(pbp_temp, index=False) 

        if load_pbp == 'true':
            ### remove the raw play-by-play file and replace it with the temporary, processed play-by-play file and then remove the temporary file
            os.remove(pbp_outfile)
            
            pbp_df = pd.read_csv(pbp_temp, encoding='utf-8')
            
            pbp_df.to_csv(pbp_outfile, index=False)
        
            os.remove(pbp_temp)


        print('Finished parsing NHL play-by-play from .HTM for ' + season_id + ' ' + game_id)

        
    ###
    ### ESPN PLAY-BY-PLAY (XML) 
    ### 

    ### part 1: retrieve ESPN's own game identifier          
    ESPN_game_df = schedule_date.copy()
    ESPN_game_df['DATE'] = ESPN_game_df['DATE'].str.replace('/','-')
    ESPN_date_df = ESPN_game_df['DATE']

    for ESPN_date in ESPN_date_df:
        ESPN_year = ESPN_date.split('-')[2]
        ESPN_year = ESPN_year.split('.')[0]
       
        ESPN_month_no = ESPN_date.split('-')[0]
        
        ESPN_day_no = ESPN_date.split('-')[1]
        
        ### retrieve the ESPN scoreboard HTML
        try:
            ESPN_scoreboard = requests.get('http://www.espn.com/nhl/scoreboard?date=' + ESPN_year + ESPN_month_no + ESPN_day_no, timeout=5).text
            f = open(files_root + 'ESPN_scoreboard.txt', 'w+')
            f.write(ESPN_scoreboard)
            f.close()
        except:
            print('Could not retrieve the ESPN scoreboard HTML for ' + season_id + ' ' + game_id)

        with open(files_root + 'ESPN_scoreboard.txt', 'r') as get_ESPN_scoreboard:
            ESPN_soup = BeautifulSoup(get_ESPN_scoreboard, 'html.parser')
   
            ESPN_teams_divs = ESPN_soup.find_all('div', {'class': 'ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db'})

            ESPN_teams = [i.get_text() for i in ESPN_teams_divs]
            ESPN_teams = [ESPN_teams[i:i+2] for i in range(0, len(ESPN_teams), 2)]
          
            ESPN_teams_df = pd.DataFrame(ESPN_teams, columns=['AWAY', 'HOME'])

            ESPN_ids_links = ESPN_soup.find_all('a', {'class': 'AnchorLink Button Button--sm Button--anchorLink Button--alt mb4 w-100'}, href=True)

            ESPN_ids = [i['href'] for i in ESPN_ids_links]

            ESPN_ids = [ESPN_ids[i:i+2] for i in range(0, len(ESPN_ids), 2)]
            ESPN_ids = [i[0].rsplit('/', 1)[1] for i in ESPN_ids]

            ESPN_ids_unique=[]
            [ESPN_ids_unique.append(i) for i in ESPN_ids if i not in ESPN_ids_unique]

            ESPN_ids_df = pd.DataFrame(ESPN_ids_unique, columns=['ESPN_ID'])          
           
            ESPN_ids_df = pd.concat([ESPN_ids_df, ESPN_teams_df], axis=1)
            if int(season_id) >= 20142015:
                ESPN_ids_df['HOME'] = ESPN_ids_df['HOME'].replace(dict_teams.MONIKERS_DICT)
                ESPN_ids_df['AWAY'] = ESPN_ids_df['AWAY'].replace(dict_teams.MONIKERS_DICT)
            elif int(season_id) < 20142015 and int(season_id) >= 20112012:
                ESPN_ids_df['HOME'] = ESPN_ids_df['HOME'].replace(dict_teams.MONIKERS_DICT_PHX)
                ESPN_ids_df['AWAY'] = ESPN_ids_df['AWAY'].replace(dict_teams.MONIKERS_DICT_PHX)
            elif int(season_id) < 20112012:
                ESPN_ids_df['HOME'] = ESPN_ids_df['HOME'].replace(dict_teams.MONIKERS_DICT_WPG2ATL)
                ESPN_ids_df['AWAY'] = ESPN_ids_df['AWAY'].replace(dict_teams.MONIKERS_DICT_WPG2ATL)
                       
            ESPN_id_df = ESPN_ids_df.copy()
            ESPN_id_df = ESPN_id_df[(ESPN_id_df['HOME'] == home) & (ESPN_id_df['AWAY'] == away)]
            try:
                ESPN_id = ESPN_id_df['ESPN_ID'].values[0]
            except:
                ESPN_id_dict = {}
                if int(season_id) >= 20142015:                
                    ESPN_id_dict = {'BOS': '01', 'BUF': '02', 'CGY': '03', 'CHI': '04', 'DET': '05', 'EDM': '06', 'CAR': '07', 'LAK': '08', 'DAL': '09', 'MTL': '10', 'NJD': '11', 'NYI': '12', 'NYR': '13', 'OTT': '14', 'PHI': '15', 'PIT': '16', 'COL': '17', 'SJS': '18', 'STL': '19', 'TBL': '20', 'TOR': '21', 'VAN': '22', 'WSH': '23', 'ARI': '24', 'ANA': '25', 'FLA': '26', 'NSH': '27', 'WPG': '28', 'CBJ': '29', 'MIN': '30', 'VGK': '31'}                   
                if int(season_id) >= 20112012 and int(season_id) <= 20132014:
                    ESPN_id_dict = {'BOS': '01', 'BUF': '02', 'CGY': '03', 'CHI': '04', 'DET': '05', 'EDM': '06', 'CAR': '07', 'LAK': '08', 'DAL': '09', 'MTL': '10', 'NJD': '11', 'NYI': '12', 'NYR': '13', 'OTT': '14', 'PHI': '15', 'PIT': '16', 'COL': '17', 'SJS': '18', 'STL': '19', 'TBL': '20', 'TOR': '21', 'VAN': '22', 'WSH': '23', 'PHX': '24', 'ANA': '25', 'FLA': '26', 'NSH': '27', 'WPG': '28', 'CBJ': '29', 'MIN': '30'}                                    
                if int(season_id) <= 20102011:
                    ESPN_id_dict = {'BOS': '01', 'BUF': '02', 'CGY': '03', 'CHI': '04', 'DET': '05', 'EDM': '06', 'CAR': '07', 'LAK': '08', 'DAL': '09', 'MTL': '10', 'NJD': '11', 'NYI': '12', 'NYR': '13', 'OTT': '14', 'PHI': '15', 'PIT': '16', 'COL': '17', 'SJS': '18', 'STL': '19', 'TBL': '20', 'TOR': '21', 'VAN': '22', 'WSH': '23', 'PHX': '24', 'ANA': '25', 'FLA': '26', 'NSH': '27', 'ATL': '28', 'CBJ': '29', 'MIN': '30'}
                ESPN_id_locationcode = ESPN_id_dict[home]


                ESPN_id_yearcode = str()
                if int(season_id) == 20062007:
                    ESPN_id_yearcode = '26'
                if int(season_id) == 20072008:
                    ESPN_id_yearcode = '27'
                if int(season_id) == 20082009:
                    ESPN_id_yearcode = '28'
                if int(season_id) == 20092010:
                    ESPN_id_yearcode = '29'                    
                if int(season_id) == 20102011:
                    ESPN_id_yearcode = '30'
                    
                ESPN_id = ESPN_id_yearcode + date.split('/')[0] + date.split('/')[1] + '0' + ESPN_id_locationcode
           
            ### part 2: retrieve ESPN's play-by-play (XML) data using ESPN_id; scrub potential illegal characters (https://bugs.python.org/issue5166)
            try:
                ESPN_url = 'http://www.espn.com/nhl/gamecast/data/masterFeed?lang=en&isAll=true&gameId=' + str(ESPN_id)
                ESPN_content = requests.get(ESPN_url, timeout=5).text
                f = open(files_root + 'pbp_ESPN.xml', 'w+')
                f.write(escape_xml_illegal_chars(ESPN_content))
                f.close()
            except:
                print('ERROR: Could not retrieve the ESPN play-by-play (XML) for ' + season_id + ' ' + game_id)

            ### part 3: parse ESPN's play-by-play (XML) data
            with open(files_root + 'pbp_ESPN.csv', 'w', newline = '') as ESPN_pbp_outfile:
                
                csvWriter = csv.writer(ESPN_pbp_outfile)
                
                csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'PERIOD', 'SECONDS_GONE', 'TIME_LEFT', 'TIME_GONE', 'EVENT', 'EVENT_TYPE', 'EVENT_WEIGHT', 'TEAM', 'X_1', 'Y_1', 'X_2', 'Y_2'])
         
                ESPN_xml = files_root + 'pbp_ESPN.xml' 
                ESPN_xml = ESPN_xml.replace(u'\x13', '-')

                try:        
                    ESPN_tree = ET.parse(ESPN_xml)
                except:
                    print('Encountered an improperly structured file for ' + season_id + ' ' + game_id + ' ESPN pbp that can still be parsed.')

                ESPN_root = ESPN_tree.getroot()

                team_id_dict = {}
                ### VGK debuted in 20182019
                if int(season_id) >= 20142015:
                    team_id_dict = {'0': '', '1': 'BOS', '2': 'BUF', '3': 'CGY', '4': 'CHI', '5': 'DET', '6': 'EDM', '7': 'CAR', '8': 'LAK', '9': 'DAL', '10': 'MTL', '11': 'NJD', '12': 'NYI', '13': 'NYR', '14': 'OTT', '15': 'PHI', '16': 'PIT', '17': 'COL', '18': 'SJS', '19': 'STL', '20': 'TBL', '21': 'TOR', '22': 'VAN', '23': 'WSH', '24': 'ARI', '25': 'ANA', '26': 'FLA', '27': 'NSH', '28': 'WPG', '29': 'CBJ', '30': 'MIN', '37': 'VGK'}
                ### force PHX instead of ARI
                if int(season_id) >= 20112012 and int(season_id) <= 20132014:
                    team_id_dict = {'0': '', '1': 'BOS', '2': 'BUF', '3': 'CGY', '4': 'CHI', '5': 'DET', '6': 'EDM', '7': 'CAR', '8': 'LAK', '9': 'DAL', '10': 'MTL', '11': 'NJD', '12': 'NYI', '13': 'NYR', '14': 'OTT', '15': 'PHI', '16': 'PIT', '17': 'COL', '18': 'SJS', '19': 'STL', '20': 'TBL', '21': 'TOR', '22': 'VAN', '23': 'WSH', '24': 'PHX', '25': 'ANA', '26': 'FLA', '27': 'NSH', '28': 'WPG', '29': 'CBJ', '30': 'MIN'}
                ### force ATL instead of WPG
                if int(season_id) <= 20102011:
                    team_id_dict = {'0': '', '1': 'BOS', '2': 'BUF', '3': 'CGY', '4': 'CHI', '5': 'DET', '6': 'EDM', '7': 'CAR', '8': 'LAK', '9': 'DAL', '10': 'MTL', '11': 'NJD', '12': 'NYI', '13': 'NYR', '14': 'OTT', '15': 'PHI', '16': 'PIT', '17': 'COL', '18': 'SJS', '19': 'STL', '20': 'TBL', '21': 'TOR', '22': 'VAN', '23': 'WSH', '24': 'PHX', '25': 'ANA', '26': 'FLA', '27': 'NSH', '28': 'ATL', '29': 'CBJ', '30': 'MIN'}

                try:
                    events = [event[2].text for event in ESPN_root.iter('Plays')]
                except:
                    print('ERROR: There were no plays in the XML file for ' + season_id + ' ' + game_id + ' ESPN pbp.')
                    continue
                    
                for plays in ESPN_root.findall('Plays'):
        
                    pbpTup = ([])
                    
                    for play in plays:
                        events = play.text.split('~')

                        period = events[4]
                        if int(period) == 5:
                            continue
        
                        time_gone = events[3]
                        
                        parse_time_gone = time_gone.split(':')
                            
                        time_left = ''
        
                        try:              
                            if int(period) < 4 and int(parse_time_gone[0]) < 20 and int(parse_time_gone[1]) < 51:
                                time_left_minutes = 19 - int(parse_time_gone[0])
                                time_left_seconds = 60 - int(parse_time_gone[1])
                                time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
                            elif int(period) < 4 and int(parse_time_gone[0]) < 20 and int(parse_time_gone[1]) > 50:
                                time_left_minutes = 19 - int(parse_time_gone[0])
                                time_left_seconds = 60 - int(parse_time_gone[1])
                                time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)
                            elif int(period) < 4 and int(parse_time_gone[0]) == 20 and int(parse_time_gone[1]) < 51:
                                time_left_minutes = 20 - int(parse_time_gone[0])
                                time_left_seconds = 60 - int(parse_time_gone[1])
                                time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
                            elif int(period) < 4 and int(parse_time_gone[0]) == 20 and int(parse_time_gone[1]) > 50:
                                time_left_minutes = 20 - int(parse_time_gone[0])
                                time_left_seconds = 60 - int(parse_time_gone[1])
                                time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)
                        except:
                            print('ERROR: Could not produce a regulation time_left value for ' + season_id + ' ' + game_id)
        
                        try:
                            if int(period) == 4 and int(parse_time_gone[0]) < 5 and int(parse_time_gone[1]) < 51:
                                time_left_minutes = 4 - int(parse_time_gone[0])
                                time_left_seconds = 60 - int(parse_time_gone[1])
                                time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
                            if int(period) == 4 and int(parse_time_gone[0]) < 5 and int(parse_time_gone[1]) > 50:
                                time_left_minutes = 4 - int(parse_time_gone[0])
                                time_left_seconds = 60 - int(parse_time_gone[1])
                                time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)
                            elif int(period) == 4 and int(parse_time_gone[0]) == 5 and int(parse_time_gone[1]) < 51:
                                time_left_minutes = 5 - int(parse_time_gone[0])
                                time_left_seconds = 60 - int(parse_time_gone[1])
                                time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
                            elif int(period) == 4 and int(parse_time_gone[0]) == 5 and int(parse_time_gone[1]) > 50:
                                time_left_minutes = 5 - int(parse_time_gone[0])
                                time_left_seconds = 60 - int(parse_time_gone[1])
                                time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)
                        except:
                            print('ERROR: Could not produce an overtime time_left value within ' + season_id + ' ' + game_id)
                                    
                        if time_gone == '20:00':
                            time_left = '0:00'
                        elif time_gone == '19:00':
                            time_left = '1:00'
                        elif time_gone == '18:00':
                            time_left = '2:00'
                        elif time_gone == '17:00':
                            time_left = '3:00'
                        elif time_gone == '16:00':
                            time_left = '4:00'
                        elif time_gone == '15:00':
                            time_left = '5:00'   
                        elif time_gone == '14:00':
                            time_left = '6:00'
                        elif time_gone == '13:00':
                            time_left = '7:00'
                        elif time_gone == '12:00':
                            time_left = '8:00'
                        elif time_gone == '11:00':
                            time_left = '9:00'
                        elif time_gone == '10:00':
                            time_left = '10:00'
                        elif time_gone == '9:00':
                            time_left = '11:00'
                        elif time_gone == '8:00':
                            time_left = '12:00'
                        elif time_gone == '7:00':
                            time_left = '13:00'
                        elif time_gone == '6:00':
                            time_left = '14:00'
                        elif time_gone == '5:00':
                            time_left = '15:00'
                        elif time_gone == '4:00':
                            time_left = '16:00'   
                        elif time_gone == '3:00':
                            time_left = '17:00'
                        elif time_gone == '2:00':
                            time_left = '18:00'
                        elif time_gone == '1:00':
                            time_left = '19:00'
                        elif time_gone == '0:00':
                            time_left = '20:00'
        
                        try:                
                            convert_to_seconds = time_gone.split(':')
                            convert_minutes = int(convert_to_seconds[0]) * 60
                            convert_seconds = int(convert_to_seconds[1])
                            seconds_gone = convert_minutes + convert_seconds
                            if period == '1':
                                seconds_gone = seconds_gone
                            if period == '2':
                                seconds_gone = 1200 + seconds_gone
                            if period == '3':
                                seconds_gone = 2400 + seconds_gone
                            if period == '4':
                                seconds_gone = 3600 + seconds_gone
                        except:
                            print('ERROR: Could not convert the time to seconds within ' + season_id + ' ' + game_id)
                           
                        team = str(events[14])
                        team = team_id_dict[team]
                        if int(season_id) < 20112012 and team == 'WPG':
                            team == 'ATL'
        
                        x_1 = events[0].replace(' ', '')
                        y_1 = events[1].replace(' ', '')
                        x_2 = ''
                        y_2 = ''
                                               
                        description = events[8].upper().replace('  ', ' ')
        
                        blocked = description.split('SHOT ')
        
                        faceoff = description.split('WON')
                        try:
                            faceoff = faceoff[1].split(' ')
                        except:
                            pass

                        event = description.split(' ')
 
                        try:
                            if event[2] == 'BENCH' and event[3] == 'PENALTY':
                                event = 'Penalty'
                        except:
                            pass
       
                        hit = description.split('CREDITED WITH ')
                                                       
                        try:
                            hit = hit[1].split(' ')
                        except:
                            hit = ''
        
                        try:
                            blocked = blocked[1].split(' ')
                        except:
                            pass
        
                        event_type = ''
        
                        try:
                            if faceoff[1] == 'FACEOFF':
                                event = 'Faceoff'
                                event_type = ''
                        except:
                            pass
        
                        if event[0] == 'GIVEAWAY':
                            event = 'Giveaway'
                            event_type = ''
        
                        if event[0] == 'GOAL':
                            event = 'Shot'
                            event_type = 'Goal'
        
                        if event[0] == 'POWER' and event[1] == 'PLAY' and event[2] == 'GOAL':
                            event = 'Shot'
                            event_type = 'Goal'
        
                        if event[0] == 'SHORTHANDED' and event[1] == 'GOAL':
                            event = 'Shot'
                            event_type = 'Goal'
        
                        try:
                            if hit[0] == 'HIT':
                                event = 'Hit'
                                event_type = ''
                        except:
                            pass
        
                        if event[0] == 'PENALTY':
                            event = 'Penalty'
                            event_type = ''
                                
                        if event[0] == 'STOPPAGE':
                            event = 'Stoppage'
                            event_type = ''
                            x_1 = ''
                            y_1 = ''
                            x_2 = ''
                            y_2 = ''
        
                        if blocked[0] == 'BLOCKED':
                            event = 'Shot'
                            event_type = 'Block'
        
                        if event[0] == 'SHOT' and event[1] == 'ON' and event[2] == 'GOAL':
                            event = 'Shot'
                            event_type = 'Save'
        
                        if event[0] == 'SHOT' and event[1] == 'MISSED':
                            event = 'Shot'
                            event_type = 'Miss'
        
                        if event[0] == 'STOPPAGE':
                            event = 'Stoppage'
                            event_type = ''
                            x_1 = ''
                            y_1 = ''
                            x_2 = ''
                            y_2 = ''
        
                        if event[0] == 'TAKEAWAY':
                            event = 'Takeaway'
                            event_type = ''
        
                        event_weight = 0
        
                        if event[0] == 'START' and event[2] == '1ST' or event[0] == 'START' and event[2] == '2ND' or event[0] == 'START' and event[2] == '3RD' or event[0] == 'START' and event[2] == 'OVERTIME':
                            event = 'Period.Start'
                            event_type = ''
                            event_weight = 1
                            x_1 = ''
                            y_1 = ''
                            x_2 = ''
                            y_2 = ''
        
                        try:
                            if event[0] == 'END' and event[2] == '1ST' or event[0] == 'END' and event[2] == '2ND' or event[0] == 'END' and event[2] == '3RD' or event[0] == 'END' and event[2] == 'OVERTIME':
                                event = 'Period.End'
                                event_type = ''
                                x_1 = ''
                                y_1 = ''
                                x_2 = ''
                                y_2 = ''
                        except:
                            pass
        
                        if event[0] == 'END' and event[2] == 'GAME':
                            continue
        
                        if event == 'Faceoff' and time_left == '20:00':
                            event_weight = 2
                        
                        pbpTup = (season_id, game_id, date, home, away, period, seconds_gone, time_left, time_gone, event, event_type, event_weight, team, x_1, y_1, x_2, y_2)
        
                        ### insert the game info and modified play-by-play data
                        csvWriter.writerow(pbpTup)
    
            ### reloads the newly minted csv file for some final touches
            ESPN_pbp_df = pd.read_csv(files_root + 'pbp_ESPN.csv', sep=',')

            ESPN_pbp_df = ESPN_pbp_df[(ESPN_pbp_df['EVENT'] == 'Faceoff') | (ESPN_pbp_df['EVENT'] == 'Giveaway') | (ESPN_pbp_df['EVENT'] == 'Hit') | (ESPN_pbp_df['EVENT'] == 'Penalty') | (ESPN_pbp_df['EVENT'] == 'Shot') | (ESPN_pbp_df['EVENT'] == 'Takeaway')]

            ESPN_pbp_df = ESPN_pbp_df.sort_values(['PERIOD', 'SECONDS_GONE', 'EVENT_WEIGHT'])
              
            ### changes the x,y for shot blocks from primary (x_1, y_1) to secondary (x_2, y_2) values since the league records where the shot was blocked by the defending player 
            try:
                ESPN_pbp_df.loc[(ESPN_pbp_df.EVENT_TYPE == 'Block'), ['X_2']] = ESPN_pbp_df.X_1; ESPN_pbp_df
                ESPN_pbp_df.loc[(ESPN_pbp_df.EVENT_TYPE == 'Block'), ['Y_2']] = ESPN_pbp_df.Y_1; ESPN_pbp_df
                ESPN_pbp_df.loc[(ESPN_pbp_df.EVENT_TYPE == 'Block'), ['X_1']] = ''; ESPN_pbp_df
                ESPN_pbp_df.loc[(ESPN_pbp_df.EVENT_TYPE == 'Block'), ['Y_1']] = ''; ESPN_pbp_df
            except:
                print('ERROR: Could not separate the XY locations into primary and secondary values for ' + season_id + ' ' + game_id + ' ESPN pbp.')

            ### removes the extraneous event_weight column
            ESPN_pbp_df = ESPN_pbp_df.drop(columns=['EVENT_WEIGHT'])

            ### flip the XY coordinates for teams whose 1st and 3rd period shots ESPN recorded with positive x-values 
            flip_XY = []

            if int(season_id) == 20072008 or int(season_id) == 20082009 or int(season_id) == 20092010:
                flip_XY = ['ANA', 'ATL', 'BOS', 'BUF', 'CBJ', 'CGY', 'EDM', 'NJD', 'NSH', 'NYR', 'OTT', 'PHX', 'PIT', 'SJS', 'STL', 'TBL', 'VAN']
                    
            if home in flip_XY:
                ESPN_pbp_df['X_1'] *= -1
                ESPN_pbp_df['Y_1'] *= -1
                ESPN_pbp_df['X_2'] *= -1
                ESPN_pbp_df['Y_2'] *= -1   
            
            ### save to file
            ESPN_pbp_df.to_csv(files_root + 'pbp_ESPN.csv', index = False)
                       
        
        print('Finished parsing ESPN play-by-play from XML for ' + season_id + ' ' + game_id)


    ###
    ### NHL PLAY-BY-PLAY (JSON)
    ###
    
    ### extract the number of goals for both the home and away team
    home_goals = livefeed_data["liveData"]["linescore"]["teams"]["home"]["goals"]
    away_goals = livefeed_data["liveData"]["linescore"]["teams"]["away"]["goals"]
    
    ### determine the home and away result
    home_result = str()
    away_result = str()
    
    if home_goals > away_goals:
        home_result = 'Win'
        away_result = 'Loss'
    elif away_goals > home_goals:
        home_result = 'Loss'
        away_result = 'Win'
    
    ### begin the portion of the script that handles the csv generation
    with open(livefeed_outfile, 'w', newline='') as livefeed_pbp:
        csvWriter = csv.writer(livefeed_pbp)
        
        if int(season_id) >= 20102011:
            csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'SECONDS_GONE', 'TIME_LEFT', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'TEAM', 'HOME_ZONE', 'AWAY_ZONE', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'X_1', 'Y_1', 'X_2', 'Y_2'])
        if int(season_id) < 20102011:
            csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'SECONDS_GONE', 'TIME_LEFT', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C'])
    
        livefeed_plays = livefeed_data["liveData"]["plays"]["allPlays"]
    
        for i in range(len(livefeed_plays))[:]:
    
            ### determine how many seconds of play have already passed, except for shootouts
            time_gone_parse = livefeed_plays[i]["about"]["periodTime"].split(":")
            time_gone_minutes_adjusted = int(time_gone_parse[0]) * 60
            time_gone_seconds = int(time_gone_parse[1])
    
            if int(game_id) < 30000 and livefeed_plays[i]["about"]["period"] != str('4'):
                time_left_seconds = 1200 - (int(time_gone_minutes_adjusted) + int(time_gone_seconds))
            elif int(game_id) < 30000 and livefeed_plays[i]["about"]["period"] == str('4'):
                time_left_seconds = 300 - (int(time_gone_minutes_adjusted) + int(time_gone_seconds))
    
            if int(game_id) < 30000 and livefeed_plays[i]["about"]["period"] == str('5'):
                time_left_seconds = ''
    
            ### check for period and return the seconds elapsed in the game for each event, except for shootouts
            if int(livefeed_plays[i]["about"]["period"]) == 1:
                seconds_gone = int(time_gone_minutes_adjusted) + int(time_gone_seconds)
            elif int(livefeed_plays[i]["about"]["period"]) == 2: # check to see if second period
                seconds_gone = 1200 + int(time_gone_minutes_adjusted) + int(time_gone_seconds)
            elif int(livefeed_plays[i]["about"]["period"]) == 3:
                seconds_gone = 2400 + int(time_gone_minutes_adjusted) + int(time_gone_seconds)
            elif int(livefeed_plays[i]["about"]["period"]) == 4:
                seconds_gone = 3600 + int(time_gone_minutes_adjusted) + int(time_gone_seconds)
            elif int(livefeed_plays[i]["about"]["period"]) == 5:
                seconds_gone = ''
    
            ### pull the time passed on the clock
            time_left = livefeed_plays[i]["about"]["periodTimeRemaining"]
            time_gone = livefeed_plays[i]["about"]["periodTime"]
    
            ### calculate the time remaining on the clock for seasons that don't have values in the livefeed for periodTimeRemaining
            if livefeed_plays[i]["about"]["periodTimeRemaining"] == '' and int(livefeed_plays[i]["about"]["period"]) < 4 and int(time_gone_parse[0]) < 20 and int(time_gone_parse[1]) < 51:
                time_left_minutes = 19 - int(time_gone_parse[0])
                time_left_seconds = 60 - int(time_gone_parse[1])
                time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
            elif livefeed_plays[i]["about"]["periodTimeRemaining"] == '' and int(livefeed_plays[i]["about"]["period"]) < 4 and int(time_gone_parse[0]) < 20 and int(time_gone_parse[1]) > 50:
                time_left_minutes = 19 - int(time_gone_parse[0])
                time_left_seconds = 60 - int(time_gone_parse[1])
                time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)
            elif livefeed_plays[i]["about"]["periodTimeRemaining"] == '' and int(livefeed_plays[i]["about"]["period"]) < 4 and int(time_gone_parse[0]) == 20 and int(time_gone_parse[1]) < 51:
                time_left_minutes = 20 - int(time_gone_parse[0])
                time_left_seconds = 60 - int(time_gone_parse[1])
                time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
            elif livefeed_plays[i]["about"]["periodTimeRemaining"] == '' and int(livefeed_plays[i]["about"]["period"]) < 4 and int(time_gone_parse[0]) == 20 and int(time_gone_parse[1]) > 50:
                time_left_minutes = 20 - int(time_gone_parse[0])
                time_left_seconds = 60 - int(time_gone_parse[1])
                time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)
    
            if livefeed_plays[i]["about"]["periodTimeRemaining"] == '' and int(livefeed_plays[i]["about"]["period"]) == 4 and int(time_gone_parse[0]) < 5 and int(time_gone_parse[1]) < 51:
                time_left_minutes = 4 - int(time_gone_parse[0])
                time_left_seconds = 60 - int(time_gone_parse[1])
                time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
            elif livefeed_plays[i]["about"]["periodTimeRemaining"] == '' and int(livefeed_plays[i]["about"]["period"]) == 4 and int(time_gone_parse[0]) < 5 and int(time_gone_parse[1]) > 50:
                time_left_minutes = 4 - int(time_gone_parse[0])
                time_left_seconds = 60 - int(time_gone_parse[1])
                time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)
            elif livefeed_plays[i]["about"]["periodTimeRemaining"] == '' and int(livefeed_plays[i]["about"]["period"]) == 4 and int(time_gone_parse[0]) == 5 and int(time_gone_parse[1]) < 51:
                time_left_minutes = 5 - int(time_gone_parse[0])
                time_left_seconds = 60 - int(time_gone_parse[1])
                time_left = str(time_left_minutes) + ':' + str(time_left_seconds)
            elif livefeed_plays[i]["about"]["periodTimeRemaining"] == '' and int(livefeed_plays[i]["about"]["period"]) == 4 and int(time_gone_parse[0]) == 5 and int(time_gone_parse[1]) > 50:
                time_left_minutes = 5 - int(time_gone_parse[0])
                time_left_seconds = 60 - int(time_gone_parse[1])
                time_left = str(time_left_minutes) + ':0' + str(time_left_seconds)
    
            if int(livefeed_plays[i]["about"]["period"]) == 5:
                time_gone = ''
    
            if time_gone == '20:00':
                time_left = '0:00'
            elif time_gone == '19:00':
                time_left = '1:00'
            elif time_gone == '18:00':
                time_left = '2:00'
            elif time_gone == '17:00':
                time_left = '3:00'
            elif time_gone == '16:00':
                time_left = '4:00'
            elif time_gone == '15:00':
                time_left = '5:00'
            elif time_gone == '14:00':
                time_left = '6:00'
            elif time_gone == '13:00':
                time_left = '7:00'
            elif time_gone == '12:00':
                time_left = '8:00'
            elif time_gone == '11:00':
                time_left = '9:00'
            elif time_gone == '10:00':
                time_left = '10:00'
            elif time_gone == '09:00':
                time_left = '11:00'
            elif time_gone == '08:00':
                time_left = '12:00'
            elif time_gone == '07:00':
                time_left = '13:00'
            elif time_gone == '06:00':
                time_left = '14:00'
            elif time_gone == '05:00':
                time_left = '15:00'
            elif time_gone == '04:00':
                time_left = '16:00'
            elif time_gone == '03:00':
                time_left = '17:00'
            elif time_gone == '02:00':
                time_left = '18:00'
            elif time_gone == '01:00':
                time_left = '19:00'
            elif time_gone == '00:00':
                time_left = '20:00'
    
            ### determine the home and away score situations
            if int(livefeed_plays[i]["about"]["goals"]["home"]) == int(livefeed_plays[i]["about"]["goals"]["away"]):
                home_situation = 'Tied'
                away_situation = 'Tied'
            elif int(livefeed_plays[i]["about"]["goals"]["home"]) > int(livefeed_plays[i]["about"]["goals"]["away"]):
                home_situation = 'Leading'
                away_situation = 'Trailing'
            elif int(livefeed_plays[i]["about"]["goals"]["home"]) < int(livefeed_plays[i]["about"]["goals"]["away"]):
                home_situation = 'Trailing'
                away_situation = 'Leading'
    
            if int(livefeed_plays[i]["about"]["period"]) == 5:
                seconds_gone = ''
    
            period = str(livefeed_plays[i]["about"]["period"]).replace('1', '1st').replace('2', '2nd').replace('3', '3rd').replace('4', 'OT').replace('5', 'SO')
    
            ### create a variable for game events to manipulate
            event = livefeed_plays[i]["result"]["event"]
    
            ### modify how certain game events are indicated
            if event == 'Game Scheduled':
                event = 'Game.Scheduled'
            elif event == 'Game Official':
                event = 'Game.Official'
            elif event == 'Game End':
                event = 'Game.End'
            elif event == 'Period Ready':
                event = 'Period.Ready'
            elif event == 'Period Start':
                event = 'Period.Start'
            elif event == 'Period End':
                event = 'Period.End'
            elif event == 'Period Official':
                event = 'Period.Official'
            elif event == 'Early Intermission End':
                event = 'Early.Intermission.End'
            elif event == 'Early Intermission Start':
                event = 'Early.Intermission.Start'
            elif event == 'Emergency Goaltender':
                event = 'Emergency.Goaltender'
            elif event == 'Official Challenge':
                event = 'Official.Challenge'
            elif event == 'Shootout Complete':
                event = 'Shootout.End'
            elif event == 'Goal':
                event = 'Shot'
            elif event == 'Blocked Shot':
                event = 'Shot'
            elif event == 'Missed Shot':
                event = 'Shot'
    
            ### create a variable for event type and detail
            event_type = str()
            event_detail = str()
    
            ### establish the type of shot events
            if livefeed_plays[i]["result"]["event"] == 'Goal':
                event_type = 'Goal'
            elif livefeed_plays[i]["result"]["event"] == 'Blocked Shot':
                event_type = 'Block'
            elif livefeed_plays[i]["result"]["event"] == 'Missed Shot':
                event_type = 'Miss'
            elif livefeed_plays[i]["result"]["event"] == 'Shot':
                event_type = 'Save'
    
            ### establish the type of penalty event and capitalize for seasons with string indicators for the severity of penalty
            if event == 'Penalty' and int(season_id) > 20092010:
                event_type = livefeed_plays[i]["result"]["penaltySeverity"]
    
            ### extract the number of penalty minutes assigned for seasons without string indicators for the severity of penalty
            if event == 'Penalty' and int(season_id) < 20102011:
                pims = livefeed_plays[i]["result"]["penaltyMinutes"]
                event_type = str(pims)
                event_type = event_type.replace('2', 'Minor').replace('4', 'Double.Minor').replace('5', 'Major').replace('10', 'Misconduct')
    
            ### modify how rogue penalty types are indicated
            if event_type == 'Bench Minor':
                event_type = 'Minor'
            elif event_type == 'Penalty Shot':
                event_type = 'Penalty.Shot'
    
            ### get and parse the available detail for each event
            try:
                event_detail = livefeed_plays[i]["result"]["secondaryType"]
            except:
                pass
    
            try:
                if livefeed_plays[i]["result"]["event"] == 'Goal' and int(season_id) < 20102011:
                    shot_type_start = livefeed_plays[i]["result"]["description"].split(') ')
                    shot_type_finish = shot_type_start[1].split(' ')
                    event_detail = shot_type_finish[0].replace(',', '')
            except:
                pass

            try:
                if event == 'Penalty':
                    event_detail = dict_penalties.PENALTIES[event_detail]
            except:
                event_detail = ''
    
            ### modify how event detail for shots is indicated
            if event_detail == 'Back':
                event_detail = 'Backhand'
            elif event_detail == 'Deflect':
                event_detail = 'Redirect'
            elif event_detail == 'Deflected':
                event_detail = 'Redirect'
            elif event_detail == 'Deflection':
                event_detail = 'Redirect'
            elif event_detail == 'Slap Shot':
                event_detail = 'Slap'
            elif event_detail == 'Snap Shot':
                event_detail = 'Snap'
            elif event_detail == 'Tip':
                event_detail = 'Redirect'
            elif event_detail == 'Tip-in':
                event_detail = 'Redirect'
            elif event_detail == 'Tip-In':
                event_detail = 'Redirect'
            elif event_detail == 'Wrap':
                event_detail = 'Wraparound'
            elif event_detail == 'Wrap around':
                event_detail = 'Wraparound'
            elif event_detail == 'Wrap-around':
                event_detail = 'Wraparound'
            elif event_detail == 'Wrap Around':
                event_detail = 'Wraparound'
            elif event_detail == 'Wrap-Around':
                event_detail = 'Wraparound'
            elif event_detail == 'Wrist Shot':
                event_detail = 'Wrist'
    
            ### avoid duplication in the event type and detail columns as needed for penalties
            if event_type == 'Match':
                event_detail = ''
            elif event_type == 'Misconduct':
                event_detail = ''
    
            if event_type == 'Game Misconduct':
                event_type = 'Misconduct'
                event_detail = 'Game'
            elif event_detail == 'Game.Misconduct':
                event_type = 'Misconduct'
                event_detail = 'Game'
    
            if event_type == 'Minor' and event_detail == 'Minor':
                event_detail = ''
            elif event_type == 'Double-Minor' and event_detail == 'Double-Minor':
                event_detail = ''
            elif event_type == 'Major' and event_detail == 'Major':
                event_detail = ''
    
            ### create a variable for game event descriptions
            description = livefeed_plays[i]["result"]["description"]
    
            ### establish the detail for stoppage events
            if description == 'Icing':
                event_type = 'Icing'
            elif description == 'Offside':
                event_type = 'Offside'
    
            ### create a variable for the team credited with each events
            try:
                team = livefeed_plays[i]["team"]["triCode"]
            except:
                pass
    
            ### clear team credit for certain events
            if event == 'Game.Scheduled' or event == 'Game.End' or event == 'Period.Ready' or event == 'Period.Start' or event == 'Period.End' or event == 'Period.Official':
                team = ''

            if int(season_id) >= 20102011:    
                ### fetch the x and y coordinates for the primary location of an event
                x_1 = str()
                y_1 = str()
        
                try:
                    x_1 = int(livefeed_plays[i]["coordinates"]["x"])
                    y_1 = int(livefeed_plays[i]["coordinates"]["y"])
                except:
                    pass
        
                ### set up x and y coordinates for the secondary location of an event (e.g. where pucks were redirected or blocked)
                x_2 = str()
                y_2 = str()
        
                if event_type == 'Block':
                    x_2 = x_1
                    y_2 = y_1
                    x_1 = ''
                    y_1 = ''
    
            ### obtain the players involved in each event
            player_A = ''
            player_B = ''
            player_C = ''
    
            try:
                player_A = livefeed_plays[i]["players"][0]["player"]["fullName"]
            except:
                pass
    
            player_A = player_A.replace(' ', '.').upper()
    
            try:
                player_B = livefeed_plays[i]["players"][1]["player"]["fullName"]
            except:
                pass
    
            player_B = player_B.replace(' ','.').upper()
    
            try:
                player_C = livefeed_plays[i]["players"][2]["player"]["fullName"]
            except:
                pass
    
            player_C = player_C.replace(' ', '.').upper()
    
            ### clear default values for events that do not have given coordinates
            if event == 'Game.Scheduled' or event == 'Game.End' or event == 'Period.Ready' or event == 'Period.Start' or event == 'Period.End' or event == 'Period.Official' or event == 'Stoppage':
                x_1 = ''
                y_1 = ''
                player_A = ''
                player_B = ''
                player_C = ''
    
            if event_type == 'Miss' or event == 'Giveaway'  or event == 'Takeaway':
                player_B = ''
                player_C = ''
    
            if event == 'Faceoff' or event_type == 'Save' or event_type == 'Block':
                player_C = ''
    
            if player_B != '' and livefeed_plays[i]["players"][1]["playerType"] == 'Goalie':
                player_B = ''
    
            if player_C != '' and livefeed_plays[i]["players"][2]["playerType"] == 'Goalie':
                player_C = ''

            if int(season_id) >= 20102011:    
                ### list of teams known to need their xy coordinates flipped (e.g. X recorded as 1 should be -1 and Y recorded as -25 should be 25)
                teams_flippedXY = ['ANA', 'ARI', 'BOS', 'BUF', 'CBJ', 'EDM', 'NJD', 'NSH', 'NYI', 'OTT', 'PIT', 'SJS', 'STL', 'TBL']
        
                ### change which team is credited for a blocked shot
                if event_type == 'Block' and team == home:
                    team = away
                elif event_type == 'Block' and team == away:
                    team = home
        
                if home == teams_flippedXY[0] or home == teams_flippedXY[1] or home == teams_flippedXY[2] or home == teams_flippedXY[3] or home == teams_flippedXY[4] or home == teams_flippedXY[5] or home == teams_flippedXY[6] or home == teams_flippedXY[7] or home == teams_flippedXY[8] or home == teams_flippedXY[9] or home == teams_flippedXY[10] or home == teams_flippedXY[11] or home == teams_flippedXY[12] or home == teams_flippedXY[13]:
                    x_1 *= -1
                    y_1 *= -1
                    x_2 *= -1
                    y_2 *= -1
        
                 ### flip the XY values of the 2nd period and OT events
                if livefeed_plays[i]["about"]["period"] == 2:
                    x_1 *= -1
                    y_1 *= -1
                    x_2 *= -1
                    y_2 *= -1
        
                 ### flip the XY values of the 2nd period and OT events
                if livefeed_plays[i]["about"]["period"] == 4:
                    x_1 *= -1
                    y_1 *= -1
                    x_2 *= -1
                    y_2 *= -1
        
                ### determine the zone the event occured in
                if x_1 == '':
                    home_zone = ''
                    away_zone = ''
                elif int(x_1) > -25 and int(x_1) < 25:
                    home_zone = 'Neutral'
                    away_zone = 'Neutral'
                elif team == home and int(x_1) < -25:
                    home_zone = 'Offensive'
                    away_zone = 'Defensive'
                elif team == home and int(x_1) > 25:
                    home_zone = 'Defensive'
                    away_zone = 'Offensive'
                elif team == away and int(x_1) < -25:
                    home_zone = 'Offensive'
                    away_zone = 'Defensive'
                elif team == away and int(x_1) > 25:
                    home_zone = 'Defensive'
                    away_zone = 'Offensive'
        
                if x_2 == '':
                    home_zone = home_zone
                    away_zone = away_zone
                elif team == home and event_type == 'Block':
                    home_zone = 'Offensive'
                    away_zone = 'Defensive'
                elif team == away and event_type == 'Block':
                    home_zone = 'Defensive'
                    away_zone = 'Offensive'
    
            ### skip over certain lines
            if event == 'Game.Scheduled' or event == 'Game.Official' or event == 'Period.Ready' or event == 'Period.Official' or event == 'Early.Intermission.Start' or event == 'Early.Intermission.End' or event == 'Emergency.Goaltender' or event == 'Official.Challenge' or event == 'Shootout.End' or event == 'Game.End':
                continue
    
            ### change the attacking player who took a blocked shot from PlayerB to PlayerA and the defending player who blocked the shot from PlayerA to PlayerB
            player_blocker = player_A
            player_shooter = player_B
    
            if event_type == 'Block':
                player_A = player_shooter
                player_B = player_blocker

            if int(season_id) >= 20102011:
                ### insert the game info and modified play-by-play data
                csvWriter.writerow((season_id, game_id, date, home, away, game_type, home_result, away_result, period, seconds_gone, time_left, time_gone, livefeed_plays[i]["about"]["goals"]["home"], livefeed_plays[i]["about"]["goals"]["away"], home_situation, away_situation, event, event_type, event_detail, team, home_zone, away_zone, player_A, player_B, player_C, x_1, y_1, x_2, y_2))

            if int(season_id) < 20102011:
                ### insert the game info and modified play-by-play data
                csvWriter.writerow((season_id, game_id, date, home, away, game_type, home_result, away_result, period, seconds_gone, time_left, time_gone, livefeed_plays[i]["about"]["goals"]["home"], livefeed_plays[i]["about"]["goals"]["away"], home_situation, away_situation, event, event_type, event_detail, team, player_A, player_B, player_C))
         
            
    print('Finished parsing NHL play-by-play from .json for ' + season_id + ' ' + game_id)