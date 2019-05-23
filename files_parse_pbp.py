# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

from bs4 import BeautifulSoup
import json
import csv
import parameters
import pandas as pd
import dict_names
import dict_penalties
import dict_teams

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
    livefeed_source = files_root + 'livefeed.json'
    livefeed_outfile = files_root + 'livefeed.csv'
    pbp_source = files_root + 'pbp.HTM'
    pbp_outfile = files_root + 'pbp.csv'
    
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
    ### PLAY-BY-PLAY (HTM)
    ###
    
    ### trigger the files that will be read from and written to; write column titles to a header row
    with open(pbp_source, 'r') as HTM_pbp_source, open(pbp_outfile, 'w', newline = '') as HTM_pbp:
    
        csvWriter = csv.writer(HTM_pbp)
        csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'SECONDS_GONE', 'TIME_LEFT', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
    
        csvRows = ([])
        
        ### create a BeautifulSoup object to parse the HTM pbp file
        pbpSoup = BeautifulSoup(HTM_pbp_source, 'html.parser')
    
        home_table = pbpSoup.find('table', id='Home')
        home_goals_row = home_table.find('td', attrs={'style':'font-size: 40px;font-weight:bold'})
        for row in home_goals_row:
            home_goals = row
    
        away_table = pbpSoup.find('table', id='Visitor')
        away_goals_row = away_table.find('td', attrs={'style':'font-size: 40px;font-weight:bold'})
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
    
        event_rows = pbpSoup.find_all('tr', attrs={'class':'evenColor'})
    
        ### loop through the event rows
        for row in range(len(event_rows)):
            get_rows = event_rows[row]
            get_tds = get_rows.find_all('td')
      
            period = get_tds[1].string
    
            time = get_tds[3].get_text()
            time_index = time.find(':')
            time_left = time[time_index+3:]
            time_gone = time[:time_index+3]
       
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
    
            try:
                if event == 'Penalty':
                    event_type = description.split('\xa0')
                    event_type = event_type[1].split('(')
                    event_type = event_type[1].split(' ')
                    event_type = event_type[0].replace('2', 'Minor').replace('4', 'Double.Minor').replace('5', 'Major').replace('10', 'Misconduct')
            except:
                event_type = ''
    
            try:
                if event == 'Penalty':
                    event_detail = description.split('\xa0')
                    event_detail = event_detail[1].split('(')
                    event_detail = event_detail[0]
                    event_detail = dict_penalties.PENALTIES[event_detail]
            except:
                event_detail = ''
    
            ### get the player who was credited either with taking a shot, winning a faceoff, delivering a hit, giving up / taking away the puck or committing a penalty
            player_A = str()
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
    
            ### create a tuple of the information to be written and add to csvRows
            pbpTup = [(season_id, game_id, date, home, away, game_type, home_result, away_result, period, seconds_gone, time_left, time_gone, home_goals, away_goals, home_situation, away_situation, home_scorediff, away_scorediff, home_strength, away_strength, home_state, away_state, event, event_type, event_detail, team, player_A, player_B, player_C, homeON_1, homeON_2, homeON_3, homeON_4, homeON_5, homeON_6, awayON_1, awayON_2, awayON_3, awayON_4, awayON_5, awayON_6)]
    
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
    
    ### clean up instances where home players are listed in away player on-ice columns when the away team is shorthanded
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
    pbp_df.to_csv(pbp_outfile, index = False)
    
    print('Finished parsing NHL play-by-play from .HTM for ' + season_id + ' ' + game_id)
    
    
    ###
    ### LIVEFEED PLAY-BY-PLAY (JSON)
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
    
        csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'SECONDS_GONE', 'TIME_LEFT', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'TEAM', 'HOME_ZONE', 'AWAY_ZONE', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'X_1', 'Y_1', 'X_2', 'Y_2'])
    
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
    
            ### insert the game info and modified play-by-play data
            csvWriter.writerow((season_id, game_id, date, home, away, game_type, home_result, away_result, period, seconds_gone, time_left, time_gone, livefeed_plays[i]["about"]["goals"]["home"], livefeed_plays[i]["about"]["goals"]["away"], home_situation, away_situation, event, event_type, event_detail, team, home_zone, away_zone, player_A, player_B, player_C, x_1, y_1, x_2, y_2))
    
    print('Finished parsing NHL play-by-play from .json for ' + season_id + ' ' + game_id)