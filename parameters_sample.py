# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 20:40:14 2017

@author: @mikegallimore
"""
season_id = '20182019'
game_id = '21243'

### url roots for game files (JSON)
livefeed_root = 'http://statsapi.web.nhl.com/api/v1/game/'
shifts_root = 'http://www.nhl.com/stats/rest/shiftcharts?cayenneExp=gameId='
ROS_root = 'http://www.nhl.com/scores/htmlreports/' + season_id + '/RO0'

### root file locations
files_root = '/your/path/NHL_Tools/Single_Game/Files/'
charts_root = '/your/path/NHL_Tools/Single_Game/Charts/'

charts_players = charts_root + 'Players/'

charts_teams = charts_root + 'Teams/'
charts_teams_period = charts_teams + 'Period/'
charts_teams_situation = charts_teams + 'Situation/'

charts_units = charts_root + 'Units/'