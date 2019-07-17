# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import numpy as np
import parameters
import dict_names
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
    livefeed_file = files_root + 'livefeed.json'
    away_shifts_infile = files_root + 'shifts_away.HTM'
    home_shifts_infile = files_root + 'shifts_home.HTM'
    away_shifts_outfile = files_root + 'shifts_away.csv'
    home_shifts_outfile = files_root + 'shifts_home.csv'   
    shifts_outfile = files_root + 'shifts.csv'
    
    ### access the game's roster file in order to create team-specific lists
    rosters_csv = files_root + 'rosters.csv'
    
    rosters_df = pd.read_csv(rosters_csv)
    
    rosters_table = rosters_df[['TEAM','PLAYER_NO', 'PLAYER_NAME', 'PLAYER_POS']]
    
    awayROS_df = rosters_table.copy()
    awayROS_df = awayROS_df[(awayROS_df['TEAM'] == away)]
    awayROS_dict = awayROS_df[['PLAYER_NO', 'PLAYER_NAME']].set_index('PLAYER_NO').T.to_dict('list')
    
    awayG_df = rosters_table.copy()
    awayG_df = awayG_df[(awayG_df.TEAM == away) & (awayG_df.PLAYER_POS == 'G')]
    awayG = awayG_df['PLAYER_NAME'].tolist()
    
    homeROS_df = rosters_table.copy()
    homeROS_df = homeROS_df[(homeROS_df['TEAM'] == home)]
    homeROS_dict = homeROS_df[['PLAYER_NO', 'PLAYER_NAME']].set_index('PLAYER_NO').T.to_dict('list')

    
    homeG_df = rosters_table.copy()
    homeG_df = homeG_df[(homeG_df.TEAM == home) & (homeG_df.PLAYER_POS == 'G')]
    homeG = homeG_df['PLAYER_NAME'].tolist()
    
    ### open the game's livefeed (JSON) file to create a few shared variables
    with open(livefeed_file) as livefeed_json:
        livefeed_data = json.load(livefeed_json)
    
        current_period = livefeed_data["liveData"]["linescore"]["currentPeriod"]
        current_time_remaining = livefeed_data["liveData"]["linescore"]["currentPeriodTimeRemaining"]
        
        time_remaining_min = 0
        time_remaining_sec = 0
    
        try:
            time_remaining_min = int(current_time_remaining.split(':')[0])
            time_remaining_sec = int(current_time_remaining.split(':')[1])
        except:
            pass
    
        if current_period == 1 and current_time_remaining != 'END':
            current_seconds_gone = 1200 - ((time_remaining_min * 60) + time_remaining_sec)
        elif current_period ==1 and current_time_remaining == 'END':
            current_seconds_gone = 1200
        if current_period == 2 and current_time_remaining != 'END':
            current_seconds_gone = 2400 - ((time_remaining_min * 60) + time_remaining_sec)
        elif current_period == 2 and current_time_remaining == 'END':
            current_seconds_gone = 2400
        if current_period == 3 and current_time_remaining != 'Final':
            current_seconds_gone = 3600 - ((time_remaining_min * 60) + time_remaining_sec)
        elif current_period == 4 and current_time_remaining != 'Final':
            current_seconds_gone = 3900 - ((time_remaining_min * 60) + time_remaining_sec)
    
    ###
    ### SHIFTS (.HTM)
    ###

    if int(season_id) >= 20072008:
    
        ###
        ### AWAY SHIFTS
        ###
               
        ### trigger the files that will be read from and written to
        with open(away_shifts_infile, 'r') as away_shifts, open(shifts_outfile, 'w', newline='') as shifts_out:
        
            csvWriter = csv.writer(shifts_out)
            csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'PLAYER_NO', 'PLAYER_NAME', 'PERIOD', 'SHIFT_NO', 'SHIFT_START', 'SHIFT_STOP'])
                
            csvRows = ([])
              
            ### create a BeautifulSoup object to parse the HTM shifts file
            shiftsSoup = BeautifulSoup(away_shifts, 'html.parser')
        
            Visitor_table = shiftsSoup.find('table', id='Visitor')
            Visitor_rows = Visitor_table.find_all('tr')
            for tr in Visitor_rows[3:4]:
                Visitor_td = tr.find_all('td')
                Visitor_row = [i.text for i in Visitor_td]
                try:
                    Visitor1 = Visitor_row[0].split('Game')
                    away1 = Visitor1[0]
                    away = dict_teams.NHL[away1]
                except:
                    Visitor2 = Visitor_row[0].split('Match/')
                    away2 = Visitor2[0]
                    away = dict_teams.NHL[away2]
        
                ### create a list of all the rows in the .HTM file
                rowList = shiftsSoup.find_all('tr')
        
                for i in range(len(rowList)-1):
                    row = rowList[i]
        
                    ### the header row of a player's shift table has a td of class playerHeading
                    if row.find('td'):
                        try:
                            rowClass = row.find('td')['class']
                        except:
                            rowClass = []
        
                        ### if a player's shift table is found, determine the player's position and get shift info
                        if 'playerHeading' in rowClass:
                            player = row.find('td').string.split(' ')
                            player_firstname = player[2]
                            player_lastname = player[1].replace(',', '')
                            player_name = player_firstname + '.' + player_lastname
                            player_no = player[0]
                            i += 2
                            row = rowList[i]
        
                            ### each row that contains shift info is of class evenColor or oddColor
                            try:
                                rowClass = row['class']
                            except:
                                rowClass = []
        
                            ### iterate through the next rows and pull shift information out of the shift rows
                            while ('evenColor' in rowClass or 'oddColor' in rowClass):
                                tds = row.find_all('td')
                                shiftNo = tds[0].string
        
                                ### get the period number. Regular season OT should be changed to period 4
                                period = int(tds[1].string) if tds[1].string != 'OT' else 4
        
                                ### get shift start and end and change the times to seconds from start of game
                                shiftStart = tds[2].string.split(' / ')[0].split(':')
                                shiftEnd = tds[3].string.split(' / ')[0].split(':')
                                duration = tds[4].string.split(' / ')[0].split(':')
                                try:
                                    shiftStart = 1200 * (period - 1) + 60 * int(shiftStart[0]) + int(shiftStart[1])
                                except:
                                    duration = 1200 * (period - 1) + 60 * int(duration[0]) + int(duration[1])
                                    shiftStart = shiftEnd - duration
                                try:
                                    shiftEnd = 1200 * (period - 1) + 60 * int(shiftEnd[0]) + int(shiftEnd[1])
                                except:
                                    duration = 1200 * (period - 1) + 60 * int(duration[0]) + int(duration[1])
                                    shiftEnd = shiftStart + duration
        
                                ### create a shift tuple of the information to be written and add to csvRows
                                shiftTup = [(season_id, game_id, date, 'Away', away, player_no, player_name, period, shiftNo, shiftStart, shiftEnd)]
                                csvRows += shiftTup
                                i += 1
                                row = rowList[i]
                                try:
                                    rowClass = row['class']
                                except:
                                    rowClass = []
        
                            ### insert a shift for the goalie if there is still time remaining in the period (only completed shifts are recorded)
                            if current_period == 1 and current_time_remaining != 'END' and player_name in awayG:
                                current_awayG_shift = (season_id, game_id, date, 'Away', away, player_no, player_name, current_period, 1, 0, current_seconds_gone)
                            elif current_period == 2 and current_time_remaining != 'END' and player_name in awayG:
                                current_awayG_shift = (season_id, game_id, date, 'Away', away, player_no, player_name, current_period, 2, 1201, current_seconds_gone)
                            elif current_period == 3 and current_time_remaining != 'Final' and player_name in awayG:
                                current_awayG_shift = (season_id, game_id, date, 'Away', away, player_no, player_name, current_period, 3, 2401, current_seconds_gone)
                            elif current_period == 4 and current_time_remaining != 'Final' and player_name in awayG:
                                current_awayG_shift = (season_id, game_id, date, 'Away', away, player_no, player_name, current_period, 4, 3601, current_seconds_gone)
            
                ### write the rows of shifts to the csv file
                csvWriter.writerows(csvRows)
                try:
                    if current_time_remaining != 'END' and current_time_remaining != 'Final':
                        csvWriter.writerow(current_awayG_shift)
                except:
                    pass
            
        ###
        ### HOME SHIFTS
        ###
        
        ### trigger the files that will be read from and written to
        with open(home_shifts_infile, 'r') as home_shifts, open(shifts_outfile, 'a', newline='') as shifts_out:
        
            csvWriter = csv.writer(shifts_out)
        
            csvRows = ([])
              
            ### create a BeautifulSoup object to parse the .HTM shifts file
            shiftsSoup = BeautifulSoup(home_shifts, 'html.parser')
        
            Home_table = shiftsSoup.find('table', id='Home')
            Home_rows = Home_table.find_all('tr')
            for tr in Home_rows[3:4]:
                Home_td = tr.find_all('td')
                Home_row = [i.text for i in Home_td]
                try:
                    Home1 = Home_row[0].split('Game')
                    home1 = Home1[0]
                    home = dict_teams.NHL[home1]
                except:
                    Home2 = Home_row[0].split('Match/')
                    home2 = Home2[0]
                    home = dict_teams.NHL[home2]
        
                ### create a list of all the rows in the .HTM file
                rowList = shiftsSoup.find_all('tr')
        
                for i in range(len(rowList)-1):
                    row = rowList[i]
        
                    ### the header row of a player's shift table has a td of class playerHeading
                    if row.find('td'):
                        try:
                            rowClass = row.find('td')['class']
                        except:
                            rowClass = []
        
                        ### if a player's shift table is found, determine the player's position and get shift info
                        if 'playerHeading' in rowClass:
                            player = row.find('td').string.split(' ')
                            player_firstname = player[2]
                            player_lastname = player[1].replace(',', '')
                                                    
                            player_name = player_firstname + '.' + player_lastname
                            player_no = player[0]
                            i += 2
                            row = rowList[i]
        
                            ### each row that contains shift info is of class evenColor or oddColor
                            try:
                                rowClass = row['class']
                            except:
                                rowClass = []
        
                            ### iterate through the next rows and pull shift information out of the shift rows
                            while ('evenColor' in rowClass or 'oddColor' in rowClass):
                                tds = row.find_all('td')
                                shiftNo = tds[0].string
        
                                ### get the period number. Regular season OT should be changed to period 4
                                period = int(tds[1].string) if tds[1].string != 'OT' else 4
        
                                ### gets shift start and end and change the times to seconds from start of game
                                shiftStart = tds[2].string.split(' / ')[0].split(':')
                                shiftEnd = tds[3].string.split(' / ')[0].split(':')
                                duration = tds[4].string.split(' / ')[0].split(':')
                                try:
                                    shiftStart = 1200 * (period - 1) + 60 * int(shiftStart[0]) + int(shiftStart[1])
                                except:
                                    duration = 1200 * (period - 1) + 60 * int(duration[0]) + int(duration[1])
                                    shiftStart = shiftEnd - duration
                                try:
                                    shiftEnd = 1200 * (period - 1) + 60 * int(shiftEnd[0]) + int(shiftEnd[1])
                                except:
                                    duration = 1200 * (period - 1) + 60 * int(duration[0]) + int(duration[1])
                                    shiftEnd = shiftStart + duration
        
                                ### create a shift tuple of the information to be written and add to csvRows
                                shiftTup = [(season_id, game_id, date, 'Home', home, player_no, player_name, period, shiftNo, shiftStart, shiftEnd)]
                                csvRows += shiftTup
                                i += 1
                                row = rowList[i]
                                try:
                                    rowClass = row['class']
                                except:
                                    rowClass = []
        
                            ### insert a shift for the goalie if there is still time remaining in the period (only completed shifts are recorded)
                            if current_period == 1 and current_time_remaining != 'END' and player_name in homeG:
                                current_homeG_shift = (season_id, game_id, date, 'Home', home, player_no, player_name, current_period, 1, 0, current_seconds_gone)
                            elif current_period == 2 and current_time_remaining != 'END' and player_name in homeG:
                                current_homeG_shift = (season_id, game_id, date, 'Home', home, player_no, player_name, current_period, 2, 1201, current_seconds_gone)
                            elif current_period == 3 and current_time_remaining != 'Final' and player_name in homeG:
                                current_homeG_shift = (season_id, game_id, date, 'Home', home, player_no, player_name, current_period, 3, 2401, current_seconds_gone)
                            elif current_period == 4 and current_time_remaining != 'Final' and player_name in homeG:
                                current_homeG_shift = (season_id, game_id, date, 'Home', home, player_no, player_name, current_period, 4, 3601, current_seconds_gone)
        
                ### write the rows of shifts to the csv file
                csvWriter.writerows(csvRows)

                try:
                    if current_time_remaining != 'END' and current_time_remaining != 'Final':
                        csvWriter.writerow(current_homeG_shift)
                except:
                    pass
    
    
    if int(season_id) == 20062007:

        ###
        ### AWAY SHIFTS
        ###
               
        ### trigger the files that will be read from and written to
        with open(away_shifts_infile, 'r') as away_shifts, open(away_shifts_outfile, 'w', newline='') as shifts_out:
        
            csvWriter = csv.writer(shifts_out)
            csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'PLAYER_NO', 'PLAYER_NAME', 'PERIOD', 'SHIFT_NO', 'SHIFT_START', 'SHIFT_STOP'])
             
            ### create a BeautifulSoup object to parse the .HTM shifts file
            shiftsSoup = BeautifulSoup(away_shifts, 'html.parser')

            ### pull the shifts for home and away teams        
            shifts_tables = shiftsSoup.find_all('table')[1:]

            for table in shifts_tables:
                
                away_elements = [i for i in table.select('font')[1:]]
                away_elements = away_elements[0].text.strip().replace('  ', ' ').replace('. ', '.').replace(' II', '.II').replace(' III', '.III').replace(' IV', '.IV').replace('DE ', '.').replace(' JR.', '.JR.').replace(' JR', '.JR.').replace('VAN ', '.').replace('VAN DER', '.')
                
                element_end = 1000
                while element_end != 0:
                    away_elements.replace(' ', ' ')
                    element_end -= 1
                    away_elements = away_elements.replace(' ', '_')

                away_elements = away_elements.split('\n\n')
               
                away_list = len(away_elements)
               
                ### loop through and pull the shift information for the players in the first half of each <font> tag within the <td>
                for i in range(0, away_list):
                    away_elements_split = away_elements[i].split('_')[0:5]
                    
                    player_no = ''
                    if away_elements_split[2] == '(F)' or away_elements_split[2] == '(C)' or away_elements_split[2] == '(L)' or away_elements_split[2] == '(R)' or away_elements_split[2] == '(D)' or away_elements_split[2] == '(G)':
                        player_no = away_elements_split[0]
                    if away_elements_split[3] == '(F)' or away_elements_split[3] == '(C)' or away_elements_split[3] == '(L)' or away_elements_split[3] == '(R)' or away_elements_split[3] == '(D)' or away_elements_split[3] == '(G)':
                        player_no = away_elements_split[1]
                    if away_elements_split[4] == '(F)' or away_elements_split[4] == '(C)' or away_elements_split[4] == '(L)' or away_elements_split[4] == '(R)' or away_elements_split[4] == '(D)' or away_elements_split[4] == '(G)':
                        player_no = away_elements_split[2]
                                      
                    player_name = ''                             
                    if away_elements_split[2] == '(F)' or away_elements_split[2] == '(C)' or away_elements_split[2] == '(L)' or away_elements_split[2] == '(R)' or away_elements_split[2] == '(D)' or away_elements_split[2] == '(G)':
                        player_name = away_elements_split[1]
                    if away_elements_split[3] == '(F)' or away_elements_split[3] == '(C)' or away_elements_split[3] == '(L)' or away_elements_split[3] == '(R)' or away_elements_split[3] == '(D)' or away_elements_split[3] == '(G)':
                        player_name = away_elements_split[2]
                    if away_elements_split[4] == '(F)' or away_elements_split[4] == '(C)' or away_elements_split[4] == '(L)' or away_elements_split[4] == '(R)' or away_elements_split[4] == '(D)' or away_elements_split[4] == '(G)':
                        player_no = away_elements_split[3]
         
                    period = ''
                    try:
                        if away_elements_split[2] == '(F)' or away_elements_split[2] == '(C)' or away_elements_split[2] == '(L)' or away_elements_split[2] == '(R)' or away_elements_split[2] == '(D)' or away_elements_split[2] == '(G)':
                            period = ''
                        if away_elements_split[3] == '(F)' or away_elements_split[3] == '(C)' or away_elements_split[3] == '(L)' or away_elements_split[3] == '(R)' or away_elements_split[3] == '(D)' or away_elements_split[3] == '(G)':
                            period = ''
                        if away_elements_split[4] == '(F)' or away_elements_split[4] == '(C)' or away_elements_split[4] == '(L)' or away_elements_split[4] == '(R)' or away_elements_split[4] == '(D)' or away_elements_split[4] == '(G)':
                            period = ''
                    except:
                        pass
                    try:
                        if len(away_elements_split[2]) == 8 and len(away_elements_split[3]) == 8:
                            period = away_elements_split[1]
                        if len(away_elements_split[3]) == 8 and len(away_elements_split[4]) == 8:
                            period = away_elements_split[2]
                    except:
                        pass

                    shift_start = 'NaN'
                    shift_end = 'NaN'
                    try:
                        if away_elements_split[2] == '(F)' or away_elements_split[2] == '(C)' or away_elements_split[2] == '(L)' or away_elements_split[2] == '(R)' or away_elements_split[2] == '(D)' or away_elements_split[2] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if away_elements_split[3] == '(F)' or away_elements_split[3] == '(C)' or away_elements_split[3] == '(L)' or away_elements_split[3] == '(R)' or away_elements_split[3] == '(D)' or away_elements_split[3] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if away_elements_split[4] == '(F)' or away_elements_split[4] == '(C)' or away_elements_split[4] == '(L)' or away_elements_split[4] == '(R)' or away_elements_split[4] == '(D)' or away_elements_split[4] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                    except:
                        pass
                    try:
                        if len(away_elements_split[2]) == 8 and len(away_elements_split[3]) == 8:
                            shift_start = away_elements_split[2]
                            shift_end = away_elements_split[3]
                        if len(away_elements_split[3]) == 8 and len(away_elements_split[4]) == 8:
                            shift_start = away_elements_split[3]
                            shift_end = away_elements_split[4]
                    except:
                        pass                    
                    try:
                        if away_elements_split[1] == '--':
                            continue
                        if away_elements_split[2] == '--':
                            continue
                        if away_elements_split[3] == '--':
                            continue
                    except:
                        pass 
                   
                    ### write the shift information for these players to file
                    csvWriter.writerow([season_id, game_id, date, 'Away', away, player_no, player_name, period, '', shift_start, shift_end])


                ### loop through and pull the shift information for the players in the second half of each <font> tag within the <td>
                for i in range(0, away_list):
                    away_elements_split = away_elements[i].replace('__', '_').split('_')[9:]

                    player_no = ''
                    try:
                        if away_elements_split[2] == '(F)' or away_elements_split[2] == '(C)' or away_elements_split[2] == '(L)' or away_elements_split[2] == '(R)' or away_elements_split[2] == '(D)' or away_elements_split[2] == '(G)':
                            player_no = away_elements_split[0]
                        if away_elements_split[3] == '(F)' or away_elements_split[3] == '(C)' or away_elements_split[3] == '(L)' or away_elements_split[3] == '(R)' or away_elements_split[3] == '(D)' or away_elements_split[3] == '(G)':
                            player_no = away_elements_split[1]
                        if away_elements_split[4] == '(F)' or away_elements_split[4] == '(C)' or away_elements_split[4] == '(L)' or away_elements_split[4] == '(R)' or away_elements_split[4] == '(D)' or away_elements_split[4] == '(G)':
                            player_no = away_elements_split[2]
                        if away_elements_split[5] == '(F)' or away_elements_split[5] == '(C)' or away_elements_split[5] == '(L)' or away_elements_split[5] == '(R)' or away_elements_split[5] == '(D)' or away_elements_split[5] == '(G)':
                            player_no = away_elements_split[3]
                        if away_elements_split[6] == '(F)' or away_elements_split[6] == '(C)' or away_elements_split[6] == '(L)' or away_elements_split[6] == '(R)' or away_elements_split[6] == '(D)' or away_elements_split[6] == '(G)':
                            player_no = away_elements_split[4] 
                        if away_elements_split[7] == '(F)' or away_elements_split[7] == '(C)' or away_elements_split[7] == '(L)' or away_elements_split[7] == '(R)' or away_elements_split[7] == '(D)' or away_elements_split[7] == '(G)':
                            player_no = away_elements_split[5]
                        if away_elements_split[8] == '(F)' or away_elements_split[8] == '(C)' or away_elements_split[8] == '(L)' or away_elements_split[8] == '(R)' or away_elements_split[8] == '(D)' or away_elements_split[8] == '(G)':
                            player_no = away_elements_split[6]
                    except:
                        pass
                    
                    player_name = ''                             
                    try:
                        if away_elements_split[2] == '(F)' or away_elements_split[2] == '(C)' or away_elements_split[2] == '(L)' or away_elements_split[2] == '(R)' or away_elements_split[2] == '(D)' or away_elements_split[2] == '(G)':
                            player_name = away_elements_split[1]
                        if away_elements_split[3] == '(F)' or away_elements_split[3] == '(C)' or away_elements_split[3] == '(L)' or away_elements_split[3] == '(R)' or away_elements_split[3] == '(D)' or away_elements_split[3] == '(G)':
                            player_name = away_elements_split[2]
                        if away_elements_split[4] == '(F)' or away_elements_split[4] == '(C)' or away_elements_split[4] == '(L)' or away_elements_split[4] == '(R)' or away_elements_split[4] == '(D)' or away_elements_split[4] == '(G)':
                            player_name = away_elements_split[3]
                        if away_elements_split[5] == '(F)' or away_elements_split[5] == '(C)' or away_elements_split[5] == '(L)' or away_elements_split[5] == '(R)' or away_elements_split[5] == '(D)' or away_elements_split[5] == '(G)':
                            player_name = away_elements_split[4]
                        if away_elements_split[6] == '(F)' or away_elements_split[6] == '(C)' or away_elements_split[6] == '(L)' or away_elements_split[6] == '(R)' or away_elements_split[6] == '(D)' or away_elements_split[6] == '(G)':
                            player_name = away_elements_split[5]
                        if away_elements_split[7] == '(F)' or away_elements_split[7] == '(C)' or away_elements_split[7] == '(L)' or away_elements_split[7] == '(R)' or away_elements_split[7] == '(D)' or away_elements_split[7] == '(G)':
                            player_name = away_elements_split[6]
                        if away_elements_split[8] == '(F)' or away_elements_split[8] == '(C)' or away_elements_split[8] == '(L)' or away_elements_split[8] == '(R)' or away_elements_split[8] == '(D)' or away_elements_split[8] == '(G)':
                            player_name = away_elements_split[7]
                    except:
                        pass
                                       
                    period = ''
                    try:
                        if away_elements_split[2] == '(F)' or away_elements_split[2] == '(C)' or away_elements_split[2] == '(L)' or away_elements_split[2] == '(R)' or away_elements_split[2] == '(D)' or away_elements_split[2] == '(G)':
                            period = ''
                        if away_elements_split[3] == '(F)' or away_elements_split[3] == '(C)' or away_elements_split[3] == '(L)' or away_elements_split[3] == '(R)' or away_elements_split[3] == '(D)' or away_elements_split[3] == '(G)':
                            period = ''
                        if away_elements_split[4] == '(F)' or away_elements_split[4] == '(C)' or away_elements_split[4] == '(L)' or away_elements_split[4] == '(R)' or away_elements_split[4] == '(D)' or away_elements_split[4] == '(G)':
                            period = ''
                        if away_elements_split[5] == '(F)' or away_elements_split[5] == '(C)' or away_elements_split[5] == '(L)' or away_elements_split[5] == '(R)' or away_elements_split[5] == '(D)' or away_elements_split[5] == '(G)':
                            period = ''
                        if away_elements_split[6] == '(F)' or away_elements_split[6] == '(C)' or away_elements_split[6] == '(L)' or away_elements_split[6] == '(R)' or away_elements_split[6] == '(D)' or away_elements_split[6] == '(G)':
                            period = ''
                        if away_elements_split[7] == '(F)' or away_elements_split[7] == '(C)' or away_elements_split[7] == '(L)' or away_elements_split[7] == '(R)' or away_elements_split[7] == '(D)' or away_elements_split[7] == '(G)':
                            period = ''
                        if away_elements_split[8] == '(F)' or away_elements_split[8] == '(C)' or away_elements_split[8] == '(L)' or away_elements_split[8] == '(R)' or away_elements_split[8] == '(D)' or away_elements_split[8] == '(G)':
                            period = ''
                    except:
                        pass
                    try:
                        if len(away_elements_split[2]) == 8 and len(away_elements_split[3]) == 8:
                            period = away_elements_split[1]
                        if len(away_elements_split[3]) == 8 and len(away_elements_split[4]) == 8:
                            period = away_elements_split[2]
                        if len(away_elements_split[4]) == 8 and len(away_elements_split[5]) == 8:
                            period = away_elements_split[3]
                        if len(away_elements_split[5]) == 8 and len(away_elements_split[6]) == 8:
                            period = away_elements_split[4]
                        if len(away_elements_split[6]) == 8 and len(away_elements_split[7]) == 8:
                            period = away_elements_split[5]
                        if len(away_elements_split[7]) == 8 and len(away_elements_split[8]) == 8:
                            period = away_elements_split[6]
                    except:
                        pass

                    shift_start = 'NaN'
                    shift_end = 'NaN'
                    try:
                        if away_elements_split[2] == '(F)' or away_elements_split[2] == '(C)' or away_elements_split[2] == '(L)' or away_elements_split[2] == '(R)' or away_elements_split[2] == '(D)' or away_elements_split[2] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if away_elements_split[3] == '(F)' or away_elements_split[3] == '(C)' or away_elements_split[3] == '(L)' or away_elements_split[3] == '(R)' or away_elements_split[3] == '(D)' or away_elements_split[3] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if away_elements_split[4] == '(F)' or away_elements_split[4] == '(C)' or away_elements_split[4] == '(L)' or away_elements_split[4] == '(R)' or away_elements_split[4] == '(D)' or away_elements_split[4] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if away_elements_split[5] == '(F)' or away_elements_split[5] == '(C)' or away_elements_split[5] == '(L)' or away_elements_split[5] == '(R)' or away_elements_split[5] == '(D)' or away_elements_split[5] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if away_elements_split[6] == '(F)' or away_elements_split[6] == '(C)' or away_elements_split[6] == '(L)' or away_elements_split[6] == '(R)' or away_elements_split[6] == '(D)' or away_elements_split[6] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if away_elements_split[7] == '(F)' or away_elements_split[7] == '(C)' or away_elements_split[7] == '(L)' or away_elements_split[7] == '(R)' or away_elements_split[7] == '(D)' or away_elements_split[7] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if away_elements_split[8] == '(F)' or away_elements_split[8] == '(C)' or away_elements_split[8] == '(L)' or away_elements_split[8] == '(R)' or away_elements_split[8] == '(D)' or away_elements_split[8] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                    except:
                        pass
                    try:
                        if len(away_elements_split[2]) == 8 and len(away_elements_split[3]) == 8:
                            shift_start = away_elements_split[2]
                            shift_end = away_elements_split[3]
                        if len(away_elements_split[3]) == 8 and len(away_elements_split[4]) == 8:
                            shift_start = away_elements_split[3]
                            shift_end = away_elements_split[4]
                        if len(away_elements_split[4]) == 8 and len(away_elements_split[5]) == 8:
                            shift_start = away_elements_split[4]
                            shift_end = away_elements_split[5]
                        if len(away_elements_split[5]) == 8 and len(away_elements_split[6]) == 8:
                            shift_start = away_elements_split[5]
                            shift_end = away_elements_split[6]
                        if len(away_elements_split[6]) == 8 and len(away_elements_split[7]) == 8:
                            shift_start = away_elements_split[6]
                            shift_end = away_elements_split[7]                       
                        if len(away_elements_split[7]) == 8 and len(away_elements_split[8]) == 8:
                            shift_start = away_elements_split[7]
                            shift_end = away_elements_split[8]
                    except:
                        pass                    
                    try:
                        if away_elements_split[3] == '--':
                            continue
                        if away_elements_split[4] == '--':
                            continue
                        if away_elements_split[5] == '--':
                            continue
                    except:
                        pass                   

                    ### write the shift information for these players to file                  
                    csvWriter.writerow([season_id, game_id, date, 'Away', away, player_no, player_name, period, '', shift_start, shift_end])


        ###
        ### HOME SHIFTS
        ###
               
        ### trigger the files that will be read from and written to
        with open(home_shifts_infile, 'r') as home_shifts, open(home_shifts_outfile, 'w', newline='') as shifts_out:
        
            csvWriter = csv.writer(shifts_out)
            csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'PLAYER_NO', 'PLAYER_NAME', 'PERIOD', 'SHIFT_NO', 'SHIFT_START', 'SHIFT_STOP'])
             
            ### create a BeautifulSoup object to parse the .HTM shifts file
            shiftsSoup = BeautifulSoup(home_shifts, 'html.parser')

            ### pull the shifts for home and away teams        
            shifts_tables = shiftsSoup.find_all('table')[1:]

            for table in shifts_tables:
                
                home_elements = [i for i in table.select('font')[1:]]
                home_elements = home_elements[0].text.strip().replace('  ', ' ').replace('. ', '.').replace(' II', '.II').replace(' III', '.III').replace(' IV', '.IV').replace('DE ', '.').replace(' JR.', '.JR.').replace(' JR', '.JR.').replace('VAN ', '.').replace('VAN DER', '.')
                
                element_end = 1000
                while element_end != 0:
                    home_elements.replace(' ', ' ')
                    element_end -= 1
                    home_elements = home_elements.replace(' ', '_')

                home_elements = home_elements.split('\n\n')
               
                home_list = len(home_elements)
               
                ### loop through and pull the shift information for the players in the first half of each <font> tag within the <td>
                for i in range(0, home_list):
                    home_elements_split = home_elements[i].split('_')[0:5]
                    
                    player_no = ''
                    if home_elements_split[2] == '(F)' or home_elements_split[2] == '(C)' or home_elements_split[2] == '(L)' or home_elements_split[2] == '(R)' or home_elements_split[2] == '(D)' or home_elements_split[2] == '(G)':
                        player_no = home_elements_split[0]
                    if home_elements_split[3] == '(F)' or home_elements_split[3] == '(C)' or home_elements_split[3] == '(L)' or home_elements_split[3] == '(R)' or home_elements_split[3] == '(D)' or home_elements_split[3] == '(G)':
                        player_no = home_elements_split[1]
                    if home_elements_split[4] == '(F)' or home_elements_split[4] == '(C)' or home_elements_split[4] == '(L)' or home_elements_split[4] == '(R)' or home_elements_split[4] == '(D)' or home_elements_split[4] == '(G)':
                        player_no = home_elements_split[2]
                                      
                    player_name = ''                             
                    if home_elements_split[2] == '(F)' or home_elements_split[2] == '(C)' or home_elements_split[2] == '(L)' or home_elements_split[2] == '(R)' or home_elements_split[2] == '(D)' or home_elements_split[2] == '(G)':
                        player_name = home_elements_split[1]
                    if home_elements_split[3] == '(F)' or home_elements_split[3] == '(C)' or home_elements_split[3] == '(L)' or home_elements_split[3] == '(R)' or home_elements_split[3] == '(D)' or home_elements_split[3] == '(G)':
                        player_name = home_elements_split[2]
                    if home_elements_split[4] == '(F)' or home_elements_split[4] == '(C)' or home_elements_split[4] == '(L)' or home_elements_split[4] == '(R)' or home_elements_split[4] == '(D)' or home_elements_split[4] == '(G)':
                        player_no = home_elements_split[3]
         
                    period = ''
                    try:
                        if home_elements_split[2] == '(F)' or home_elements_split[2] == '(C)' or home_elements_split[2] == '(L)' or home_elements_split[2] == '(R)' or home_elements_split[2] == '(D)' or home_elements_split[2] == '(G)':
                            period = ''
                        if home_elements_split[3] == '(F)' or home_elements_split[3] == '(C)' or home_elements_split[3] == '(L)' or home_elements_split[3] == '(R)' or home_elements_split[3] == '(D)' or home_elements_split[3] == '(G)':
                            period = ''
                        if home_elements_split[4] == '(F)' or home_elements_split[4] == '(C)' or home_elements_split[4] == '(L)' or home_elements_split[4] == '(R)' or home_elements_split[4] == '(D)' or home_elements_split[4] == '(G)':
                            period = ''
                    except:
                        pass
                    try:
                        if len(home_elements_split[2]) == 8 and len(home_elements_split[3]) == 8:
                            period = home_elements_split[1]
                        if len(home_elements_split[3]) == 8 and len(home_elements_split[4]) == 8:
                            period = home_elements_split[2]
                    except:
                        pass


                    shift_start = 'NaN'
                    shift_end = 'NaN'
                    try:
                        if home_elements_split[2] == '(F)' or home_elements_split[2] == '(C)' or home_elements_split[2] == '(L)' or home_elements_split[2] == '(R)' or home_elements_split[2] == '(D)' or home_elements_split[2] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if home_elements_split[3] == '(F)' or home_elements_split[3] == '(C)' or home_elements_split[3] == '(L)' or home_elements_split[3] == '(R)' or home_elements_split[3] == '(D)' or home_elements_split[3] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if home_elements_split[4] == '(F)' or home_elements_split[4] == '(C)' or home_elements_split[4] == '(L)' or home_elements_split[4] == '(R)' or home_elements_split[4] == '(D)' or home_elements_split[4] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                    except:
                        pass
                    try:
                        if len(home_elements_split[2]) == 8 and len(home_elements_split[3]) == 8:
                            shift_start = home_elements_split[2]
                            shift_end = home_elements_split[3]
                        if len(home_elements_split[3]) == 8 and len(home_elements_split[4]) == 8:
                            shift_start = home_elements_split[3]
                            shift_end = home_elements_split[4]
                    except:
                        pass                    
                    try:
                        if home_elements_split[1] == '--':
                            continue
                        if home_elements_split[2] == '--':
                            continue
                        if home_elements_split[3] == '--':
                            continue
                    except:
                        pass 

                    ### write the shift information for these players to file
                    csvWriter.writerow([season_id, game_id, date, 'Home', home, player_no, player_name, period, '', shift_start, shift_end])


                ### loop through and pull the shift information for the players in the second half of each <font> tag within the <td>
                for i in range(0, home_list):
                    home_elements_split = home_elements[i].replace('__', '_').split('_')[9:]

                    player_no = ''
                    try:
                        if home_elements_split[2] == '(F)' or home_elements_split[2] == '(C)' or home_elements_split[2] == '(L)' or home_elements_split[2] == '(R)' or home_elements_split[2] == '(D)' or home_elements_split[2] == '(G)':
                            player_no = home_elements_split[0]
                        if home_elements_split[3] == '(F)' or home_elements_split[3] == '(C)' or home_elements_split[3] == '(L)' or home_elements_split[3] == '(R)' or home_elements_split[3] == '(D)' or home_elements_split[3] == '(G)':
                            player_no = home_elements_split[1]
                        if home_elements_split[4] == '(F)' or home_elements_split[4] == '(C)' or home_elements_split[4] == '(L)' or home_elements_split[4] == '(R)' or home_elements_split[4] == '(D)' or home_elements_split[4] == '(G)':
                            player_no = home_elements_split[2]
                        if home_elements_split[5] == '(F)' or home_elements_split[5] == '(C)' or home_elements_split[5] == '(L)' or home_elements_split[5] == '(R)' or home_elements_split[5] == '(D)' or home_elements_split[5] == '(G)':
                            player_no = home_elements_split[3]
                        if home_elements_split[6] == '(F)' or home_elements_split[6] == '(C)' or home_elements_split[6] == '(L)' or home_elements_split[6] == '(R)' or home_elements_split[6] == '(D)' or home_elements_split[6] == '(G)':
                            player_no = home_elements_split[4]
                        if home_elements_split[7] == '(F)' or home_elements_split[7] == '(C)' or home_elements_split[7] == '(L)' or home_elements_split[7] == '(R)' or home_elements_split[7] == '(D)' or home_elements_split[7] == '(G)':
                            player_no = home_elements_split[5]
                        if home_elements_split[8] == '(F)' or home_elements_split[8] == '(C)' or home_elements_split[8] == '(L)' or home_elements_split[8] == '(R)' or home_elements_split[8] == '(D)' or home_elements_split[8] == '(G)':
                            player_no = home_elements_split[6]  
                    except:
                        pass
                    
                    player_name = ''                             
                    try:
                        if home_elements_split[2] == '(F)' or home_elements_split[2] == '(C)' or home_elements_split[2] == '(L)' or home_elements_split[2] == '(R)' or home_elements_split[2] == '(D)' or home_elements_split[2] == '(G)':
                            player_name = home_elements_split[1]
                        if home_elements_split[3] == '(F)' or home_elements_split[3] == '(C)' or home_elements_split[3] == '(L)' or home_elements_split[3] == '(R)' or home_elements_split[3] == '(D)' or home_elements_split[3] == '(G)':
                            player_name = home_elements_split[2]
                        if home_elements_split[4] == '(F)' or home_elements_split[4] == '(C)' or home_elements_split[4] == '(L)' or home_elements_split[4] == '(R)' or home_elements_split[4] == '(D)' or home_elements_split[4] == '(G)':
                            player_name = home_elements_split[3]
                        if home_elements_split[5] == '(F)' or home_elements_split[5] == '(C)' or home_elements_split[5] == '(L)' or home_elements_split[5] == '(R)' or home_elements_split[5] == '(D)' or home_elements_split[5] == '(G)':
                            player_name = home_elements_split[4]
                        if home_elements_split[6] == '(F)' or home_elements_split[6] == '(C)' or home_elements_split[6] == '(L)' or home_elements_split[6] == '(R)' or home_elements_split[6] == '(D)' or home_elements_split[6] == '(G)':
                            player_name = home_elements_split[5]
                        if home_elements_split[7] == '(F)' or home_elements_split[7] == '(C)' or home_elements_split[7] == '(L)' or home_elements_split[7] == '(R)' or home_elements_split[7] == '(D)' or home_elements_split[7] == '(G)':
                            player_name = home_elements_split[6]
                        if home_elements_split[8] == '(F)' or home_elements_split[8] == '(C)' or home_elements_split[8] == '(L)' or home_elements_split[8] == '(R)' or home_elements_split[8] == '(D)' or home_elements_split[8] == '(G)':
                            player_name = home_elements_split[7]
                    except:
                        pass
                                       
                    period = ''
                    try:
                        if home_elements_split[2] == '(F)' or home_elements_split[2] == '(C)' or home_elements_split[2] == '(L)' or home_elements_split[2] == '(R)' or home_elements_split[2] == '(D)' or home_elements_split[2] == '(G)':
                            period = ''
                        if home_elements_split[3] == '(F)' or home_elements_split[3] == '(C)' or home_elements_split[3] == '(L)' or home_elements_split[3] == '(R)' or home_elements_split[3] == '(D)' or home_elements_split[3] == '(G)':
                            period = ''
                        if home_elements_split[4] == '(F)' or home_elements_split[4] == '(C)' or home_elements_split[4] == '(L)' or home_elements_split[4] == '(R)' or home_elements_split[4] == '(D)' or home_elements_split[4] == '(G)':
                            period = ''
                        if home_elements_split[5] == '(F)' or home_elements_split[5] == '(C)' or home_elements_split[5] == '(L)' or home_elements_split[5] == '(R)' or home_elements_split[5] == '(D)' or home_elements_split[5] == '(G)':
                            period = ''
                        if home_elements_split[6] == '(F)' or home_elements_split[6] == '(C)' or home_elements_split[6] == '(L)' or home_elements_split[6] == '(R)' or home_elements_split[6] == '(D)' or home_elements_split[6] == '(G)':                            
                            period = ''
                        if home_elements_split[7] == '(F)' or home_elements_split[7] == '(C)' or home_elements_split[7] == '(L)' or home_elements_split[7] == '(R)' or home_elements_split[7] == '(D)' or home_elements_split[7] == '(G)':
                            period = ''
                        if home_elements_split[8] == '(F)' or home_elements_split[8] == '(C)' or home_elements_split[8] == '(L)' or home_elements_split[8] == '(R)' or home_elements_split[8] == '(D)' or home_elements_split[8] == '(G)':
                            period = ''
                    except:
                        pass
                    try:
                        if len(home_elements_split[2]) == 8 and len(home_elements_split[3]) == 8:
                            period = home_elements_split[1]
                        if len(home_elements_split[3]) == 8 and len(home_elements_split[4]) == 8:
                            period = home_elements_split[2]
                        if len(home_elements_split[4]) == 8 and len(home_elements_split[5]) == 8:
                            period = home_elements_split[3]
                        if len(home_elements_split[5]) == 8 and len(home_elements_split[6]) == 8:
                            period = home_elements_split[4]
                        if len(home_elements_split[6]) == 8 and len(home_elements_split[7]) == 8:
                            period = home_elements_split[5]
                        if len(home_elements_split[7]) == 8 and len(home_elements_split[8]) == 8:
                            period = home_elements_split[6]
                    except:
                        pass

                    shift_start = 'NaN'
                    shift_end = 'NaN'
                    try:
                        if home_elements_split[2] == '(F)' or home_elements_split[2] == '(C)' or home_elements_split[2] == '(L)' or home_elements_split[2] == '(R)' or home_elements_split[2] == '(D)' or home_elements_split[2] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if home_elements_split[3] == '(F)' or home_elements_split[3] == '(C)' or home_elements_split[3] == '(L)' or home_elements_split[3] == '(R)' or home_elements_split[3] == '(D)' or home_elements_split[3] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if home_elements_split[4] == '(F)' or home_elements_split[4] == '(C)' or home_elements_split[4] == '(L)' or home_elements_split[4] == '(R)' or home_elements_split[4] == '(D)' or home_elements_split[4] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if home_elements_split[5] == '(F)' or home_elements_split[5] == '(C)' or home_elements_split[5] == '(L)' or home_elements_split[5] == '(R)' or home_elements_split[5] == '(D)' or home_elements_split[5] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if home_elements_split[6] == '(F)' or home_elements_split[6] == '(C)' or home_elements_split[6] == '(L)' or home_elements_split[6] == '(R)' or home_elements_split[6] == '(D)' or home_elements_split[6] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if home_elements_split[7] == '(F)' or home_elements_split[7] == '(C)' or home_elements_split[7] == '(L)' or home_elements_split[7] == '(R)' or home_elements_split[7] == '(D)' or home_elements_split[7] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                        if home_elements_split[8] == '(F)' or home_elements_split[8] == '(C)' or home_elements_split[8] == '(L)' or home_elements_split[8] == '(R)' or home_elements_split[8] == '(D)' or home_elements_split[8] == '(G)':
                            shift_start = 'NaN'
                            shift_end = 'NaN'
                    except:
                        pass
                    try:
                        if len(home_elements_split[2]) == 8 and len(home_elements_split[3]) == 8:
                            shift_start = home_elements_split[2]
                            shift_end = home_elements_split[3]
                        if len(home_elements_split[3]) == 8 and len(home_elements_split[4]) == 8:
                            shift_start = home_elements_split[3]
                            shift_end = home_elements_split[4]
                        if len(home_elements_split[4]) == 8 and len(home_elements_split[5]) == 8:
                            shift_start = home_elements_split[4]
                            shift_end = home_elements_split[5]
                        if len(home_elements_split[5]) == 8 and len(home_elements_split[6]) == 8:
                            shift_start = home_elements_split[5]
                            shift_end = home_elements_split[6]
                        if len(home_elements_split[6]) == 8 and len(home_elements_split[7]) == 8:
                            shift_start = home_elements_split[6]
                            shift_end = home_elements_split[7]
                        if len(home_elements_split[7]) == 8 and len(home_elements_split[8]) == 8:
                            shift_start = home_elements_split[7]
                            shift_end = home_elements_split[8]
                    except:
                        pass                    
                    try:
                        if home_elements_split[3] == '--':
                            continue
                        if home_elements_split[4] == '--':
                            continue
                        if home_elements_split[5] == '--':
                            continue
                    except:
                        pass                   

                    ### write the shift information for these players to file                  
                    csvWriter.writerow([season_id, game_id, date, 'Home', home, player_no, player_name, period, '', shift_start, shift_end])

    ### reload the newly minted csv file for some final touches
    try:
        if int(season_id) >= 20072008:
            shifts_df = pd.read_csv(shifts_outfile)

            ### convert empty values into strings for easy removal
            shifts_df['SHIFT_START'].replace(np.nan, 'NaN', inplace=True)
            shifts_df['SHIFT_STOP'].replace(np.nan, 'NaN', inplace=True)            

            ### replace names for special name cases
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'SEBASTIAN.AHO') & (shifts_df.TEAM == 'CAR'),['PLAYER_NAME']] = 'SEBASTIAN.A.AHO'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'SEBASTIAN.AHO') & (shifts_df.TEAM == 'NYI'),['PLAYER_NAME']] = 'SEBASTIAN.J.AHO'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'COLLE,.DAL'),['PLAYER_NAME']] = 'MICHAEL.DAL.COLLE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'COSTA,.DA'),['PLAYER_NAME']] = 'STEPHANE.DA.COSTA'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'LA.DE'),['PLAYER_NAME']] = 'JACOB.DE.LA.ROSE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'LEO,.DE'),['PLAYER_NAME']] = 'CHASE.DE.LEO'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'EK,.ERIKSSON'),['PLAYER_NAME']] = 'JOEL.ERIKSSON.EK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'KARLSSON,.FORSBACKA'),['PLAYER_NAME']] = 'JAKOB.FORSBACKA.KARLSSON'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'GIUSEPPE,.DI'),['PLAYER_NAME']] = 'PHILLIP.DI.GIUSEPPE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'HAAN,.DE'),['PLAYER_NAME']] = 'CALVIN.DE.HAAN'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'III,.HILLEN'),['PLAYER_NAME']] = 'JACK.HILLEN'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'IV,.MEYER'),['PLAYER_NAME']] = 'FREDDY.MEYER'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'RIEMSDYK,.VAN') & (shifts_df.TEAM == 'PHI'),['PLAYER_NAME']] = 'JAMES.VAN.RIEMSDYK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'RIEMSDYK,.VAN') & (shifts_df.TEAM == 'TOR'),['PLAYER_NAME']] = 'JAMES.VAN.RIEMSDYK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'RIEMSDYK,.VAN') & (shifts_df.TEAM == 'CAR'),['PLAYER_NAME']] = 'TREVOR.VAN.RIEMSDYK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'RIEMSDYK,.VAN') & (shifts_df.TEAM == 'CHI'),['PLAYER_NAME']] = 'TREVOR.VAN.RIEMSDYK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'LOUIS,.ST'),['PLAYER_NAME']] = 'MARTIN.ST..LOUIS'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'LOUIS,.ST.'),['PLAYER_NAME']] = 'MARTIN.ST..LOUIS'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'PIERRE,.ST'),['PLAYER_NAME']] = 'MARTIN.ST..PIERRE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'PIERRE,.ST.'),['PLAYER_NAME']] = 'MARTIN.ST..PIERRE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'ROVERE,.DELLA'),['PLAYER_NAME']] = 'STEFAN.DELLA.ROVERE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'BRABANT,.VAN'),['PLAYER_NAME']] = 'BRYCE.VAN.BRABANT'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'DER.VAN'),['PLAYER_NAME']] = 'DAVID.VAN.DER.GULIK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'VELDE,.VANDE'),['PLAYER_NAME']] = 'CHRIS.VANDE.VELDE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'GUILDER,.VAN'),['PLAYER_NAME']] = 'MARK.VAN.GUILDER'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'RYN,.VAN'),['PLAYER_NAME']] = 'MIKE.VAN.RYN'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'VRIES,.DE'),['PLAYER_NAME']] = 'GREG.DE.VRIES'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'ZOTTO,.DEL'),['PLAYER_NAME']] = 'MICHAEL.DEL.ZOTTO'; shifts_df          
            
            ### change any player names that have been given specific styling
            shifts_df['PLAYER_NAME'] = shifts_df['PLAYER_NAME'].replace(dict_names.NAMES)
            
            ### delete rows with botched names
            shifts_df = shifts_df[shifts_df.PLAYER_NAME != '.']
                                
            ### save the adjusted dataframe to file
            shifts_df.to_csv(shifts_outfile, index = False)
    
        if int(season_id) == 20062007:
            away_shifts_df = pd.read_csv(away_shifts_outfile)
            home_shifts_df = pd.read_csv(home_shifts_outfile)
            
            ### convert empty values into strings for easy removal
            away_shifts_df['SHIFT_START'].replace(np.nan, 'NaN', inplace=True)
            away_shifts_df['SHIFT_STOP'].replace(np.nan, 'NaN', inplace=True)            
            home_shifts_df['SHIFT_START'].replace(np.nan, 'NaN', inplace=True)
            home_shifts_df['SHIFT_STOP'].replace(np.nan, 'NaN', inplace=True)            
                       
            ### change any player names that have been given specific styling
            away_shifts_df['PLAYER_NAME'] = away_shifts_df['PLAYER_NO'].replace(awayROS_dict)               
            home_shifts_df['PLAYER_NAME'] = home_shifts_df['PLAYER_NO'].replace(homeROS_dict)
            
            ### forward-fill empty player number and player name column rows with the last instance of each
            away_shifts_df['PLAYER_NO'] = away_shifts_df['PLAYER_NO'].replace(0,np.nan).ffill().astype(int)            
            away_shifts_df['PLAYER_NAME'] = away_shifts_df['PLAYER_NAME'].replace(0,np.nan).ffill().astype(str)
            home_shifts_df['PLAYER_NO'] = home_shifts_df['PLAYER_NO'].replace(0,np.nan).ffill().astype(int)            
            home_shifts_df['PLAYER_NAME'] = home_shifts_df['PLAYER_NAME'].replace(0,np.nan).ffill().astype(str)

            ### delete all rows that lack shift start and end times
            away_shifts_df = away_shifts_df[(away_shifts_df['SHIFT_START'] != 'NaN') & (away_shifts_df['SHIFT_STOP'] != 'NaN')]
            home_shifts_df = home_shifts_df[(home_shifts_df['SHIFT_START'] != 'NaN') & (home_shifts_df['SHIFT_STOP'] != 'NaN')]

            ### generate shift numbers
            away_shifts_df['SHIFT_NO'] = away_shifts_df.groupby((away_shifts_df['PLAYER_NAME'] != away_shifts_df['PLAYER_NAME'].shift(1)).cumsum()).cumcount()+1
            home_shifts_df['SHIFT_NO'] = home_shifts_df.groupby((home_shifts_df['PLAYER_NAME'] != home_shifts_df['PLAYER_NAME'].shift(1)).cumsum()).cumcount()+1
    
            ### remove extraneous formatting
            away_shifts_df['SHIFT_START'] = away_shifts_df['SHIFT_START'].str.split(':', 1).str.get(1)
            away_shifts_df['SHIFT_STOP'] = away_shifts_df['SHIFT_STOP'].str.split(':', 1).str.get(1)     

            home_shifts_df['SHIFT_START'] = home_shifts_df['SHIFT_START'].str.split(':', 1).str.get(1)
            home_shifts_df['SHIFT_STOP'] = home_shifts_df['SHIFT_STOP'].str.split(':', 1).str.get(1)     

            ### change shift start and end times to seconds from start of game
            away_shifts_regulation = away_shifts_df.copy()
            away_shifts_regulation = away_shifts_regulation[(away_shifts_regulation['PERIOD'] < 4)]               
            away_period = away_shifts_regulation['PERIOD']

            away_shifts_regulation['SHIFT_START'] = away_shifts_regulation['SHIFT_START'].str.split(':')
            away_shift_start_minutes = away_shifts_regulation['SHIFT_START'].str.get(0).astype(int)
            away_shift_start_seconds = away_shifts_regulation['SHIFT_START'].str.get(1).astype(int)
            away_shifts_regulation['SHIFT_START'] = (1200 * away_period) - ((60 * away_shift_start_minutes) + away_shift_start_seconds)

            away_shifts_regulation['SHIFT_STOP'] = away_shifts_regulation['SHIFT_STOP'].str.split(':')
            away_shift_end_minutes = away_shifts_regulation['SHIFT_STOP'].str.get(0).astype(int)
            away_shift_end_seconds = away_shifts_regulation['SHIFT_STOP'].str.get(1).astype(int)
            away_shifts_regulation['SHIFT_STOP'] = (1200 * away_period) - ((60 * away_shift_end_minutes) + away_shift_end_seconds)

            home_shifts_regulation = home_shifts_df.copy()
            home_shifts_regulation = home_shifts_regulation[(home_shifts_regulation['PERIOD'] < 4)]
            home_period = home_shifts_regulation['PERIOD']
            
            home_shifts_regulation['SHIFT_START'] = home_shifts_regulation['SHIFT_START'].str.split(':')
            home_shift_start_minutes = home_shifts_regulation['SHIFT_START'].str.get(0).astype(int)
            home_shift_start_seconds = home_shifts_regulation['SHIFT_START'].str.get(1).astype(int)
            home_shifts_regulation['SHIFT_START'] = (1200 * home_period) - ((60 * home_shift_start_minutes) + home_shift_start_seconds)

            home_shifts_regulation['SHIFT_STOP'] = home_shifts_regulation['SHIFT_STOP'].str.split(':')
            home_shift_end_minutes = home_shifts_regulation['SHIFT_STOP'].str.get(0).astype(int)
            home_shift_end_seconds = home_shifts_regulation['SHIFT_STOP'].str.get(1).astype(int)
            home_shifts_regulation['SHIFT_STOP'] = (1200 * home_period) - ((60 * home_shift_end_minutes) + home_shift_end_seconds)

            try:
                away_shifts_overtime = away_shifts_df.copy()
                away_shifts_overtime = away_shifts_overtime[(away_shifts_overtime['PERIOD'] == 4)] 
                
                away_shifts_overtime['SHIFT_START'] = away_shifts_overtime['SHIFT_START'].str.split(':')
                away_shift_start_minutes = away_shifts_overtime['SHIFT_START'].str.get(0).astype(int)
                away_shift_start_seconds = away_shifts_overtime['SHIFT_START'].str.get(1).astype(int)
                away_shifts_overtime['SHIFT_START'] = 3900 - ((60 * away_shift_start_minutes) + away_shift_start_seconds)

                away_shifts_overtime['SHIFT_STOP'] = away_shifts_overtime['SHIFT_STOP'].str.split(':')
                away_shift_end_minutes = away_shifts_overtime['SHIFT_STOP'].str.get(0).astype(int)
                away_shift_end_seconds = away_shifts_overtime['SHIFT_STOP'].str.get(1).astype(int)
                away_shifts_overtime['SHIFT_STOP'] = 3900 - ((60 * away_shift_end_minutes) + away_shift_end_seconds)
                
                away_shifts = pd.concat([away_shifts_regulation, away_shifts_overtime])
                away_shifts = away_shifts.sort_values(['PLAYER_NAME', 'PERIOD', 'SHIFT_NO'])

                home_shifts_overtime = home_shifts_df.copy()
                home_shifts_overtime = home_shifts_overtime[(home_shifts_overtime['PERIOD'] == 4)] 

                home_shifts_overtime['SHIFT_START'] = home_shifts_overtime['SHIFT_START'].str.split(':')
                home_shift_start_minutes = home_shifts_overtime['SHIFT_START'].str.get(0).astype(int)
                home_shift_start_seconds = home_shifts_overtime['SHIFT_START'].str.get(1).astype(int)
                home_shifts_overtime['SHIFT_START'] = 3900 - ((60 * home_shift_start_minutes) + home_shift_start_seconds)

                home_shifts_overtime['SHIFT_STOP'] = home_shifts_overtime['SHIFT_STOP'].str.split(':')
                home_shift_end_minutes = home_shifts_overtime['SHIFT_STOP'].str.get(0).astype(int)
                home_shift_end_seconds = home_shifts_overtime['SHIFT_STOP'].str.get(1).astype(int)
                home_shifts_overtime['SHIFT_STOP'] = 3900 - ((60 * home_shift_end_minutes) + home_shift_end_seconds)
                
                home_shifts = pd.concat([home_shifts_regulation, home_shifts_overtime])
                home_shifts = home_shifts.sort_values(['PLAYER_NAME', 'PERIOD', 'SHIFT_NO'])

                ### save the adjusted dataframes to file
                away_shifts.to_csv(away_shifts_outfile, index = False)
                home_shifts.to_csv(home_shifts_outfile, index = False)
            except:
                ### save the adjusted dataframes to file
                away_shifts = away_shifts_regulation
                home_shifts = home_shifts_regulation
                away_shifts.to_csv(away_shifts_outfile, index = False)
                home_shifts.to_csv(home_shifts_outfile, index = False)                    
                
            ### merge the separate shift files into one and save to file
            shifts_df = pd.concat([away_shifts, home_shifts])
            shifts_df.to_csv(shifts_outfile, index = False)                             

    except:
        if int(season_id) >= 20072008:    
            shifts_df = pd.read_csv(shifts_outfile, encoding='latin-1')

            ### convert empty values into strings for easy removal
            shifts_df['SHIFT_START'].replace(np.nan, 'NaN', inplace=True)
            shifts_df['SHIFT_STOP'].replace(np.nan, 'NaN', inplace=True)            

            ### replace names for special name cases
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'SEBASTIAN.AHO') & (shifts_df.TEAM == 'CAR'),['PLAYER_NAME']] = 'SEBASTIAN.A.AHO'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'SEBASTIAN.AHO') & (shifts_df.TEAM == 'NYI'),['PLAYER_NAME']] = 'SEBASTIAN.J.AHO'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'COLLE,.DAL'),['PLAYER_NAME']] = 'MICHAEL.DAL.COLLE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'COSTA,.DA'),['PLAYER_NAME']] = 'STEPHANE.DA.COSTA'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'LA.DE'),['PLAYER_NAME']] = 'JACOB.DE.LA.ROSE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'LEO,.DE'),['PLAYER_NAME']] = 'CHASE.DE.LEO'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'EK,.ERIKSSON'),['PLAYER_NAME']] = 'JOEL.ERIKSSON.EK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'KARLSSON,.FORSBACKA'),['PLAYER_NAME']] = 'JAKOB.FORSBACKA.KARLSSON'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'GIUSEPPE,.DI'),['PLAYER_NAME']] = 'PHILLIP.DI.GIUSEPPE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'HAAN,.DE'),['PLAYER_NAME']] = 'CALVIN.DE.HAAN'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'III,.HILLEN'),['PLAYER_NAME']] = 'JACK.HILLEN'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'IV,.MEYER'),['PLAYER_NAME']] = 'FREDDY.MEYER'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'RIEMSDYK,.VAN') & (shifts_df.TEAM == 'PHI'),['PLAYER_NAME']] = 'JAMES.VAN.RIEMSDYK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'RIEMSDYK,.VAN') & (shifts_df.TEAM == 'TOR'),['PLAYER_NAME']] = 'JAMES.VAN.RIEMSDYK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'RIEMSDYK,.VAN') & (shifts_df.TEAM == 'CAR'),['PLAYER_NAME']] = 'TREVOR.VAN.RIEMSDYK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'RIEMSDYK,.VAN') & (shifts_df.TEAM == 'CHI'),['PLAYER_NAME']] = 'TREVOR.VAN.RIEMSDYK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'LOUIS,.ST'),['PLAYER_NAME']] = 'MARTIN.ST..LOUIS'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'LOUIS,.ST.'),['PLAYER_NAME']] = 'MARTIN.ST..LOUIS'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'PIERRE,.ST'),['PLAYER_NAME']] = 'MARTIN.ST..PIERRE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'PIERRE,.ST.'),['PLAYER_NAME']] = 'MARTIN.ST..PIERRE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'ROVERE,.DELLA'),['PLAYER_NAME']] = 'STEFAN.DELLA.ROVERE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'BRABANT,.VAN'),['PLAYER_NAME']] = 'BRYCE.VAN.BRABANT'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'DER.VAN'),['PLAYER_NAME']] = 'DAVID.VAN.DER.GULIK'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'VELDE,.VANDE'),['PLAYER_NAME']] = 'CHRIS.VANDE.VELDE'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'GUILDER,.VAN'),['PLAYER_NAME']] = 'MARK.VAN.GUILDER'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'RYN,.VAN'),['PLAYER_NAME']] = 'MIKE.VAN.RYN'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'VRIES,.DE'),['PLAYER_NAME']] = 'GREG.DE.VRIES'; shifts_df
            shifts_df.loc[(shifts_df.PLAYER_NAME == 'ZOTTO,.DEL'),['PLAYER_NAME']] = 'MICHAEL.DEL.ZOTTO'; shifts_df          

            ### change any player names that have been given specific styling
            shifts_df['PLAYER_NAME'] = shifts_df['PLAYER_NAME'].replace(dict_names.NAMES)
            
            ### delete rows with botched names
            shifts_df = shifts_df[shifts_df.PLAYER_NAME != '.']
                                
            ### save the adjusted dataframe to file
            shifts_df.to_csv(shifts_outfile, index = False)

        if int(season_id) == 20062007:
            away_shifts_df = pd.read_csv(away_shifts_outfile, encoding='latin-1')
            home_shifts_df = pd.read_csv(home_shifts_outfile, encoding='latin-1')
            
            ### convert empty values into strings for easy removal
            away_shifts_df['SHIFT_START'].replace(np.nan, 'NaN', inplace=True)
            away_shifts_df['SHIFT_STOP'].replace(np.nan, 'NaN', inplace=True)            
            home_shifts_df['SHIFT_START'].replace(np.nan, 'NaN', inplace=True)
            home_shifts_df['SHIFT_STOP'].replace(np.nan, 'NaN', inplace=True)            
                       
            ### change any player names that have been given specific styling
            away_shifts_df['PLAYER_NAME'] = away_shifts_df['PLAYER_NO'].replace(awayROS_dict)               
            home_shifts_df['PLAYER_NAME'] = home_shifts_df['PLAYER_NO'].replace(homeROS_dict)
            
            ### make a duplicateforward-fill empty player number and player name column rows with the last instance of each
            away_shifts_df['PLAYER_NO'] = away_shifts_df['PLAYER_NO'].replace(0,np.nan).ffill().astype(int)            
            away_shifts_df['PLAYER_NAME'] = away_shifts_df['PLAYER_NAME'].replace(0,np.nan).ffill().astype(str)
            home_shifts_df['PLAYER_NO'] = home_shifts_df['PLAYER_NO'].replace(0,np.nan).ffill().astype(int)            
            home_shifts_df['PLAYER_NAME'] = home_shifts_df['PLAYER_NAME'].replace(0,np.nan).ffill().astype(str)

            ### delete all rows that lack shift start and end times
            away_shifts_df = away_shifts_df[(away_shifts_df['SHIFT_START'] != 'NaN') & (away_shifts_df['SHIFT_STOP'] != 'NaN')]
            home_shifts_df = home_shifts_df[(home_shifts_df['SHIFT_START'] != 'NaN') & (home_shifts_df['SHIFT_STOP'] != 'NaN')]

            ### generate shift numbers
            away_shifts_df['SHIFT_NO'] = away_shifts_df.groupby((away_shifts_df['PLAYER_NAME'] != away_shifts_df['PLAYER_NAME'].shift(1)).cumsum()).cumcount()+1
            home_shifts_df['SHIFT_NO'] = home_shifts_df.groupby((home_shifts_df['PLAYER_NAME'] != home_shifts_df['PLAYER_NAME'].shift(1)).cumsum()).cumcount()+1
    
            ### remove extraneous formatting
            away_shifts_df['SHIFT_START'] = away_shifts_df['SHIFT_START'].str.split(':', 1).str.get(1)
            away_shifts_df['SHIFT_STOP'] = away_shifts_df['SHIFT_STOP'].str.split(':', 1).str.get(1)     

            home_shifts_df['SHIFT_START'] = home_shifts_df['SHIFT_START'].str.split(':', 1).str.get(1)
            home_shifts_df['SHIFT_STOP'] = home_shifts_df['SHIFT_STOP'].str.split(':', 1).str.get(1)     

            ### change shift start and end times to seconds from start of game
            away_shifts_regulation = away_shifts_df.copy()
            away_shifts_regulation = away_shifts_regulation[(away_shifts_regulation['PERIOD'] < 4)]               
            away_period = away_shifts_regulation['PERIOD']

            away_shifts_regulation['SHIFT_START'] = away_shifts_regulation['SHIFT_START'].str.split(':')
            away_shift_start_minutes = away_shifts_regulation['SHIFT_START'].str.get(0).astype(int)
            away_shift_start_seconds = away_shifts_regulation['SHIFT_START'].str.get(1).astype(int)
            away_shifts_regulation['SHIFT_START'] = (1200 * away_period) - ((60 * away_shift_start_minutes) + away_shift_start_seconds)

            away_shifts_regulation['SHIFT_STOP'] = away_shifts_regulation['SHIFT_STOP'].str.split(':')
            away_shift_end_minutes = away_shifts_regulation['SHIFT_STOP'].str.get(0).astype(int)
            away_shift_end_seconds = away_shifts_regulation['SHIFT_STOP'].str.get(1).astype(int)
            away_shifts_regulation['SHIFT_STOP'] = (1200 * away_period) - ((60 * away_shift_end_minutes) + away_shift_end_seconds)

            home_shifts_regulation = home_shifts_df.copy()
            home_shifts_regulation = home_shifts_regulation[(home_shifts_regulation['PERIOD'] < 4)]
            home_period = home_shifts_regulation['PERIOD']
            
            home_shifts_regulation['SHIFT_START'] = home_shifts_regulation['SHIFT_START'].str.split(':')
            home_shift_start_minutes = home_shifts_regulation['SHIFT_START'].str.get(0).astype(int)
            home_shift_start_seconds = home_shifts_regulation['SHIFT_START'].str.get(1).astype(int)
            home_shifts_regulation['SHIFT_START'] = (1200 * home_period) - ((60 * home_shift_start_minutes) + home_shift_start_seconds)

            home_shifts_regulation['SHIFT_STOP'] = home_shifts_regulation['SHIFT_STOP'].str.split(':')
            home_shift_end_minutes = home_shifts_regulation['SHIFT_STOP'].str.get(0).astype(int)
            home_shift_end_seconds = home_shifts_regulation['SHIFT_STOP'].str.get(1).astype(int)
            home_shifts_regulation['SHIFT_STOP'] = (1200 * home_period) - ((60 * home_shift_end_minutes) + home_shift_end_seconds)

            try:
                away_shifts_overtime = away_shifts_df.copy()
                away_shifts_overtime = away_shifts_overtime[(away_shifts_overtime['PERIOD'] == 4)] 

                away_shifts_overtime['SHIFT_START'] = away_shifts_overtime['SHIFT_START'].str.split(':')
                away_shift_start_minutes = away_shifts_overtime['SHIFT_START'].str.get(0).astype(int)
                away_shift_start_seconds = away_shifts_overtime['SHIFT_START'].str.get(1).astype(int)
                away_shifts_overtime['SHIFT_START'] = 3900 - ((60 * away_shift_start_minutes) + away_shift_start_seconds)

                away_shifts_overtime['SHIFT_STOP'] = away_shifts_overtime['SHIFT_STOP'].str.split(':')
                away_shift_end_minutes = away_shifts_overtime['SHIFT_STOP'].str.get(0).astype(int)
                away_shift_end_seconds = away_shifts_overtime['SHIFT_STOP'].str.get(1).astype(int)
                away_shifts_overtime['SHIFT_STOP'] = 3900 - ((60 * away_shift_end_minutes) + away_shift_end_seconds)
                
                away_shifts = pd.concat([away_shifts_regulation, away_shifts_overtime])
                away_shifts = away_shifts.sort_values(['PLAYER_NAME', 'PERIOD', 'SHIFT_NO'])


                home_shifts_overtime = home_shifts_df.copy()
                home_shifts_overtime = home_shifts_overtime[(home_shifts_overtime['PERIOD'] == 4)] 

                home_shifts_overtime['SHIFT_START'] = home_shifts_overtime['SHIFT_START'].str.split(':')
                home_shift_start_minutes = home_shifts_overtime['SHIFT_START'].str.get(0).astype(int)
                home_shift_start_seconds = home_shifts_overtime['SHIFT_START'].str.get(1).astype(int)
                home_shifts_overtime['SHIFT_START'] = 3900 - ((60 * home_shift_start_minutes) + home_shift_start_seconds)

                home_shifts_overtime['SHIFT_STOP'] = home_shifts_overtime['SHIFT_STOP'].str.split(':')
                home_shift_end_minutes = home_shifts_overtime['SHIFT_STOP'].str.get(0).astype(int)
                home_shift_end_seconds = home_shifts_overtime['SHIFT_STOP'].str.get(1).astype(int)
                home_shifts_overtime['SHIFT_STOP'] = 3900 - ((60 * home_shift_end_minutes) + home_shift_end_seconds)
                
                home_shifts = pd.concat([home_shifts_regulation, home_shifts_overtime])
                home_shifts = home_shifts.sort_values(['PLAYER_NAME', 'PERIOD', 'SHIFT_NO'])

                ### save the adjusted dataframes to file
                away_shifts.to_csv(away_shifts_outfile, index = False)
                home_shifts.to_csv(home_shifts_outfile, index = False)
            except:
                ### save the adjusted dataframes to file
                away_shifts = away_shifts_regulation
                home_shifts = home_shifts_regulation
                away_shifts.to_csv(away_shifts_outfile, index = False)
                home_shifts.to_csv(home_shifts_outfile, index = False)                    
                
            ### merge the separate shift files into one and save to file
            shifts_df = pd.concat([away_shifts, home_shifts])
            shifts_df.to_csv(shifts_outfile, index = False)
                
                
    print('Finished parsing NHL shifts from .HTM for ' + season_id + ' ' + game_id)