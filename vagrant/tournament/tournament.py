#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import logging
import sys


def connect(db_name='tournament'):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect('dbname={}'.format(db_name))
        cursor = conn.cursor()
    except Exception, e:
        print 'Unable to connect to database; exiting!'
        logging.exception(e)
        sys.exit(1)
        
    return conn, cursor


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM matches;")
    cursor.execute("UPDATE players SET matches = 0, wins = 0;")
    db.commit()

    cursor.close()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM players;")
    db.commit()

    cursor.close()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    cursor.execute("SELECT COUNT(*) FROM players;")
    res = cursor.fetchone()
    count = res[0]

    cursor.close()
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect();
    query = """INSERT INTO players (name) VALUES (%s);"""
    args = (name,)
    cursor.execute(query, args)
    db.commit()

    cursor.close()
    db.close()


def playerStandings():
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
    db, cursor = connect();
    cursor.execute("SELECT * FROM player_standings;")
    res = cursor.fetchmany(countPlayers())

    cursor.close()
    db.close()
    return res


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    # Update the matches table with match details
    match_query = """INSERT INTO matches (winner, loser) VALUES (%s, %s)"""
    match_args = (winner, loser)
    cursor.execute(match_query, match_args)

    # Update players table with details of played matches and wins
    query = """UPDATE players SET matches = matches + 1 WHERE _id IN (%s, %s)"""
    args = (winner, loser)
    cursor.execute(query, args)

    query = """UPDATE players SET wins = wins + 1 WHERE _id = %s"""
    args = (winner,)
    cursor.execute(query, args)
    db.commit()

    cursor.close()
    db.close()
 

def swissPairings():
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
    standings = playerStandings()
    if len(standings)%2 != 0:
        print 'No. of entries not even; current solution supports only an even number of players'
        return

    pairings = []
    #The next two players to be paired are always the first two elements in
    #the list. User indices 0, 1 to retrieve the player tuple and retrieve 
    #their id's and names from the tuple.
    while len(standings) > 0:
        player1 = standings[0][0], standings[0][1] #a tuple with id and name
        player2 = standings[1][0], standings[1][1]
        pairings.append((player1[0], player1[1], player2[0], player2[1]))

        standings = standings[2:]

    return pairings

