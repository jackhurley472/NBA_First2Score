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

nba_teams = teams.get_teams()

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
        violation = False
        hasInitials = False
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
                hasInitials = True

            violation = True
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
            if ('. ' in playerTwo):
                playerTwo_last = playerTwo[playerTwo.find('.')+2:]
                playerTwo_first = playerTwo[:playerTwo.find('.')]
            if ('. ' in player):
                player_last = player[player.find('.')+2:]
                player_first = player[:player.find('.')]
            hasInitials = True

        home_won_tip = False

        info_dict = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id).get_normalized_dict()
        info = info_dict['PlayerStats']
        for x in info:
            if ((player_last in x['PLAYER_NAME']) and (x['PLAYER_NAME'].startswith(player_first))):
                if ((x['TEAM_ID'] == team_id) and (not violation)):
                    home_won_tip = True
                    break
                elif ((x['TEAM_ID'] == team_id) and (violation)):
                    break

        home_scored_first = False
        scoring_play = ''
        for x in plays:
            if (x['SCOREMARGIN'] != None):
                if (x['HOMEDESCRIPTION'] != None):
                    home_scored_first = True
                    scoring_play = x['HOMEDESCRIPTION']
                else:
                    scoring_play = x['VISITORDESCRIPTION']
                break

        if (home_won_tip and home_scored_first):
            counter += 1
        elif ((not home_won_tip) and (not home_scored_first)):
            counter += 1

        total += 1
        print(counter/total, end='      ')
        print(counter, end='      ')
        print(total, end='      ')
        if (hasInitials):
            print(player_first, end=' ')
        print(player_last, end='     ')
        print(play_description, end='     ')
        print(scoring_play, end='     ')
        print(totalErrors,end=' ')
        print(totalErrors2,end=' ')
        print(totalErrors3)
        time.sleep(1)
    
print((counter/total)*100)