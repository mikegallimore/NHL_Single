# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import pandas as pd
import matplotlib.pyplot as plt
import parameters

def parse_ids(season_id, game_id, images):

    ### pull common variables from the parameters file
    charts_players = parameters.charts_players
    files_root = parameters.files_root

    ### generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()
    teams = [away, home]

    ### create variables that point to the .csv processed stats files for players
    players_individual_file = files_root + 'stats_players_individual.csv'
    players_onice_file = files_root + 'stats_players_onice.csv'
    
    ### create a dataframe object that reads in info from the .csv files
    players_individual_df = pd.read_csv(players_individual_file)
    players_onice_df = pd.read_csv(players_onice_file)
           
    ### loop through each team
    for team in teams:
          
        if team == away:
            team_text = 'AWAY'
            team_colors = ['#e60000', '#f26666', '#ffcccc']
    
        if team == home:
            team_text = 'HOME'
            team_colors = ['#206a92', '#439bc8', '#66ccff']   
                      
        ### create dataframes; filter for team, game state and position; add gamescore metric and create a subset with it and the player names   
        game_state = '5v5'       
        F_5v5_df = players_individual_df.copy()
        F_5v5_df = F_5v5_df[(F_5v5_df['TEAM'] == team) & (F_5v5_df['STATE'] == game_state) & (F_5v5_df['POS'] == 'F')]                
        F_5v5_df['GS_5v5'] = (0.75 * F_5v5_df['G']) + (0.7 * F_5v5_df['1_A']) + (0.55 * (F_5v5_df['A'] - F_5v5_df['1_A'])) + (0.075 * F_5v5_df['ONS']) + (0.05 * F_5v5_df['BK']) + ((0.15 * F_5v5_df['PD']) - (0.15 * F_5v5_df['PT'])) + ((0.01 * F_5v5_df['FOW']) - (0.01 * (F_5v5_df['FO'] - F_5v5_df['FOW'])))
        F_5v5 = F_5v5_df[['PLAYER', 'GS_5v5']]

        D_5v5_df = players_individual_df.copy()
        D_5v5_df = D_5v5_df[(D_5v5_df['TEAM'] == team) & (D_5v5_df['STATE'] == game_state) & (D_5v5_df['POS'] == 'D')]                
        D_5v5_df['GS_5v5'] = (0.75 * D_5v5_df['G']) + (0.7 * D_5v5_df['1_A']) + (0.55 * (D_5v5_df['A'] - D_5v5_df['1_A'])) + (0.075 * D_5v5_df['ONS']) + (0.05 * D_5v5_df['BK']) + ((0.15 * D_5v5_df['PD']) - (0.15 * D_5v5_df['PT'])) + ((0.01 * D_5v5_df['FOW']) - (0.01 * (D_5v5_df['FO'] - D_5v5_df['FOW'])))
        D_5v5 = D_5v5_df[['PLAYER', 'GS_5v5']]

        G_5v5_df = players_onice_df.copy()
        G_5v5_df = G_5v5_df[(G_5v5_df['TEAM'] == team) & (G_5v5_df['STATE'] == game_state) & (G_5v5_df['POS'] == 'G')]
        G_5v5_df['GS_5v5'] = (-0.75 * G_5v5_df['GA']) + (0.1 * (G_5v5_df['ONSA'] - G_5v5_df['GA']))
        G_5v5 = G_5v5_df[['PLAYER', 'GS_5v5']]
        
        game_state = 'PP'  
        F_PP_df = players_individual_df.copy()
        F_PP_df = F_PP_df[(F_PP_df['TEAM'] == team) & (F_PP_df['STATE'] == game_state) & (F_PP_df['POS'] == 'F')]
        F_PP_df['GS_PP'] = (0.75 * F_PP_df['G']) + (0.7 * F_PP_df['1_A']) + (0.55 * (F_PP_df['A'] - F_PP_df['1_A'])) + (0.075 * F_PP_df['ONS']) + (0.05 * F_PP_df['BK']) + ((0.15 * F_PP_df['PD']) - (0.15 * F_PP_df['PT'])) + ((0.01 * F_PP_df['FOW']) - (0.01 * (F_PP_df['FO'] - F_PP_df['FOW'])))
        F_PP = F_PP_df[['PLAYER', 'GS_PP']]

        D_PP_df = players_individual_df.copy()
        D_PP_df = D_PP_df[(D_PP_df['TEAM'] == team) & (D_PP_df['STATE'] == game_state) & (D_PP_df['POS'] == 'D')]
        D_PP_df['GS_PP'] = (0.75 * D_PP_df['G']) + (0.7 * D_PP_df['1_A']) + (0.55 * (D_PP_df['A'] - D_PP_df['1_A'])) + (0.075 * D_PP_df['ONS']) + (0.05 * D_PP_df['BK']) + ((0.15 * D_PP_df['PD']) - (0.15 * D_PP_df['PT'])) + ((0.01 * D_PP_df['FOW']) - (0.01 * (D_PP_df['FO'] - D_PP_df['FOW'])))
        D_PP = D_PP_df[['PLAYER', 'GS_PP']]

        G_PP_df = players_onice_df.copy()
        G_PP_df = G_PP_df[(G_PP_df['TEAM'] == team) & (G_PP_df['STATE'] == game_state) & (G_PP_df['POS'] == 'G')]
        G_PP_df['GS_PP'] = (-0.75 * G_PP_df['GA']) + (0.1 * (G_PP_df['ONSA'] - G_PP_df['GA']))
        G_PP = G_PP_df[['PLAYER', 'GS_PP']]
        
        game_state = 'SH'
        F_SH_df = players_individual_df.copy()
        F_SH_df = F_SH_df[(F_SH_df['TEAM'] == team) & (F_SH_df['STATE'] == game_state) & (F_SH_df['POS'] == 'F')]
        F_SH_df['GS_SH'] = (0.75 * F_SH_df['G']) + (0.7 * F_SH_df['1_A']) + (0.55 * (F_SH_df['A'] - F_SH_df['1_A'])) + (0.075 * F_SH_df['ONS']) + (0.05 * F_SH_df['BK']) + ((0.15 * F_SH_df['PD']) - (0.15 * F_SH_df['PT'])) + ((0.01 * F_SH_df['FOW']) - (0.01 * (F_SH_df['FO'] - F_SH_df['FOW'])))
        F_SH = F_SH_df[['PLAYER', 'GS_SH']]

        D_SH_df = players_individual_df.copy()
        D_SH_df = D_SH_df[(D_SH_df['TEAM'] == team) & (D_SH_df['STATE'] == game_state) & (D_SH_df['POS'] == 'D')]
        D_SH_df['GS_SH'] = (0.75 * D_SH_df['G']) + (0.7 * D_SH_df['1_A']) + (0.55 * (D_SH_df['A'] - D_SH_df['1_A'])) + (0.075 * D_SH_df['ONS']) + (0.05 * D_SH_df['BK']) + ((0.15 * D_SH_df['PD']) - (0.15 * D_SH_df['PT'])) + ((0.01 * D_SH_df['FOW']) - (0.01 * (D_SH_df['FO'] - D_SH_df['FOW'])))
        D_SH = D_SH_df[['PLAYER', 'GS_SH']]

        G_SH_df = players_onice_df.copy()
        G_SH_df = G_SH_df[(G_SH_df['TEAM'] == team) & (G_SH_df['STATE'] == game_state) & (G_SH_df['POS'] == 'G')]
        G_SH_df['GS_SH'] = (-0.75 * G_SH_df['GA']) + (0.1 * (G_SH_df['ONSA'] - G_SH_df['GA']))
        G_SH = G_SH_df[['PLAYER', 'GS_SH']]

        ### merge the dataframes for each position into a new dataframe; create a composite gamescore to sort and rank by
        F_GS = pd.merge(F_5v5, F_PP, on='PLAYER', how='inner')
        F_GS = pd.merge(F_GS, F_SH, on='PLAYER', how='inner')
        F_GS['GS_ALL'] = F_GS['GS_5v5'] + F_GS['GS_PP'] + F_GS['GS_SH']
        F_GS = F_GS.sort_values(by=['GS_ALL'], ascending = True)
        F_GS['RANK'] = F_GS['GS_ALL'].rank(method='first')
        F_GS['RANK'] -= 1

        D_GS = pd.merge(D_5v5, D_PP, on='PLAYER', how='inner')
        D_GS = pd.merge(D_GS, D_SH, on='PLAYER', how='inner')
        D_GS['GS_ALL'] = D_GS['GS_5v5'] + D_GS['GS_PP'] + D_GS['GS_SH']
        D_GS = D_GS.sort_values(by=['GS_ALL'], ascending = True)
        D_GS['RANK'] = D_GS['GS_ALL'].rank(method='first')
        D_GS['RANK'] -= 1

        G_GS = pd.merge(G_5v5, G_PP, on='PLAYER', how='inner')
        G_GS = pd.merge(G_GS, G_SH, on='PLAYER', how='inner')
        G_GS['GS_ALL'] = G_GS['GS_5v5'] + G_GS['GS_PP'] + G_GS['GS_SH']
        G_GS = G_GS.sort_values(by=['GS_ALL'], ascending = True)
        G_GS['RANK'] = G_GS['GS_ALL'].rank(method='first')
        G_GS['RANK'] -= 1
                     
        ### create a figure with two subplots sharing the y-axis
        fig, axarr = plt.subplots(3, sharex=True, figsize=(8,6), gridspec_kw={'width_ratios': [1], 'height_ratios': [5,3,1]})
        
         ### set the plot title
        axarr[0].set_title(date + ' Gamescores\n ' + away + ' @ ' + home + '\n' )
    
        ### create bars indicating the game score for the players at each position
        try:
            F_GS.plot(x='PLAYER', y=['GS_5v5', 'GS_PP', 'GS_SH'], kind='barh', stacked=True, color=[team_colors[0], team_colors[1], team_colors[2]], width=0.75, legend=False, ax=axarr[0]);
        except:
            pass
        try:
            D_GS.plot(x='PLAYER', y=['GS_5v5', 'GS_PP', 'GS_SH'], kind='barh', stacked=True, color=[team_colors[0], team_colors[1], team_colors[2]], width=0.75, legend=False, ax=axarr[1]);
        except:
            pass    
        try:
            G_GS.plot(x='PLAYER', y=['GS_5v5', 'GS_PP', 'GS_SH'], kind='barh', stacked=True, color=[team_colors[0], team_colors[1], team_colors[2]], width=0.75, legend=False, ax=axarr[2]);
        except:
            pass
    
        ### remove the y-labels for the plot
        axarr[0].set_xlabel('')
        axarr[0].set_ylabel('')
        
        axarr[1].set_xlabel('')
        axarr[1].set_ylabel('')
        
        axarr[2].set_xlabel('')
        axarr[2].set_ylabel('')
    
        ### set vertical indicators for break-even
        axarr[0].axvspan(0, 0, ymin=0, ymax=1, alpha=0.5, color='black')
        axarr[1].axvspan(0, 0, ymin=0, ymax=1, alpha=0.5, color='black')
        axarr[2].axvspan(0, 0, ymin=0, ymax=1, alpha=0.5, color='black')
    
        ### change the tick parameters for each axes
        axarr[0].tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            left=False,
            labelbottom=False)

        axarr[1].tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            left=False,
            labelbottom=False)
    
        axarr[2].tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            left=False,
            labelbottom=True)
        
        ### create a list of x-axis tick values contingent on the max values for shots for and against 
        F_max = F_GS['GS_ALL']
        F_max = F_max.max()
        F_min = F_GS['GS_ALL']
        F_min = F_min.min()

        D_max = D_GS['GS_ALL']
        D_max = D_max.max()
        D_min = D_GS['GS_ALL']
        D_min = D_min.min()

        G_max = G_GS['GS_ALL']
        G_max = G_max.max()
        G_min = G_GS['GS_ALL']
        G_min = G_min.min()

        max_list = [F_max, D_max, G_max]

        x_tickmax = max(max_list)

        if x_tickmax <= 0.5:
            x_ticklabels = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        if x_tickmax > 0.5 and x_tickmax <= 1:
            x_ticklabels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        if x_tickmax > 1 and x_tickmax <= 1.5:
            x_ticklabels = [0.0, 0.3, 0.6, 0.9, 1.2, 1.5]
        if x_tickmax > 1.5 and x_tickmax <= 2:
            x_ticklabels = [0.0, 0.4, 0.8, 1.2, 1.6, 2]
        if x_tickmax > 2 and x_tickmax <= 2.5:
            x_ticklabels = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
        if x_tickmax > 2.5 and x_tickmax <= 3.0:
            x_ticklabels = [0.0, 0.6, 1.2, 1.8, 2.4, 3.0]
        
        ### use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
        axarr[0].set_xticks(x_ticklabels, minor=False)
        axarr[1].set_xticks(x_ticklabels, minor=False)
        axarr[2].set_xticks(x_ticklabels, minor=False)
        
        ### remove the borders to each subplot
        axarr[0].spines["top"].set_visible(False)   
        axarr[0].spines["bottom"].set_visible(False)    
        axarr[0].spines["right"].set_visible(False)    
        axarr[0].spines["left"].set_visible(False)  

        axarr[1].spines["top"].set_visible(False)   
        axarr[1].spines["bottom"].set_visible(False)    
        axarr[1].spines["right"].set_visible(False)    
        axarr[1].spines["left"].set_visible(False)  

        axarr[2].spines["top"].set_visible(False)   
        axarr[2].spines["bottom"].set_visible(False)    
        axarr[2].spines["right"].set_visible(False)    
        axarr[2].spines["left"].set_visible(False)  

        plt.legend(loc='center', bbox_to_anchor=(.5, -1), ncol=3).get_frame().set_linewidth(0.0)
        
        ### save the image to file
        if team == away:
            plt.savefig(charts_players + '_gamescores_away.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_players + '_gamescores_home.png', bbox_inches='tight', pad_inches=0.2)    
        
        ### show the current figure
        if images == 'show':
            plt.show()
        
        ### close the current figure   
        plt.close(fig)
        
        
        print('Plotting ' + team + ' gamescores for players.')   
            
            
    print('Finished plotting player gamescores.')