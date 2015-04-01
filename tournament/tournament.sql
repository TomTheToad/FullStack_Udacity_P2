-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Player names and sequenced ids, puposely seperated from Player Statistics 1NF,2NF,3NF
CREATE TABLE players (
		id SERIAL PRIMARY KEY,
		name TEXT,
		num_tours INTEGER,
		num_matches INTEGER,
		total_match_wins INTEGER,
		total_tour_wins INTEGER,
		total_bye INTEGER,
		total_points INTEGER,
		avg_points_match INTEGER		
);


-- Tournament names and sequenced ids, purposely seperated from Tournament Statistics 1NF, 2NF, 3NF
CREATE TABLE tournaments ( 
		id SERIAL PRIMARY KEY, 
		name TEXT,
		match_points INTEGER DEFAULT 10,
		tour_points INTEGER DEFAULT 20,
		winner TEXT,
		num_rounds INTEGER,
		num_matches INTEGER,
		num_players INTEGER
);

CREATE TABLE tournament_players ( 
		player_id INTEGER REFERENCES players(id),
		tour_id INTEGER REFERENCES tournaments(id),
		match_wins INTEGER DEFAULT 0,
		match_losses INTEGER DEFAULT 0,
		matches_played INTEGER DEFAULT 0,
		tour_points INTEGER DEFAULT 0,
		PRIMARY KEY(tour_id, player_id)
);

CREATE TABLE match_pairings (
		id SERIAL PRIMARY KEY,
		tour_id INTEGER REFERENCES tournaments(id),
		player1 INTEGER REFERENCES players(id),
		player2 INTEGER REFERENCES players(id),
		round INTEGER
);


CREATE TABLE match_results (
		match_id INTEGER REFERENCES match_pairings(id) ON DELETE CASCADE,
		player_id INTEGER REFERENCES players(id),
		is_winner BOOL,
		is_bye BOOL,
		points_awarded INTEGER,
		PRIMARY KEY(match_id, player_id)

);

CREATE VIEW match_pairings_results AS
		SELECT 
			mp.tour_id, 
			mp.id as match_id, 
			mr.player_id, mr.is_winner, 
			mr.is_bye, mr.points_awarded
		FROM match_pairings as mp 
		JOIN match_results as mr
		ON mp.id = mr.match_id;
