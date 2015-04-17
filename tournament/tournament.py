#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# Created by Victor Asselta
# written for project2 in Udacity's Full Stack NanoDegree
# Please see the accompanying README file.
# This file represents an attempt to satisfy all extra credit and
# some areas of my own interest.
#

import math
from random import randint
from DB_Handler import *

# Used to call an instance of DB_Handler and set some basic parameters for the connection
def connect():
    DB = DB_Handler()
    DB.dbname = 'tournament'
    DB.tourID = '1'
    
    return DB

# Fetches a previous created view used for updating player statistics.    
def fetchResultsView():
    
    DB = connect()
    DB.tableName = ('match_pairings_results',)
    DB.queryReturn = True
    results = DB.read()
    
    return results

# Uses the above view to update tournament statistics for wins, losses, matches played, and points
def updateTourStats(tourID = '1'):
    playerStats = fetchResultsView()

    for stats in playerStats:
        
        # Extrapolate player statistics from dictionary.
        playerID = stats[2]
        points = str(stats[5])
        
        # Test to see if player won or lost this match.
        if stats[3] == True:
            win = '1'
            loss = '0'
        else:
            win = '0'
            loss = '1'
            
        # Database Handler calls
        DB = connect()
        DB.tableName = ('tournament_players',)
        DB.restrict = True
        DB.restrictWhere = (('tour_id', tourID ), ('player_id', playerID))
        data = None
        DB.queryConditions = (('matches_played', 'matches_played + 1'),('match_wins', ('match_wins + ' + win)),('match_losses', ('match_losses + ' + loss)), ('tour_points',('tour_points +' + points)))
        
#         data = (('matches_played', 'matches_played + 1'),('match_wins', ('match_wins + ' + win)),('match_losses', ('match_losses + ' + loss)), ('tour_points',('tour_points +' + points)))
        
        DB.update(data)  
#         queryContent = "UPDATE tournament_players SET matches_played = matches_played + 1," \
#             " match_wins = match_wins + {}, match_losses = match_losses + {}, tour_points = tour_points + {} WHERE tour_id = {} AND player_id = {}".format(win,loss,points,t_ID,playerID)

# Next version method for updating players globl statistcis form multiple tournaments.
# I've elected to not include this because the assignment requires the deletion of player records
# and it I did not want players of the same name constantly being created in the players table.
# That being said, it would have no effect other than creating a mess.    
def updateGlobalStats():
    #TODO
    pass
    
# Method that creates the next set of matches
# Requires player1, player2 which the match contestants, the current tournament id (tourID) and the round (tour_round)
def createMatches(player1, player2, tourID='1', tour_round = '1'):
    
# Next version, allows for testing for None so bye need not have a player ID
#     if player2 == "bye":
#         player2 = None
    
    DB = connect()
    DB.tableName = ('match_pairings',)
    
    values = ('tour_id', 'player1', 'player2', 'round')
    data = (tourID, player1, player2, tour_round)
    
    DB.create(values, data)
#     queryContent = "INSERT INTO match_pairings (tour_id, player1, player2, round)" \
#             " VALUES({},{},{},{})".format(tourID, player1, player2, tour_round)

# A method used in testing to clear data related to default tournament 1 used for the assignment.           
def clearTestData():
    
    DB = connect()
    DB.tableName = ('match_pairings', 'tournament_players')
    DB.restrict = True
    DB.restrictWhere = (('tour_id', '1'),)
    
#     queryContent1 = "DELETE FROM match_pairings WHERE tour_id = 1"
#     queryContent2 = "DELETE FROM tournament_players WHERE tour_id = 1"

# Deletes all matches
def deleteMatches(tourID='1'):
    """Remove all the match records from the database."""
    
    DB = connect()
    DB.restrict = True
    DB.restrictWhere = (('tour_id', '1'),)
    DB.tableName = ('match_pairings',)
    DB.delete()
    DB.tableName = ('tournament_players',)
    DB.delete()

    print('All matches for tournament {} have been removed').format(tourID)
    
# Deletes all players and their global statistics from players table
def deletePlayerRegistry():
    DB = connect()
    
    DB.tableName = ('players',)
    DB.delete()

    print("All player records have been deleted form the registry")
    
# Deletes all players from a particular tournament. Accepts a tournament id.
def deletePlayers(tourID='1'):
    """Remove all the player records from the database."""

    DB = connect()
    DB.tableName = ('tournament_players',)
    DB.restrict = True
    DB.restrictWhere = (('tour_ID', tourID),)
    DB.delete()

    print("All player records have been deleted form the tournament")
    
    deleteMatches()
    deletePlayerRegistry()

# Method to return a count of the number of players registered for a tournament.
# Accepts one default argument for current tournament (tourID)
def countPlayers(tourID='1'):
    """Returns the number of players currently registered."""

    DB = connect()
    DB.tableName = ('tournament_players',)
    DB.restrict = True
    DB.restrictWhere = (('tour_ID', tourID),)
    DB.count = True
    results = DB.read()

    print("Total number of Players = " + str(results[0][0]))
    return results[0][0] 

# Add a player, argument (name), to the global players table 'players'
def createPlayer(name):
    
    DB = connect()
    DB.tableName = ('players',)
    DB.queryReturn = True
    results = DB.create(('name',), (name,))

    del(DB.tableName)
    return results

# Adds a player to the default tournament per assignment requirements described below.
def registerPlayer(name):
    """Adds a player to the players table in the tournament database.
       This will probably need to be updated to include the tournamentPlayers table as well for
       project testing
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    newPlayer = createPlayer(name)
    newPlayerID = newPlayer[0][0]

    values = ('player_id', 'tour_id', 'tour_points')
    data = (newPlayerID, '1', '0')

    DB = connect()
    DB.tableName = ('tournament_players',)

    DB.create(values, data)

# As below but included a default tournament ID related to the assignment
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
    
    DB = connect()
    DB.tableName = ('tournament_players','players')
    DB.multiSelect = True
    DB.select = ('tournament_players.player_id', 'players.name', 'tournament_players.match_wins', 'tournament_players.matches_played')
    DB.restrict = True
    DB.restrictWhere = (('tournament_players.tour_id', tourID),)
    DB.queryReturn = True
    DB.queryConditions = (('AND tournament_players.player_id','players.id'),)
    DB.orderBy = 'tournament_players.match_wins'
    results = DB.read()
    print(results)
    
#     queryContent = "SELECT tournament_players.player_id, players.name, tournament_players.match_wins, " \
#         "tournament_players.matches_played from tournament_players, players where " \
#         "tournament_players.tour_id = {} and tournament_players.player_id = players.id ORDER BY tournament_players.match_wins".format(tourID)
#     
    return results
    
# Takes two arguments and returns one to represent winner.
# This would need to be updated to allow for multiple contestants.
def whoWonGenerator(p1, p2):
    winner = randint(1, 2)
    
    if winner == 1:
        return p1
    else:
        return p2

# This would be used to determine the number of rounds necessary to determine a winner
def numberRounds(tourID='1'):
    numPlayers = countPlayers()
    numberRounds = math.log2(numPlayers)
    
    print "The current number of rounds for {} players is {}".format(str(numPlayers),str(numberRounds))
    
    return numberRounds

# Reports the results of an individual match.
# Takes 4 arguments, 2 players (winner and loser) and 2 default arguments for the tournament id and round.
def reportMatch(winner, loser, tourID = '1', tour_round='1'):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Populates the match_pairings table for use in swiss pairings.
    createMatches(winner, loser)
    
    DB = connect()
    DB.tableName = ('match_pairings',)
    DB.restrict = True
    DB.restrictWhere = (('tour_id', tourID),('round', tour_round),('player1', winner))
    DB.queryConditions = (('OR player2', winner),)
    firstQuery = DB.read()
    
#     queryContent1 = "SELECT * FROM match_pairings WHERE " \
#         "tour_id = {} AND round = {} AND player1 = {} OR player2 = {}".format(tourID,tour_round, winner, winner)
    
    print firstQuery
    
    matchID = firstQuery[0][0]
    
    print("Match ID = {}").format(matchID)
    
    DB.tableName = ('match_results',)
    values = ('match_id','player_id','is_winner','is_bye','points_awarded')
    
    if loser == "bye":
        win_data = (matchID, winner, True, True, 10)
#         queryContent2 = "INSERT INTO match_results (match_id, player_id,is_winner, is_bye, points_awarded) " \
#             "values ({},{}, true, true, 10)".format(matchID, winner)
    else:
        win_data = (matchID, winner, True, False, 10)
#         queryContent2 = "INSERT INTO match_results (match_id, player_id, is_winner, is_bye, points_awarded) " \
#             "values ({},{}, true, false, 10),({},{}, false, false, 0)".format(matchID, winner)
    DB.create(values, win_data)
    
    lose_data = (matchID, loser, False, False, 0)
    
    DB.create(values, lose_data)
    
# Test to determine if a number is odd.
# Allows for the creation of bye rounds if necessary.   
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
    
    #Need to figure out when/how to update standings
    updateTourStats()
    
    DB = connect()
    DB.multiSelect = True
    DB.select = ('players.id', 'tournament_players.player_id', 'players.name', 'tournament_players.tour_points') 
    DB.tableName = ('players', 'tournament_players')
    DB.restrict = True
    DB.restrictWhere = (('tour_id','1'),)
    DB.queryConditions = (('AND players.id','tournament_players.player_id' ),)
    DB.orderBy = 'tour_points'
    regPlayerInfo = DB.read()
    regPlayerCount = DB.rowCount
    print("regPlayer info =" + str(regPlayerInfo))
 
#     queryContent = "select players.id, tournament_players.player_id, players.name, tournament_players.tour_points from players, tournament_players where tour_id = '1' AND players.id = tournament_players.player_id ORDER BY tour_points;".format(tourID)
#     regPlayerInfo = cursor.fetchall()
#     regPlayerCount = cursor.rowcount
    
    oddNumEntrants = isOdd(regPlayerCount)
    
    if oddNumEntrants == False:
        print "Even Number of contestants"
    else:
        print "Odd number of contestants"
        
    i = 1
    match = 1
    matchList = []
    
    # Logic to both create matches based on the order returned(by points) and create bye rounds and record accordingly.
    # The pairings are arranged by points to allow for similar player abilities.
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
        
    print "Total number of players = {} ".format(regPlayerCount)
    print matchList
    return matchList
    
    DB.close()

