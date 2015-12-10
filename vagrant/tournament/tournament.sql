-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Connect to the postgres DB to ensure there are no open connections to the 
-- tournament DB; remove all open sessions/connections. Finally try to DROP the 
-- tournament DB.
\c postgres
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity 
WHERE pg_stat_activity.datname = current_database() AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS tournament;

-- Create a fresh DB with necessary tables 
CREATE DATABASE tournament;
\c tournament;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS players;

CREATE TABLE players(
	_id 	SERIAL PRIMARY KEY,
	name 	TEXT NOT NULL,
	matches	INTEGER NOT NULL DEFAULT 0,
	wins 	INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE matches(
	_id SERIAL PRIMARY KEY,
	winner INTEGER NOT NULL REFERENCES players(_id) ON DELETE CASCADE,
	loser INTEGER NOT NULL REFERENCES players(_id) ON DELETE CASCADE
	CHECK (winner <> loser)
);

CREATE VIEW player_standings AS SELECT _id, name, wins, matches FROM players 
ORDER BY wins DESC;

COMMIT;
