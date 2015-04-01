#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import math
import psycopg2
from random import randint

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")
    print("Tournament database connection established.")
    
def fetchResultsView():
    
    queryContent = "SELECT * FROM match_pairings_results;"
    
    DB = connect()
    cursor = DB.cursor()
    
    cursor.execute(queryContent)
    results = cursor.fetchall()
    
    DB.commit()
    DB.close()
    
    return results

def updateTourStats(tourID = '1'):
    playerStats = fetchResultsView()
    
    DB = connect()
    cursor = DB.cursor()

    for counter, r in enumerate(playerStats):
        
        print counter
    
        # Extrapolate player statistics from dictionary.
        t_ID = tourID
        playerID = playerStats[counter][2]
        points = playerStats[counter][5]
        
        # Test to see if player won or lost this match.
        if playerStats[counter][3] == True:
            win = 1
            loss = 0
        else:
            win = 0
            loss = 1
        
        
        queryContent = "UPDATE tournament_players SET matches_played = matches_played + 1," \
            " match_wins = match_wins + {}, match_losses = match_losses + {}, tour_points = tour_points + {} WHERE tour_id = {} AND player_id = {}".format(win,loss,points,t_ID,playerID)

        print(queryContent)

        cursor.execute(queryContent)
        DB.commit()
    DB.close()
    
def updateGlobalStats():
    pass
    
    
def createMatches(player1, player2, tourID='1', tour_round = '1'):
    
    if player2 == "bye":
        player2 = None
    
    queryContent = "INSERT INTO match_pairings (tour_id, player1, player2, round)" \
            " VALUES({},{},{},{})".format(tourID, player1, player2, tour_round)
            
    DB = connect()
    cursor = DB.cursor()
    
    cursor.execute(queryContent)
    
    DB.commit()
    DB.close()

def clearTestData():
    
    DB = connect()
    cursor = DB.cursor()
    
    queryContent1 = "DELETE FROM match_pairings WHERE tour_id = 1"
    queryContent2 = "DELETE FROM tournament_players WHERE tour_id = 1"

    cursor.execute(queryContent1)
    q1Rows = cursor.rowcount
    print("{} rows deleted").format(q1Rows)
    
    cursor.execute(queryContent2)
    q2Rows = cursor.rowcount
    print("{} rows deleted").format(q2Rows)
    
    DB.commit()
    DB.close()
    
def deleteMatches(tourID='1'):
    """Remove all the match records from the database."""
    
    DB = connect()
    cursor = DB.cursor()
    
    queryContent = "DELETE FROM match_pairings WHERE tour_id = {};".format(tourID)
    queryContent2 = "DELETE FROM tournament_players WHERE tour_id = {}".format(tourID)
    
    cursor.execute(queryContent)
    cursor.execute(queryContent2)

    DB.commit()
    DB.close

    print('All matches for tournament {} have been removed').format(tourID)
    
def deletePlayerRegistry():
    DB = connect()
    cursor = DB.cursor()

    queryContent = "DELETE FROM players"
    cursor.execute(queryContent)

    DB.commit()
    DB.close()

    print("All player records have been deleted form the registry")
    

def deletePlayers(tourID='1'):
    """Remove all the player records from the database."""

    DB = connect()
    cursor = DB.cursor()

    queryContent = "DELETE FROM tournament_players WHERE tour_id = {};".format(tourID)
    cursor.execute(queryContent)

    DB.commit()
    DB.close()

    print("All player records have been deleted form the tournament")
    
    deleteMatches()
    deletePlayerRegistry()

def countPlayers(tourID='1'):
    """Returns the number of players currently registered."""

    DB = connect()
    cursor = DB.cursor()

    queryContents = "SELECT count(*) FROM tournament_players WHERE tour_id = {};".format(tourID)
    cursor.execute(queryContents)
    numPlayers = cursor.fetchone()

    DB.commit()
    DB.close()

    print("Total number of Players = " + str(numPlayers[0]))
    return numPlayers[0] 

def createPlayer(name):
    
    DB = connect()
    cursor = DB.cursor()

    
    playerName = str(name)
    queryContent = "INSERT INTO players (name) VALUES (%s) RETURNING *"
    cursor.execute(queryContent, (playerName,))
    playerInfo = cursor.fetchall()
    returnValue = [playerInfo[0][0], playerInfo[0][1]]
    
    DB.commit()
    DB.close()
    
    return returnValue


def registerPlayer(name, tourID='1'):
    """Adds a player to the players table in the tournament database.
       This will probably need to be updated to include the tournamentPlayers table as well for
       project testing
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cursor = DB.cursor()

    playerInfo = createPlayer(name)
    playerID = playerInfo[0]
    playerName = str(playerInfo[1])
    
    
    queryContent = "INSERT INTO tournament_players (player_id, tour_id, tour_points) VALUES ({},{}, 0);".format(playerID, tourID)

    cursor.execute(queryContent)

    DB.commit()
    DB.close()

    print("Added Player: " + playerName + " with ID " + str(playerID) + " to registry.")


def playerStandings(tourID = '1'):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    updateTourStats()
    
    queryContent = "SELECT tournament_players.player_id, players.name, tournament_players.match_wins, " \
        "tournament_players.matches_played from tournament_players, players where " \
        "tournament_players.tour_id = {} and tournament_players.player_id = players.id ORDER BY tournament_players.match_wins".format(tourID)
    
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(queryContent)
    results = cursor.fetchall()
    
    DB.commit()
    DB.close()
    
    print results
    return results
    

def whoWonGenerator(p1, p2):
    winner = randint(1, 2)
    
    if winner == 1:
        return p1
    else:
        return p2
    
def numberRounds(tourID='1'):
    numPlayers = countPlayers()
    numberRounds = math.log2(numPlayers)
    
    print "The current number of rounds for {} players is {}".format(str(numPlayers),str(numberRounds))
    
    return numberRounds

def reportMatch(winner, loser, tourID = '1', tour_round='1'):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    createMatches(winner, loser)
    
    DB = connect()
    cursor = DB.cursor()
    queryContent1 = "SELECT * FROM match_pairings WHERE " \
        "tour_id = {} AND round = {} AND player1 = {} OR player2 = {}".format(tourID,tour_round, winner, winner)
    cursor.execute(queryContent1)
    firstQuery = cursor.fetchall()
    
    print firstQuery
    
    matchID = firstQuery[0][0]
    
    print("Match ID = {}").format(matchID)
    
    if loser == "bye":
        queryContent2 = "INSERT INTO match_results (match_id, player_id,is_winner, is_bye, points_awarded) " \
            "values ({},{}, true, true, 10)".format(matchID, winner)
    else:
        queryContent2 = "INSERT INTO match_results (match_id, player_id, is_winner, is_bye, points_awarded) " \
            "values ({},{}, true, false, 10),({},{}, false, false, 0)".format(matchID, winner, matchID, loser)
    
    cursor.execute(queryContent2)
    DB.commit()
    DB.close()
    
    
def isOdd(value):
    if value % 2 == 0:
        return False
    else:
        return True
 
 
def swissPairings(tourID='1'):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    
    #TEMP FIX, need to figure out when/how to update standing
    updateTourStats()

    DB = connect()
    cursor = DB.cursor()

    queryContent = "select players.id, tournament_players.player_id, players.name, tournament_players.tour_points from players, tournament_players where tour_id = '1' AND players.id = tournament_players.player_id ORDER BY tour_points;".format(tourID)
    
    cursor.execute(queryContent)
    regPlayerInfo = cursor.fetchall()
    regPlayerCount = cursor.rowcount
    
    oddNumEntrants = isOdd(regPlayerCount)
    
    if oddNumEntrants == False:
        print "Even Number of contestants"
    else:
        print "Odd number of contestants"
        
    i = 1
    match = 1
    matchList = []
    
    while i < regPlayerCount:
        print "match {} : contestants {} and {}".format(str(match), str(regPlayerInfo[i - 1][0]), str(regPlayerInfo[i][0]))
        matchList.append((regPlayerInfo[i - 1][0],regPlayerInfo[i - 1][2],regPlayerInfo[i][0],regPlayerInfo[i][2]))
#         winner = whoWonGenerator(regPlayerInfo[i - 1][0], regPlayerInfo[i][0])
#         print "And the winner is: " + str(winner)
        match += 1
        i += 2
        if i == regPlayerCount:
            print "match {} : contestants {} has a bye round".format(str(match), str(regPlayerInfo[i - 1][0]))
            # the following will create an error because bye does not have an id. FIX
            matchList.append((regPlayerInfo[i - 1][0],regPlayerInfo[i - 1][2],'bye','bye'))
        
    print "Total number of players = {} ".format(regPlayerInfo.__len__())
    print matchList
    return matchList
    
    DB.close()

