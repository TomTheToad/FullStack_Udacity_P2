#!/usr/bin/env python
#
# version 3.2
# tournament.py -- implementation of a Swiss-system tournament
# Created by Victor Asselta
# written for project2 in Udacity's Full Stack NanoDegree
# Please see the accompanying README file.
# This file represents an attempt to satisfy all extra credit and
# some areas of my own interest.
#

import math
import os
from random import randint
from DB_Handler import DB_Handler


# Fields
# Track to see if first run is true for current call
# Known bug, appears to continue to call with testing.
# Solution: make tournament.py class in next version and
# set using decorator.
runInit = True

# If first run of tournament then check to see if database schema exists
# and create it if not.


def __createDB():

    try:
        scriptReturn = os.system("createdb tournament")

        if scriptReturn == 0:
            print("Tournament database created")
    except:
        print("Unable to run system calls. "
              "Please see the setup section in the"
              "README.txt file")


def __initializeDB():
    print("Database Initialization called")

    __createDB()

    firstRun = DB_Handler()
    firstRun.dbname = 'tournament'

    # Attempt to call tournament.sql script file to
    # initialize tournament database

    if os.path.exists("tournament.sql"):
        scriptPath = os.path.realpath("tournament.sql")

        print(scriptPath)

        try:
            queryContent = open(scriptPath, "r").read()
            firstRun.sendQuery(queryContent)
        except:
            print("Tournament Database already exists or there is an error in "
                  "the script file. See README.txt and manually configure if"
                  "necessary.")

        # Set global runInit to False after database created
        global runInit
        runInit = False


# Used to call an instance of DB_Handler and set some basic
# parameters for the connection
def connect(query):
    DB = DB_Handler()
    DB.dbname = 'tournament'

    global runInit

    # Check for first run condition
    # If True then run initialization query calling tournament.sql script
    if runInit is True:
        __initializeDB()

    returnedResults = DB.sendQuery(query)

    return returnedResults


# Fetches a previous created view used for updating player statistics.
def fetchResultsView():

    queryContent = "SELECT * FROM match_pairings_results;"
    returnedResults = connect(queryContent)

    return returnedResults


# Functionality for use with multiple tournaments
# Test tournament will be added with __initializeDB()
def createTournament(tournamentName):

    t_name = "'" + str(tournamentName) + "'"
    queryContent = 'INSERT INTO tournaments (name) VALUES (%s);' % (t_name)

    connect(queryContent)


# Uses the above view to update tournament statistics for
# wins, losses, matches played, and points
def updateTourStats(tourID='1'):
    playerStats = fetchResultsView()

    for player in playerStats:

        # Extrapolate player statistics from dictionary.
        t_ID = tourID
        playerID = player[2]

        # Test to see if player won or lost this match.
        if player[3] == True:
            win = 1
            loss = 0
            points = 10
        else:
            win = 0
            loss = 1
            points = 0

        queryContent = "UPDATE tournament_players SET matches_played = "\
            " matches_played + 1, match_wins = match_wins + {}, "\
            "match_losses = match_losses + {}, tour_points = tour_points + {}"\
            " WHERE tour_id = {} AND player_id = {} "\
            "RETURNING *".format(win, loss, points, t_ID, playerID)

        # Check for Bye None player before sending query
        if playerID is not None:
            connect(queryContent)


# Method that creates the next set of matches
# Requires player1, player2 which the match contestants, the current tournament
# id (tourID) and the round (tour_round)
def createMatches(player1, player2, tourID='1', tour_round='1'):

    if player2 == "bye":
        player2 = None

    values = "{},{},{},{}".format(tourID, player1, player2, tour_round)
    queryContent = "INSERT INTO match_pairings "\
        "(tour_id, player1, player2, round)"\
        " VALUES(%s)" % (values)

    returnedResults = connect(queryContent)
    return returnedResults


# Deletes all matches
def deleteMatches(tourID='1'):
    """Remove all the match records from the database."""

    queryContent = "DELETE FROM match_pairings "\
        "WHERE tour_id = {};".format(tourID)
    connect(queryContent)

    queryContent2 = "DELETE FROM tournament_players "\
        "WHERE tour_id = {}".format(tourID)
    connect(queryContent2)

    print('All matches for tournament {} have been removed').format(tourID)


# Deletes all players and their global statistics from players table
# Remove for use with interface use to keep players over multiple tournaments.
def deletePlayerRegistry():

    queryContent = "DELETE FROM players"
    connect(queryContent)

    print("All player records have been deleted form the registry")


# Deletes all players from a particular tournament. Accepts a tournament id.
def deletePlayers(tourID='1'):
    """Remove all the player records from the database."""

    queryContent = "DELETE FROM tournament_players "\
        "WHERE tour_id = {};".format(tourID)
    connect(queryContent)

    print("All player records have been deleted form the tournament")

    deleteMatches()
    deletePlayerRegistry()


# Method to return a count of the number of players registered in a tournament.
# Accepts one default argument for current tournament (tourID)
def countPlayers(tourID='1'):
    """Returns the number of players currently registered."""

    queryContents = "SELECT count(*) FROM tournament_players "\
        "WHERE tour_id = {};".format(tourID)
    numPlayers = connect(queryContents)

    print("Total number of Players = " + str(numPlayers[0][0]))
    return numPlayers[0][0]


# Add a player, argument (name), to the global players table 'players'
def createPlayer(name):

    str(name)
    playerName = name.replace("'", " ")

    value = "'{}'".format(playerName)
    queryContent = "INSERT INTO players (name) VALUES (%s) "\
        "RETURNING *" % (value)

    playerInfo = connect(queryContent)
    returnValue = [playerInfo[0][0], playerInfo[0][1]]

    return returnValue


# Adds a player to the default tournament per assignment requirements below.
def registerPlayer(name, tourID='1'):
    """Adds a player to the players table in the tournament database.
       This will probably need to be updated to include the tournamentPlayers
       table as well for project testing

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    playerInfo = createPlayer(name)
    playerID = playerInfo[0]
    playerName = str(playerInfo[1])

    value = "'{}','{}'".format(playerID, tourID)
    queryContent = "INSERT INTO tournament_players "\
        "(player_id, tour_id, tour_points) VALUES (%s, 0)" % (value)

    connect(queryContent)

    print("Added Player: " + playerName + " with ID " +
          str(playerID) + " to registry.")


# As below but included a default tournament ID related to the assignment
def playerStandings(tourID='1'):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # Make sure tour stats are current
    updateTourStats()

    queryContent = "SELECT id, name, wins, matches_played "\
        "FROM pairings ORDER BY points DESC;".format(tourID)

    results = connect(queryContent)

    return results


# Takes two arguments and returns one to represent winner.
# This would need to be updated to allow for multiple contestants.
def whoWonGenerator(p1, p2):
    winner = randint(1, 2)

    if winner == 1:
        return p1
    else:
        return p2


# This would be used to determine the number of rounds
# necessary to determine a winner
def numberRounds(tourID='1'):
    numPlayers = countPlayers()
    numberRounds = math.log2(numPlayers)

    print "The current number of rounds for "\
        "{} players is {}".format(str(numPlayers), str(numberRounds))

    return numberRounds


# Reports the results of an individual match.
# Takes 4 arguments, 2 players (winner and loser) and
# 2 default arguments for the tournament id and round.
def reportMatch(winner, loser, tourID='1', tour_round='1'):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    createMatches(winner, loser)

    values = "tour_id = {} AND round = {} AND player1 = {} "\
        "OR player2 = {}".format(tourID, tour_round, winner, winner)
    queryContent = "SELECT * FROM match_pairings WHERE (%s)" % (values)

    firstQuery = connect(queryContent)

    matchID = firstQuery[0][0]

    if loser == "bye":
        values = "{},{}, true, true".format(matchID, winner)
        winQuery = "INSERT INTO match_results (match_id, player_id, "\
            "is_winner, is_bye) values (%s)" % (values)
    else:
        values = "{},{}, true, false".format(matchID, winner)
        winQuery = "INSERT INTO match_results (match_id, player_id, "\
            "is_winner, is_bye) values (%s)" % (values)

        values = "{},{}, false, false".format(matchID, loser)
        loseQuery = "INSERT INTO match_results (match_id, player_id, "\
                    "is_winner, is_bye) values (%s)" % (values)

        print(loseQuery)
        connect(loseQuery)

    connect(winQuery)


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
    regPlayerInfo = playerStandings()
    regPlayerCount = countPlayers()

    # Determine if player number is odd to allow for bye rounds
    oddNumEntrants = isOdd(regPlayerCount)

    # Output results of previous test to console
    if oddNumEntrants is False:
        print "Even Number of contestants"
    else:
        print "Odd number of contestants"

    # The following logic is a means to determine pairings for the entrants
    # dependent upon their place in the standings.
    # Outputs results of logic to console and returns the new match list.
    i = 1
    match = 1
    matchList = []

    str(match)
    str(regPlayerInfo)

    while i < regPlayerCount:
        print "match {} : contestants {} "\
            "and {}".format(match, regPlayerInfo[i - 1][0],
                            regPlayerInfo[i][0])
        matchList.append((regPlayerInfo[i - 1][0], regPlayerInfo[i - 1][2],
                          regPlayerInfo[i][0], regPlayerInfo[i][2]))

        match += 1
        i += 2

        # Determines if player is last on list and creates a bye round.
        # Will be necessary for bye rounds in interface.
        if i == regPlayerCount:
            print "match {} : contestants {} "\
                "has a bye round".format(match, regPlayerInfo[i - 1][0])
            # might create an error because bye does not have an id. FIX
            matchList.append((regPlayerInfo[i - 1][0],
                              regPlayerInfo[i - 1][2], 'bye', 'bye'))

    print "Total number of players = {} ".format(regPlayerInfo.__len__())
    return matchList
