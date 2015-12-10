-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--PRAGMA journal_mode=truncate;

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS players;

CREATE TABLE players(
	_id 	SERIAL PRIMARY KEY,
	name 	TEXT NOT NULL,
	matches	INTEGER NOT NULL DEFAULT 0,
	wins 	INTEGER NOT NULL DEFAULT 0);

COMMIT;
