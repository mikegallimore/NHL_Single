# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 23:55:23 2018

@author: @mikegallimore
"""

import requests
import parameters

### pull common variables from the parameters file
season_id = parameters.season_id
game_id = parameters.game_id
files_root = parameters.files_root

### retrieve HTM rosters
try:
    ROS_content = requests.get('http://www.nhl.com/scores/htmlreports/' + season_id + '/RO0' + game_id + '.HTM', timeout=5).text
    if(len(ROS_content) < 10000):
        raise Exception
    f = open(files_root + 'rosters.HTM', 'w+')
    f.write(ROS_content)
    f.close()
    print('Retrieved NHL rosters (HTM) for ' + season_id + ' ' + game_id)
except:
    print('ERROR: Could not retrieve NHL rosters (HTM) for ' + season_id + ' ' + game_id)

### retrieve HTM play-by-play
try:
    PBP_content = requests.get('http://www.nhl.com/scores/htmlreports/' + season_id + '/PL0' + game_id + '.HTM', timeout=5).text
    if(len(ROS_content) < 10000):
        raise Exception
    f = open(files_root + 'pbp.HTM', 'w+')
    f.write(PBP_content)
    f.close()
    print('Retrieved NHL play-by-play (HTM) for ' + season_id + ' ' + game_id)
except:
    print('ERROR: Could not retrieve NHL play-by-play (HTM) for ' + season_id + ' ' + game_id)

### retrieve HTM home shift charts
try:
    TH0_content = requests.get('http://www.nhl.com/scores/htmlreports/' + season_id + '/TH0' + game_id + '.HTM', timeout=5).text
    if(len(TH0_content) < 10000):
        raise Exception
    f = open(files_root + 'shifts_home.HTM', 'w+')
    f.write(TH0_content)
    f.close()
    print('Retrieved NHL shifts (THO, HTM) for ' + season_id + ' ' + game_id)
except:
    print('ERROR: Could not retrieve NHL shifts (THO, HTM) for ' + season_id + ' ' + game_id)

### retrieve HTM visitor shift charts
try:
    TV0_content = requests.get('http://www.nhl.com/scores/htmlreports/' + season_id + '/TV0' + game_id + '.HTM', timeout=5).text
    if(len(TV0_content) < 10000):
        raise Exception
    f = open(files_root +'shifts_away.HTM', 'w+')
    f.write(TV0_content)
    f.close()
    print('Retrieved NHL shifts (TVI, HTM) for ' + season_id + ' ' + game_id)
except:
    print('ERROR: Could not retrieve NHL shifts (TVI, HTM) for ' + season_id + ' ' + game_id)

### retrieve JSON livefeed
try:
    JSON_content = requests.get('http://statsapi.web.nhl.com/api/v1/game/' + season_id[0:4] + '0' + game_id + '/feed/live', timeout=5).text
    if(len(JSON_content) < 1000):
        raise Exception
    f = open(files_root + 'livefeed.json', 'w+')
    f.write(JSON_content)
    f.close()
    print('Retrieved NHL livefeed (JSON) for ' + season_id + ' ' + game_id)
except:
    print('ERROR: Could not retrieve NHL livefeed (JSON) ' + season_id + ' ' + game_id)

### retrieve JSON shifts
try:
    JSON_content = requests.get('http://www.nhl.com/stats/rest/shiftcharts?cayenneExp=gameId=' + season_id[0:4] + '0' + game_id, timeout=5).text
    if(len(JSON_content) < 1000):
        raise Exception
    f = open(files_root + 'shifts.json', 'w+')
    f.write(JSON_content)
    f.close()
    print('Retrieved NHL shifts (JSON) for ' + season_id + ' ' + game_id)
except:
    print('ERROR: Could not retrieve NHL shifts (JSON) for ' + season_id + ' ' + game_id)