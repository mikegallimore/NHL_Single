# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

import csv
import pandas as pd
import numpy as np
import parameters

def parse_ids(season_id, game_id):

    # pull common variables from the parameters file
    files_root = parameters.files_root

    # generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()
    teams = [away, home]
    
    # establish file locations and destinations
    TOI_matrix = files_root + 'TOI_matrix.csv'
    pbp = files_root + 'pbp.csv'
    stats_teams = files_root + 'stats_teams.csv'
    
    # create a dataframe for extracting TOI info
    TOI_df = pd.read_csv(TOI_matrix)
    
    # create a dataframe for extracting non-shootout play-by-play info
    pbp_df = pd.read_csv(pbp)
    pbp_df = pbp_df[(pbp_df['PERIOD'] != 5)]

    # create a dataframe for extracting shootout play-by-play info
    shootout_df = pd.read_csv(pbp)
    shootout_df = shootout_df[(shootout_df['PERIOD'] == 5)]
    
    away_shootout_result = 0
    home_shootout_result = 0
    
    away_shootout_goals = shootout_df[(shootout_df['TEAM'] == away) & (shootout_df['EVENT_TYPE'] == 'Goal')].count()[1]
    home_shootout_goals = shootout_df[(shootout_df['TEAM'] == home) & (shootout_df['EVENT_TYPE'] == 'Goal')].count()[1]
    
    if away_shootout_goals > home_shootout_goals:
        away_shootout_result = 1
        
    elif away_shootout_goals < home_shootout_goals:
        home_shootout_result = 1
    
    # trigger the csv files that will be written; write column titles to a header row 
    with open(stats_teams, 'w', newline = '') as teams_stats:
    
        teams_out = csv.writer(teams_stats)  
        teams_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'STATE', 'GP', 'TOI', 'GF', 'GA', 'xGF', 'xGA', 'ONSF', 'ONSA', 'USF', 'USA', 'SF', 'SA', 'FO', 'FOW', 'PENA', 'PENF', 'HF', 'HA', 'TF', 'TA', 'GD', 'xGD', 'ONSD', 'USD', 'SD'])
        
        # begin looping by team     
        for team in teams:
            
            if team == away:
                team_text = 'AWAY'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                team_zone = team_text + '_ZONE'
                team_shootout_result = away_shootout_result
                opponent_shootout_result = home_shootout_result
            elif team == home:
                team_text = 'HOME'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                team_zone = team_text + '_ZONE'
                team_shootout_result = home_shootout_result
                opponent_shootout_result = away_shootout_result

    
            ###
            ### TIME ON ICE
            ###
            
            toi_all = round(TOI_df[team_text].count() * 0.0166667, 1)
            toi_5v5_first = TOI_df[TOI_df[team_strength] == '5v5'].count()
            toi_5v5 = round(toi_5v5_first[1] * 0.0166667, 1)
            toi_PP_first = TOI_df[TOI_df[team_state] == 'PP'].count()
            toi_PP = round(toi_PP_first[1] * 0.0166667, 1)
            toi_SH_first = TOI_df[TOI_df[team_state] == 'SH'].count()
            toi_SH = round(toi_SH_first[1] * 0.0166667, 1)
     
        
            ###
            ### PLAY-BY-PLAY  
            ###
    
            #
            # shot metrics
            #
            
            # goals (shots that scored)
            event = 'Goal'
            GF_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event)].count()[1] + team_shootout_result
            GA_all = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event)].count()[1] + opponent_shootout_result
            GF_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5')].count()[1]
            GA_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5')].count()[1]
            GF_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP')].count()[1]
            GA_PP = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP')].count()[1]
            GF_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH')].count()[1]
            GA_SH = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH')].count()[1]
    
            GD_all = GF_all - GA_all
            GD_5v5 = GF_5v5 - GA_5v5
            GD_PP = GF_PP - GA_PP        
            GD_SH = GF_SH - GA_SH 
    
            # on-net shots (shots that scored or were saved)
            event='Save'
            ONSF_all = GF_all + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event)].count()[1]
            ONSA_all = GA_all + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event)].count()[1]
            ONSF_5v5 = GF_5v5 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5')].count()[1]
            ONSA_5v5 = GA_5v5 + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5')].count()[1]
            ONSF_PP = GF_PP + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP')].count()[1]
            ONSA_PP = GA_PP + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP')].count()[1]
            ONSF_SH = GF_SH + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH')].count()[1]
            ONSA_SH = GA_SH + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH')].count()[1]
        
            ONSD_all = ONSF_all - ONSA_all
            ONSD_5v5 = ONSF_5v5 - ONSA_5v5
            ONSD_PP = ONSF_PP - ONSA_PP        
            ONSD_SH = ONSF_SH - ONSA_SH 
    
            # unblocked shots (shots that scored, were saved or missed)
            event = 'Miss'       
            USF_all = ONSF_all + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event)].count()[1]
            USA_all = ONSA_all + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event)].count()[1]
            USF_5v5 = ONSF_5v5 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5')].count()[1]
            USA_5v5 = ONSA_5v5 + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5')].count()[1]
            USF_PP = ONSF_PP + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP')].count()[1]
            USA_PP = ONSA_PP + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP')].count()[1]
            USF_SH = ONSF_SH + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH')].count()[1]
            USA_SH = ONSA_SH + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH')].count()[1]
            
            USD_all = USF_all - USA_all
            USD_5v5 = USF_5v5 - USA_5v5
            USD_PP = USF_PP - USA_PP        
            USD_SH = USF_SH - USA_SH 
    
            # shots (shots that scored, were saved, missed or were blocked)
            event = 'Shot'
            SF_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event)].count()[1]
            SA_all = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event)].count()[1]
            SF_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5')].count()[1]
            SA_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5')].count()[1]
            SF_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP')].count()[1]
            SA_PP = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP')].count()[1]
            SF_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH')].count()[1]
            SA_SH = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH')].count()[1]
        
            SD_all = SF_all - SA_all
            SD_5v5 = SF_5v5 - SA_5v5
            SD_PP = SF_PP - SA_PP        
            SD_SH = SF_SH - SA_SH

            # expected goals
            xGF_all = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block'), pbp_df['xG'], 0).sum(), 2)
            xGA_all = round(np.where((pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block'), pbp_df['xG'], 0).sum(), 2)
            xGF_5v5 = round(np.where((pbp_df['TEAM'] == team) & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block'), pbp_df['xG'], 0).sum(), 2)
            xGA_5v5 = round(np.where((pbp_df['TEAM'] != team) & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block'), pbp_df['xG'], 0).sum(), 2)
            xGF_PP = round(np.where((pbp_df['TEAM'] == team) & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block'), pbp_df['xG'], 0).sum(), 2)
            xGA_PP = round(np.where((pbp_df['TEAM'] != team) & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block'), pbp_df['xG'], 0).sum(), 2)
            xGF_SH = round(np.where((pbp_df['TEAM'] == team) & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block'), pbp_df['xG'], 0).sum(), 2)
            xGA_SH = round(np.where((pbp_df['TEAM'] != team) & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block'), pbp_df['xG'], 0).sum(), 2)

            xGD_all = round(xGF_all - xGA_all, 2)
            xGD_5v5 = round(xGF_5v5 - xGA_5v5, 2)
            xGD_PP = round(xGF_PP - xGA_PP, 2)       
            xGD_SH = round(xGF_SH - xGA_SH, 2)
            
            #
            # non-shot metrics
            #
            
            # faceoffs
            event = 'Faceoff'
            FO_all = pbp_df[(pbp_df['EVENT'] == event)].count()[1]
            FOW_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event)].count()[1]
            FO_5v5 = pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5')].count()[1]
            FOW_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5')].count()[1]
            FO_PP = pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP')].count()[1]
            FOW_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP')].count()[1]
            FO_SH = pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH')].count()[1]
            FOW_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH')].count()[1]
      
            # penalties
            event = 'Penalty'
            PENA_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event)].count()[1]
            PENF_all = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event)].count()[1]
            PENA_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT'] == event)].count()[1]
            PENF_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT'] == event)].count()[1]
            PENA_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT'] == event)].count()[1]
            PENF_PP = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT'] == event)].count()[1]
            PENA_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT'] == event)].count()[1]
            PENF_SH = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT'] == event)].count()[1]
       
            # hits
            event = 'Hit'
            HF_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event)].count()[1]
            HA_all = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event)].count()[1]
            HF_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT'] == event)].count()[1]
            HA_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT'] == event)].count()[1]
            HF_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT'] == event)].count()[1]
            HA_PP = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT'] == event)].count()[1]
            HF_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT'] == event)].count()[1]
            HA_SH = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT'] == event)].count()[1]
              
            # turnovers (giveaways and takeaways)
            event = 'Takeaway'
            TKF_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event)].count()[1]
            TKA_all = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event)].count()[1]
            TKF_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT'] == event)].count()[1]
            TKA_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT'] == event)].count()[1]
            TKF_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT'] == event)].count()[1]
            TKA_PP = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT'] == event)].count()[1]
            TKF_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT'] == event)].count()[1]
            TKA_SH = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT'] == event)].count()[1]
    
            event = 'Giveaway'
            GVA_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event)].count()[1]
            GVF_all = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event)].count()[1]
            GVA_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT'] == event)].count()[1]
            GVF_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT'] == event)].count()[1]
            GVA_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT'] == event)].count()[1]
            GVF_PP = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT'] == event)].count()[1]
            GVA_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT'] == event)].count()[1]
            GVF_SH = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT'] == event)].count()[1]
        
            TF_all = TKF_all + GVF_all
            TA_all = TKA_all + GVA_all
            TF_5v5 = TKF_5v5 + GVF_5v5
            TA_5v5 = TKA_5v5 + GVA_5v5
            TF_PP = TKF_PP + GVF_PP
            TA_PP = TKA_PP + GVA_PP
            TF_SH = TKF_SH + GVF_SH
            TA_SH = TKA_SH + GVA_SH

    
            ###
            ### WRITE TO FILE
            ###
            
            if team == away:
                team_text = 'Away'
            elif team == home:
                team_text = 'Home'
    
            # arrange team data to record
            teams_out.writerow((season_id, game_id, date, team_text, team, 'ALL', '1', toi_all, GF_all, GA_all, xGF_all, xGA_all, ONSF_all, ONSA_all, USF_all, USA_all, SF_all, SA_all, FO_all, FOW_all, PENA_all, PENF_all, HF_all, HA_all, TF_all, TA_all, GD_all, xGD_all, ONSD_all, USD_all, SD_all))
            teams_out.writerow((season_id, game_id, date, team_text, team, '5v5', '1', toi_5v5, GF_5v5, GA_5v5, xGF_5v5, xGA_5v5, ONSF_5v5, ONSA_5v5, USF_5v5, USA_5v5, SF_5v5, SA_5v5, FO_5v5, FOW_5v5, PENA_5v5, PENF_5v5, HF_5v5, HA_5v5, TF_5v5, TA_5v5, GD_5v5, xGD_5v5, ONSD_5v5, USD_5v5, SD_5v5))
            teams_out.writerow((season_id, game_id, date, team_text, team, 'PP', '1', toi_PP, GF_PP, GA_PP, xGF_PP, xGA_PP, ONSF_PP, ONSA_PP, USF_PP, USA_PP, SF_PP, SA_PP, FO_PP, FOW_PP, PENA_PP, PENF_PP, HF_PP, HA_PP, TF_PP, TA_PP, GD_PP, xGD_PP, ONSD_PP, USD_PP, SD_PP))
            teams_out.writerow((season_id, game_id, date, team_text, team, 'SH', '1', toi_SH, GF_SH, GA_SH, xGF_SH, xGA_SH, ONSF_SH, ONSA_SH, USF_SH, USA_SH, SF_SH, SA_SH, FO_SH, FOW_SH, PENA_SH, PENF_SH, HF_SH, HA_SH, TF_SH, TA_SH, GD_SH, xGD_SH, ONSD_SH, USD_SH, SD_SH))
    
    # status update
    print('Finished generating team stats for ' + season_id + ' ' + game_id)