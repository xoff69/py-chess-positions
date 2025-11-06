python storecsv.py C:\\developpement\\pgn\\2016



docker run -d `
  --name chessvger `
  -e POSTGRES_PASSWORD=postgres `
  -v "C:\developpement\chessvger\python\chess-py\chesscount\csv:/data" `
  -v "C:\developpement\chessvger\python\chess-py\chesscount\pgdata:/var/lib/postgresql/data" `
  -p 5434:5432 `
  postgres:16


docker exec -it chessvger psql -U postgres
-- Table des parties
--najdorf
SELECT count(*)
FROM games g
JOIN position_games pg ON g.id = pg.game_id
WHERE pg.fen = 'rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 0 6'
LIMIT 20;
SELECT count(*)
FROM games g
JOIN position_games pg ON g.id = pg.game_id
WHERE pg.fen = 'rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 0 6'
LIMIT 20;


$ ls C:\\home\\echecs\\pgn\\
2025


KingBase x x x
2015  x  x  x
2011 x x x
2013 x x x
2017   x
2019 x
2021 x
2023 x
collections x
events2 x
openings2  x
pgnb x
players2 x
twic1998  x
twic2000 x
twic2002  x
twic2004 x
twic2006 x
twic2008 x
twic2010 x
2012 x
2014 x
2016   x
2018 x
2020 x
2022  x
2024  x
events1 x
openings1 x
pgna x
players1 x
twic1997 x
twic1999 x
twic2001 x
twic2003 x
twic2005 x
twic2007 x
twic2009 x
