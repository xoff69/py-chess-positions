python storecsv.py C:\\home\\echecs\\pgn\\2015



docker run -d   --name pg   -e POSTGRES_PASSWORD=postgres   -v "C:\home\developpement\python\chess-py\chesscount\csv:/data"   -p 5432:5432   postgres:16

docker exec -it pg psql -U postgres
-- Table des parties
--najdorf
SELECT g.*
FROM games g
JOIN position_games pg ON g.id = pg.game_id
WHERE pg.fen = 'rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 0 6'
LIMIT 20;
