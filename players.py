from nba_api.stats.static import teams
from nba_api.stats.static import players
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.endpoints import playbyplay
from nba_api.stats.endpoints import boxscoretraditionalv2

import time

counter = 0
total = 0

totalErrors = 0
totalErrors2 = 0
totalErrors3 = 0

totaltotal = 0

nba_teams = teams.get_teams()
nba_players = players.get_active_players()
playersWithStats =[]
for x in nba_players:
    dict = {
        "name": x['full_name'],
        "wins": 0,
        "attempts": 0,
        "win_percentage": 0.0
    }
    playersWithStats.append(dict)

for team in nba_teams:
  
    team_id = team['id']

    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id,
                                season_nullable=Season.default,
                                season_type_nullable=SeasonType.regular)  

    games_dict = gamefinder.get_normalized_dict()
    games = games_dict['LeagueGameFinderResults']
    home_games = []
    for i in range(len(games)):
        if 'vs.' in games[i]['MATCHUP']:
            home_games.append(games[i])

    for game in home_games:

        game_id = game['GAME_ID']
        game_matchup = game['MATCHUP']

        plays_dict = playbyplay.PlayByPlay(game_id).get_normalized_dict()
        plays = plays_dict['PlayByPlay']
        play = plays[1]
        play_description = play['HOMEDESCRIPTION']
        
        if (play_description == '' or play_description == None):
            totalErrors += 1
            continue
        player = ''
        playerOne = ''
        playerTwo = ''
        info_dict = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id).get_normalized_dict()
        info = info_dict['PlayerStats']
        jump_loser = ''
        jump_winner = ''
        if 'Violation' in play_description:
            player = play_description[0:play_description.find(' Violation')]

            if (player == '' or player == None):
                totalErrors2 += 1
                continue

            player_last = player
            player_first = ''
            if ('. ' in player):
                player_last = player[player.find('.')+2:]
                player_first = player[:player.find('.')]

            for x in info:
                if ((player in x['PLAYER_NAME']) and (x['PLAYER_NAME'].startswith(player_first))):
                    jump_loser = x['PLAYER_NAME']
                    continue
            
            for item in playersWithStats:
                if (item['name'] == jump_loser):
                    item['attempts'] += 1
                    item['win_percentage'] = item['wins'] / item['attempts']

            print("violation", end='   ')

        else:
            playerOne = play_description[10:play_description.find(" vs.")]
            playerTwo = play_description[play_description.find("vs.")+4:play_description.find(':')]
            player = play_description[play_description.find("Tip to")+7:]

            if ((playerOne == '') or (playerTwo == '') or (player == '') or (playerOne == None) or (playerTwo == None) or (player == None) or (playerOne == playerTwo)):
                totalErrors3 += 1
                continue

            playerOne_last = playerOne
            playerOne_first = ''
            playerTwo_last = playerTwo
            playerTwo_first = ''
            player_last = player
            player_first = ''
            if ('. ' in playerOne):
                playerOne_last = playerOne[playerOne.find('.')+2:]
                playerOne_first = playerOne[:playerOne.find('.')]
                print(playerOne_first, end=' ')
                print(playerOne_last)
            if ('. ' in playerTwo):
                playerTwo_last = playerTwo[playerTwo.find('.')+2:]
                playerTwo_first = playerTwo[:playerTwo.find('.')]
                print(playerTwo_first, end=' ')
                print(playerTwo_last)
            if ('. ' in player):
                player_last = player[player.find('.')+2:]
                player_first = player[:player.find('.')]
                print(player_first, end=' ')
                print(player_last)

            player_t_id = ''
            playerOne_t_id = ''
            playerTwo_t_id = ''
            playerOne_fullname = ''
            playerTwo_fullname = ''

            for x in info:        
                if ((player_last in x['PLAYER_NAME']) and (x['PLAYER_NAME'].startswith(player_first))):
                    player_t_id = x['TEAM_ID']
                if ((playerOne_last in x['PLAYER_NAME']) and (x['PLAYER_NAME'].startswith(playerOne_first))):
                    if (x['TEAM_ID'] == team_id):
                        playerOne_t_id = x['TEAM_ID']
                        playerOne_fullname = x['PLAYER_NAME']
                if ((playerTwo_last in x['PLAYER_NAME']) and (x['PLAYER_NAME'].startswith(playerTwo_first))):
                    if (x['TEAM_ID'] != team_id):
                        playerTwo_t_id = x['TEAM_ID']
                        playerTwo_fullname = x['PLAYER_NAME']

            if (player_t_id == playerOne_t_id):
                jump_winner = playerOne_fullname
                jump_loser = playerTwo_fullname
            else:
                jump_winner = playerTwo_fullname
                jump_loser = playerOne_fullname

            for item in playersWithStats:
                if (item['name'] == jump_loser):
                    item['attempts'] += 1
                    item['win_percentage'] = item['wins'] / item['attempts']

                if (item['name'] == jump_winner):
                    item['wins'] += 1
                    item['attempts'] += 1
                    item['win_percentage'] = item['wins'] / item['attempts']
            
        totaltotal += 1
        print("winner:", end=' ')
        print(jump_winner, end=' ')
        print("loser:", end=' ')
        print(jump_loser, end='    ')
        print(play_description, end='   ')
        print(totalErrors,end=' ')
        print(totalErrors2,end=' ')
        print(totalErrors3,end=' ')
        print(totaltotal)

        time.sleep(1)

f = open("player_data.txt", "w")
for item in playersWithStats:
    if (item['attempts'] > 0):
        f.write(str(item['name']))
        f.write(' ')
        f.write(str(item['wins']))
        f.write(' ')
        f.write(str(item['attempts']))
        f.write(' ')
        f.write(str(item['win_percentage']))
        f.write('\n')
    
f.close()