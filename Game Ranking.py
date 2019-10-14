#pip install python
#pip install xlrd
def read_csv(file):
        csv_file = pd.read_excel(file)
        return csv_file


def add_lost_player_column():
        csv_file = read_csv('InputData.xlsx')   #Add input file here
        csv_file['Lost'] = 'NaN'
        for i in range(len(csv_file)):
            if csv_file.iloc[i]['Player1'] == csv_file.iloc[i]['Won']: #if player1 is in won column then add player 2 in lost col
                csv_file.loc[i,'Lost'] = csv_file.iloc[i]['Player2']
            else:
                csv_file.loc[i,'Lost'] = csv_file.iloc[i]['Player1'] #else add player1 in lost col
        return csv_file
    
def get_unique_players():  
        csv_file = add_lost_player_column()
        player1 = pd.DataFrame(csv_file.Player1.unique())  #unique players from Player1 col
        player2 = pd.DataFrame(csv_file.Player2.unique())  #unique players from Player2 col
        append_p1_and_p2=player1.append(player2)    #merge unique player1 and unique player2 
        append_p1_and_p2.columns=['name']
        name_of_players = append_p1_and_p2.name.unique()  #final unique players name
        return name_of_players
    
def Rating_points():   #gives 2 column , 1: players name , 2: rating = 0
    name_of_players = get_unique_players()
    rating_points = pd.DataFrame(name_of_players)
    rating_points.columns = ['name']
    rating_points['Ranking points'] = 0
    return rating_points
    
def ELO_algo():
    rating_points = Rating_points()
    csv_file = add_lost_player_column()
    for i in range(len(csv_file)):
        #get the name of 2 players from 1st row
        Player1 = csv_file.iloc[i]['Player1'] 
        Player2 = csv_file.iloc[i]['Player2']
        #get the ranking points of that palyers
        player1_points =  rating_points.loc[ rating_points['name'] == Player1, 'Ranking points'].iloc[0]
        player2_points =  rating_points.loc[ rating_points['name'] == Player2, 'Ranking points'].iloc[0]
        #calculate probablity of win and loss of that player
        P_A_wins = 1/(1+10**((player2_points-player1_points)/400))
        P_B_wins = 1/(1+10**((player1_points-player2_points)/400))
        won = csv_file.iloc[i]['Won']   #gives the name of won player
        lost = csv_file.iloc[i]['Lost'] #gives the name of lost player
        #update the rating points a/c to ELO algorithm
        if Player1 == won:
            rating_points.loc[rating_points.name ==Player1, 'Ranking points'] = player1_points + 30*(1-P_A_wins)
            rating_points.loc[rating_points.name ==Player2, 'Ranking points'] = player2_points + 30*(0-P_B_wins)
        if Player2 == won:
            rating_points.loc[rating_points.name ==Player1, 'Ranking points'] = player1_points + 30*(0-P_A_wins)
            rating_points.loc[rating_points.name ==Player2, 'Ranking points'] = player2_points + 30*(1-P_B_wins)
            
    return rating_points
    
def insert_data():
        csv_file = add_lost_player_column()
        name_of_players = get_unique_players()
        final = []
        for name in name_of_players:
            won = csv_file.loc[csv_file['Won'] == name]   #ll rows having the given name in Won column
            lost = csv_file.loc[csv_file['Lost'] == name] #all rows having the given name in Lost column
            played = len(won) + len(lost)  
            data = {'Player':name,'Played':played,'Won':len(won),'Lost':len(lost)}
            final.append(data)
        return final
    
def add_ranking_points():
    rating_points = ELO_algo()
    name_of_players = get_unique_players()
    final = insert_data()
    final_table = pd.DataFrame(final)
    for i in name_of_players:
        rating = rating_points.loc[rating_points['name'] == i, 'Ranking points'].iloc[0]  #give the ranking of the given name from rating_points table
        final_table.loc[final_table.Player == i, 'Ranking Points'] = rating   #add that ranking in final_table where Player = given name
    return final_table

def final_preview():
        final_table = add_ranking_points()
        final_table['Rank']=final_table['Ranking Points'].rank(ascending=0,method='dense')
        final_table['Rank']=final_table['Ranking Points'].rank(ascending=0,method='dense')
        final_table = final_table.sort_values('Rank')
        final_table = final_table[['Player','Played','Won','Lost','Ranking Points','Rank',]]
        final_table.reset_index(drop=True, inplace=True)
        final_table.to_csv('Output File.csv',float_format='%.f',index = False)  #only integers in o/p csv
        return final_table
    
final_preview()