-- Table definitions for the tournament project.
-- Created by Victor Asselta for Udacity project 2 of the Full Stack Nanodegree
-- 
-- The following schema was designed to support multiple tournaments, permanent player records
-- between tournaments, and an overall points system. It's an attempt to solve the problem
-- introduced in the project where data is wiped out between rounds yet still allow for
-- multiple tournaments and overall player standings for a round, tournament, and multiple tournaments.
--
-- This is the initialization scheme for t

-- Player names and sequenced ids, 1NF,2NF,3NF
-- Stores Global player data to allow for statistics over the course of many tournaments
CREATE TABLE players (
		id SERIAL PRIMARY KEY,
		name TEXT,
		num_tours INTEGER,
		num_matches INTEGER,	
);


-- Tournament names and sequenced ids, to allow for multiple tournaments and statistics 1NF, 2NF, 3NF
CREATE TABLE tournaments ( 
		id SERIAL PRIMARY KEY, 
		name TEXT,
		match_points INTEGER DEFAULT 10,
		tour_points INTEGER DEFAULT 20,
		winner TEXT,
);

-- A link table (tournament & players) for player tournament registration and local statistics
CREATE TABLE tournament_players ( 
		player_id INTEGER REFERENCES players(id),
		tour_id INTEGER REFERENCES tournaments(id),
		match_wins INTEGER DEFAULT 0,
		match_losses INTEGER DEFAULT 0,
		matches_played INTEGER DEFAULT 0,
		tour_points INTEGER DEFAULT 0,
		PRIMARY KEY(tour_id, player_id)
);

-- Table to store player pairings per rounds. Inluded a serial ID to identify each round uniquely.
CREATE TABLE match_pairings (
		id SERIAL PRIMARY KEY,
		tour_id INTEGER REFERENCES tournaments(id),
		player1 INTEGER REFERENCES players(id),
		player2 INTEGER REFERENCES players(id),
		round INTEGER
);

-- Table to store match results for unique pairings.
CREATE TABLE match_results (
		match_id INTEGER REFERENCES match_pairings(id) ON DELETE CASCADE,
		player_id INTEGER REFERENCES players(id),
		is_winner BOOL,
		is_bye BOOL,
		points_awarded INTEGER,
		PRIMARY KEY(match_id, player_id)

);

-- View used to allow for easier statistics updates. (winner, bye round, points, matchid, tourid)
CREATE VIEW match_pairings_results AS
		SELECT 
			mp.tour_id, 
			mp.id as match_id, 
			mr.player_id, mr.is_winner, 
			mr.is_bye, mr.points_awarded
		FROM match_pairings as mp 
		JOIN match_results as mr
		ON mp.id = mr.match_id;
		
CREATE VIEW pairings AS
		select 
			p.id,
			tp.tour_id,
			tp.player_id, 
			p.name, 
			tp.tour_points 
			from players as p, tournament_players as tp
			ON players.id = tournament_players.player_id ORDER BY tour_points;
