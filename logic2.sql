\COPY games (file_name, game_index, event, site, date, round, white, black, result, eco, moves) FROM '/data/games_2015.csv' WITH (FORMAT csv, HEADER true);
\COPY games (file_name, game_index, event, site, date, round, white, black, result, eco, moves) FROM '/data/games_2017.csv' WITH (FORMAT csv, HEADER true);
\COPY games (file_name, game_index, event, site, date, round, white, black, result, eco, moves) FROM '/data/games_KingBase.csv' WITH (FORMAT csv, HEADER true);

\COPY tmp_position_games FROM '/data/position_games_2015.csv' WITH (FORMAT csv, HEADER true);
\COPY tmp_position_games FROM '/data/position_games_2017.csv' WITH (FORMAT csv, HEADER true);
\COPY tmp_position_games FROM '/data/position_games_KingBase.csv' WITH (FORMAT csv, HEADER true);

INSERT INTO positions (zobrist)
SELECT DISTINCT zobrist FROM tmp_position_games
ON CONFLICT DO NOTHING;

INSERT INTO position_games (position_id, game_id, fen)
SELECT p.id, t.game_id, t.fen
FROM tmp_position_games t
JOIN positions p ON p.zobrist = t.zobrist
ON CONFLICT DO NOTHING;
