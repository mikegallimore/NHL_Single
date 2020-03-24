# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import dict_team_colors

def switch_team_colors(away, home): 
    
    away_color = dict_team_colors.team_color_1st[away]
    home_color = dict_team_colors.team_color_1st[home]
    
    if away == 'ANA' and home == 'ARI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'ARI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ANA' and home == 'CAR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'CAR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ANA' and home == 'CGY':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'CGY':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ANA' and home == 'CHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'CHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ANA' and home == 'COL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'COL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ANA' and home == 'DET':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'DET':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ANA' and home == 'MTL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'MTL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ANA' and home == 'NJD':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'NJD':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ANA' and home == 'NYI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'NYI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ANA' and home == 'NYR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'NYR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ANA' and home == 'OTT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'OTT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ANA' and home == 'PHI':
        away_color = dict_team_colors.team_color_3rd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_3rd[home]
    if away == 'ANA' and home == 'PIT':
        away_color = dict_team_colors.team_color_3rd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ANA' and away == 'PIT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_3rd[home]
    
    
    if away == 'ARI' and home == 'CAR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ARI' and away == 'CAR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ARI' and home == 'CGY':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ARI' and away == 'CGY':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ARI' and home == 'CHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ARI' and away == 'CHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ARI' and home == 'CAR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ARI' and away == 'CAR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ARI' and home == 'COL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ARI' and away == 'COL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ARI' and home == 'DET':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ARI' and away == 'DET':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ARI' and home == 'MTL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ARI' and away == 'MTL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ARI' and home == 'NJD':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ARI' and away == 'NJD':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ARI' and home == 'OTT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ARI' and away == 'OTT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'ARI' and home == 'PHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'ARI' and away == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    
    
    if away == 'BOS' and home == 'ANA':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_3rd[home]        
    if home == 'BOS' and away == 'ANA':
        away_color = dict_team_colors.team_color_3rd[away]
        home_color = dict_team_colors.team_color_1st[home]
    if away == 'BOS' and home == 'BUF':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_3rd[home]        
    if home == 'BOS' and away == 'BUF':
        away_color = dict_team_colors.team_color_3rd[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'BOS' and home == 'CGY':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'BOS' and away == 'CGY':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'BOS' and home == 'PHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'BOS' and away == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'BOS' and home == 'VGK':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'BOS' and away == 'VGK':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    
    
    if away == 'BUF' and home == 'CBJ':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if home == 'BUF' and away == 'CBJ':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]
    if away == 'BUF' and home == 'COL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'BUF' and away == 'COL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if away == 'BUF' and home == 'EDM':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if home == 'BUF' and away == 'EDM':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if away == 'BUF' and home == 'FLA':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if home == 'BUF' and away == 'FLA':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]
    if away == 'BUF' and home == 'LAK':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'BUF' and away == 'LAK':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]               
    if away == 'BUF' and home == 'NYI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if home == 'BUF' and away == 'NYI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if away == 'BUF' and home == 'NYR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if home == 'BUF' and away == 'NYR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if away == 'BUF' and home == 'STL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if home == 'BUF' and away == 'STL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if away == 'BUF' and home == 'SJS':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'BUF' and away == 'SJS':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if away == 'BUF' and home == 'TBL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'BUF' and away == 'TBL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if away == 'BUF' and home == 'TOR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'BUF' and away == 'TOR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if away == 'BUF' and home == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if home == 'BUF' and away == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if away == 'BUF' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]        
    if home == 'BUF' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if away == 'BUF' and home == 'WPG':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]        
    if home == 'BUF' and away == 'WPG':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    
    
    if away == 'CAR' and home == 'CGY':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CAR' and away == 'CGY':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]     
    if away == 'CAR' and home == 'CHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CAR' and away == 'CHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]     
    if away == 'CAR' and home == 'COL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CAR' and away == 'COL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]     
    if away == 'CAR' and home == 'DET':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CAR' and away == 'DET':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]     
    if away == 'CAR' and home == 'MTL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CAR' and away == 'MTL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]     
    if away == 'CAR' and home == 'NJD':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CAR' and away == 'NJD':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]     
    if away == 'CAR' and home == 'OTT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CAR' and away == 'OTT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]    
    if away == 'CAR' and home == 'PHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CAR' and away == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    
    
    if away == 'CBJ' and home == 'COL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CBJ' and away == 'COL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'CBJ' and home == 'DAL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CBJ' and away == 'DAL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'CBJ' and home == 'EDM':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CBJ' and away == 'EDM':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'CBJ' and home == 'FLA':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CBJ' and away == 'FLA':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'CBJ' and home == 'LAK':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CBJ' and away == 'LAK':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'CBJ' and home == 'NYI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CBJ' and away == 'NYI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'CBJ' and home == 'NYR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CBJ' and away == 'NYR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'CBJ' and home == 'STL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CBJ' and away == 'STL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'CBJ' and home == 'SJS':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CBJ' and away == 'SJS':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'CBJ' and home == 'TBL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CBJ' and away == 'TBL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'CBJ' and home == 'TOR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CBJ' and away == 'TOR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'CBJ' and home == 'VAN':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CBJ' and away == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'CBJ' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CBJ' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'CBJ' and home == 'WPG':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CBJ' and away == 'WPG':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    
    
    if away == 'CGY' and home == 'CHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CGY' and away == 'CHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]     
    if away == 'CGY' and home == 'COL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CGY' and away == 'COL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]     
    if away == 'CGY' and home == 'DET':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CGY' and away == 'DET':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]     
    if away == 'CGY' and home == 'COL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CGY' and away == 'COL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]     
    if away == 'CGY' and home == 'MTL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CGY' and away == 'MTL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]     
    if away == 'CGY' and home == 'NJD':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CGY' and away == 'NJD':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]    
    if away == 'CGY' and home == 'OTT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CGY' and away == 'OTT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if away == 'CGY' and home == 'PHI':
        away_color = dict_team_colors.team_color_3rd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CGY' and away == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_3rd[home] 
      
    
    if away == 'CHI' and home == 'COL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CHI' and away == 'COL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'CHI' and home == 'DET':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CHI' and away == 'DET':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'CHI' and home == 'MTL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CHI' and away == 'MTL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'CHI' and home == 'NJD':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CHI' and away == 'NJD':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'CHI' and home == 'OTT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'CHI' and away == 'OTT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'CHI' and home == 'PHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'CHI' and away == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    
    
    if away == 'COL' and home == 'DET':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'COL' and away == 'DET':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'COL' and home == 'EDM':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'COL' and away == 'EDM':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'COL' and home == 'FLA':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'COL' and away == 'FLA':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'COL' and home == 'MTL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'COL' and away == 'MTL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'COL' and home == 'NJD':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'COL' and away == 'NJD':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'COL' and home == 'NSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'COL' and away == 'NSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'COL' and home == 'OTT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'COL' and away == 'OTT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'COL' and home == 'PHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'COL' and away == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'COL' and home == 'VAN':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'COL' and away == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'COL' and home == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'COL' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    
    
    if away == 'DAL' and home == 'EDM':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'DAL' and away == 'EDM':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'DAL' and home == 'FLA':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'DAL' and away == 'FLA':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'DAL' and home == 'MIN':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'DAL' and away == 'MIN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'DAL' and home == 'STL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'DAL' and away == 'STL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'DAL' and home == 'TBL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'DAL' and away == 'TBL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'DAL' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'DAL' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    
    
    if away == 'DET' and home == 'EDM':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'DET' and away == 'EDM':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'DET' and home == 'MTL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'DET' and away == 'MTL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'DET' and home == 'NJD':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'DET' and away == 'NJD':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'DET' and home == 'OTT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'DET' and away == 'OTT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'DET' and home == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'DET' and away == 'PHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    
    
    if away == 'EDM' and home == 'FLA':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'EDM' and away == 'FLA':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'EDM' and home == 'LAK':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'EDM' and away == 'LAK':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'EDM' and home == 'MIN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'EDM' and away == 'MIN':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'EDM' and home == 'NSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'EDM' and away == 'NSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'EDM' and home == 'NYI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'EDM' and away == 'NYI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'EDM' and home == 'NYR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'EDM' and away == 'NYR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'EDM' and home == 'SJS':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'EDM' and away == 'SJS':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'EDM' and home == 'STL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'EDM' and away == 'STL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'EDM' and home == 'TBL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'EDM' and away == 'TBL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'EDM' and home == 'TOR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'EDM' and away == 'TOR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'EDM' and home == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'EDM' and away == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'EDM' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'EDM' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'EDM' and home == 'WPG':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'EDM' and away == 'WPG':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    
    
    if away == 'FLA' and home == 'LAK':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'FLA' and away == 'LAK':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'FLA' and home == 'MIN':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'FLA' and away == 'MIN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'FLA' and home == 'LAK':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'FLA' and away == 'LAK':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'FLA' and home == 'NYI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'FLA' and away == 'NYI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'FLA' and home == 'NYR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'FLA' and away == 'NYR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'FLA' and home == 'STL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'FLA' and away == 'STL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'FLA' and home == 'TBL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'FLA' and away == 'TBL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'FLA' and home == 'TOR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'FLA' and away == 'TOR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'FLA' and home == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'FLA' and away == 'VAN':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'FLA' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'FLA' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]         
    if away == 'FLA' and home == 'WPG':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'FLA' and away == 'WPG':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    
    
    if away == 'LAK' and home == 'NYI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'LAK' and away == 'NYI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'LAK' and home == 'NYR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'LAK' and away == 'NYR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'LAK' and home == 'STL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'LAK' and away == 'STL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'LAK' and home == 'VAN':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'LAK' and away == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'LAK' and home == 'NYI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'LAK' and away == 'NYI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'LAK' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'LAK' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    
    
    if away == 'MIN' and home == 'SJS':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'MIN' and away == 'SJS':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'MIN' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'MIN' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    
    
    if away == 'MTL' and home == 'NJD':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'MTL' and away == 'NJD':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'MTL' and home == 'OTT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'MTL' and away == 'OTT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'MTL' and home == 'PHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'MTL' and away == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'MTL' and home == 'PIT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'MTL' and away == 'PIT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    
    
    if away == 'NJD' and home == 'OTT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'NJD' and away == 'OTT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]
    if away == 'NJD' and home == 'PHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NJD' and away == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NJD' and home == 'OTT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'NJD' and away == 'OTT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    
    
    if away == 'NSH' and home == 'PHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NSH' and away == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NSH' and home == 'PIT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NSH' and away == 'PIT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NSH' and home == 'VGK':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NSH' and away == 'VGK':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    
    
    if away == 'NYI' and home == 'NYR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NYI' and away == 'NYR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NYI' and home == 'STL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NYI' and away == 'STL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NYI' and home == 'TBL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NYI' and away == 'TBL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NYI' and home == 'TOR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NYI' and away == 'TOR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NYI' and home == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'NYI' and away == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NYI' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'NYI' and away == 'NYR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]
    if away == 'NYI' and home == 'WPG':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NYI' and away == 'WPG':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    
    
    if away == 'NYR' and home == 'SJS':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NYR' and away == 'SJS':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NYR' and home == 'STL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NYR' and away == 'STL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NYR' and home == 'TBL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NYR' and away == 'TBL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NYR' and home == 'TOR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NYR' and away == 'TOR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'NYR' and home == 'VAN':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'NYR' and away == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]
    if away == 'NYR' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'NYR' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]
    if away == 'NYR' and home == 'WPG':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'NYR' and away == 'WPG':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    
    if away == 'OTT' and home == 'PHI':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'OTT' and away == 'PHI':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'OTT' and home == 'PIT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'OTT' and away == 'PIT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    
    
    if away == 'PHI' and home == 'PIT':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'PHI' and away == 'PIT':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    
    
    if away == 'PIT' and home == 'VGK':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'PIT' and away == 'VGK':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    
    
    if away == 'SJS' and home == 'TBL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'SJS' and away == 'TBL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]
    
    
    if away == 'STL' and home == 'TBL':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'STL' and away == 'TBL':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'STL' and home == 'TOR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'STL' and away == 'TOR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    if away == 'STL' and home == 'VAN':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'STL' and away == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]
    if away == 'STL' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'STL' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]
    if away == 'STL' and home == 'WPG':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'STL' and away == 'WPG':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]
    
    
    if away == 'TBL' and home == 'TOR':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'TBL' and away == 'TOR':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'TBL' and home == 'VAN':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'TBL' and away == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    if away == 'TBL' and home == 'WPG':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'TBL' and away == 'WPG':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    
    
    if away == 'TOR' and home == 'VAN':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'TOR' and away == 'VAN':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]
    if away == 'TOR' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'TOR' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]
    if away == 'TOR' and home == 'WPG':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_3rd[home]  
    if home == 'TOR' and away == 'WPG':
        away_color = dict_team_colors.team_color_3rd[away]
        home_color = dict_team_colors.team_color_1st[home]
    
    
    if away == 'VAN' and home == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'VAN' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    if away == 'TBL' and home == 'WPG':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'TBL' and away == 'WPG':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home] 
    
    
    if away == 'VGK' and home == 'WSH':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]  
    if home == 'VGK' and away == 'WSH':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home] 
    
    
    if away == 'WSH' and home == 'WPG':
        away_color = dict_team_colors.team_color_2nd[away]
        home_color = dict_team_colors.team_color_1st[home]  
    if home == 'WSH' and away == 'WPG':
        away_color = dict_team_colors.team_color_1st[away]
        home_color = dict_team_colors.team_color_2nd[home]


    return [away_color, home_color]