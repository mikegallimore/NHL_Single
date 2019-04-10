# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 22:10:14 2018

@author: @mikegallimore
"""

from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import parameters
import dict_names
import dict_teams

### pull common variables from the parameters file
season_id = parameters.season_id
game_id = parameters.game_id
date = parameters.date
home = parameters.home
away = parameters.away
teams = parameters.teams
files_root = parameters.files_root

### establish file locations and destinations
livefeed_file = files_root + 'livefeed.json'
away_shifts_file = files_root + 'shifts_away.HTM'
home_shifts_file = files_root + 'shifts_home.HTM'
shifts_outfile = files_root + 'shifts.csv'

### access the game's roster file in order to create team-specific lists
rosters_csv = files_root + 'rosters.csv'

rosters_df = pd.read_csv(rosters_csv)

rosters_table = rosters_df[['TEAM','PLAYER_NO', 'PLAYER_NAME', 'PLAYER_POS']]

awayROS_df = rosters_table.copy()
awayROS_df = awayROS_df[(awayROS_df['TEAM'] == away)]
awayROS_list = awayROS_df['PLAYER_NAME'].tolist()

awayG_df = rosters_table.copy()
awayG_df = awayG_df[(awayG_df.TEAM == away) & (awayG_df.PLAYER_POS == 'G')]
awayG = awayG_df['PLAYER_NAME'].tolist()

homeROS_df = rosters_table.copy()
homeROS_df = homeROS_df[(homeROS_df['TEAM'] == home)]
homeROS_list = homeROS_df['PLAYER_NAME'].tolist()

homeG_df = rosters_table.copy()
homeG_df = homeG_df[(homeG_df.TEAM == home) & (homeG_df.PLAYER_POS == 'G')]
homeG = homeG_df['PLAYER_NAME'].tolist()

### open the game's livefeed (JSON) file to create a few shared variables
with open(livefeed_file) as livefeed_json:
    livefeed_data = json.load(livefeed_json)
    livefeed_parsed = livefeed_data

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

###
### AWAY SHIFTS
###
        
### trigger the files that will be read from and written to
with open(away_shifts_file, 'r') as away_shifts, open(shifts_outfile, 'w', newline='') as shifts_out:

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
with open(home_shifts_file, 'r') as home_shifts, open(shifts_outfile, 'a', newline='') as shifts_out:

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


### reload the newly minted csv file for some final touches
try:
    shifts_df = pd.read_csv(shifts_outfile)

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
    shifts_df.loc[(shifts_df.PLAYER_NAME == 'VELDE,.VANDE'),['PLAYER_NAME']] = 'CHRIS.VANDE.VELDE'; shifts_df
    shifts_df.loc[(shifts_df.PLAYER_NAME == 'DER.VAN'),['PLAYER_NAME']] = 'DAVID.VAN.DER.GULIK'; shifts_df
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

except:
    shifts_df = pd.read_csv(shifts_outfile, encoding='latin-1')

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


print('Finished parsing NHL shifts from .HTM for ' + season_id + ' ' + game_id)