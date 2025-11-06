SELECT g.file_name, g.white, g.black, pg.fen
FROM position_games pg
JOIN games g ON g.id = pg.game_id
WHERE pg.pionsdoubles = TRUE
  AND pg.white_pawns <= 8
  AND pg.black_pawns <= 8
LIMIT 20;


