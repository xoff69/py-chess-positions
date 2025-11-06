-- Jeux de parties
\COPY games (file_name, game_index, event, site, date, round, white, black, result, eco, moves)    FROM '/data/games_2013.csv' WITH (FORMAT csv, HEADER true);


-- Positions temporaires
\COPY tmp_position_games (    zobrist, game_id, fen,    white_queens, black_queens,    white_rooks, black_rooks,    white_bishops, black_bishops,    white_knights, black_knights,    white_pawns, black_pawns,    isGrandRoqueBlanc, isGrandRoqueNoir,    isPetitRoqueBlanc, isPetitRoqueNoir,    bxf7, bxh6, bxf2, bxh3,    doublecheck, ep, foudecouleuropposee,    pat, pionsdoubles, pionstriples) FROM '/data/position_games_2013.csv' WITH (FORMAT csv, HEADER true);




-- Insertion des Zobrist uniques dans positions
-- 1. Ajout des nouvelles positions uniques
INSERT INTO positions (zobrist)
SELECT DISTINCT zobrist
FROM tmp_position_games
ON CONFLICT (zobrist) DO NOTHING;

-- 2. Lien entre position ↔ partie
INSERT INTO position_games (
    position_id, game_id, fen,
    white_queens, black_queens,
    white_rooks, black_rooks,
    white_bishops, black_bishops,
    white_knights, black_knights,
    white_pawns, black_pawns,
    isGrandRoqueBlanc, isGrandRoqueNoir,
    isPetitRoqueBlanc, isPetitRoqueNoir,
    bxf7, bxh6, bxf2, bxh3,
    doublecheck, ep, foudecouleuropposee,
    pat, pionsdoubles, pionstriples
)
SELECT
    p.id, t.game_id, t.fen,
    t.white_queens, t.black_queens,
    t.white_rooks, t.black_rooks,
    t.white_bishops, t.black_bishops,
    t.white_knights, t.black_knights,
    t.white_pawns, t.black_pawns,
    t.isGrandRoqueBlanc, t.isGrandRoqueNoir,
    t.isPetitRoqueBlanc, t.isPetitRoqueNoir,
    t.bxf7, t.bxh6, t.bxf2, t.bxh3,
    t.doublecheck, t.ep, t.foudecouleuropposee,
    t.pat, t.pionsdoubles, t.pionstriples
FROM tmp_position_games t
JOIN positions p ON p.zobrist = t.zobrist;

truncate  tmp_position_games;

--DROP TABLE IF EXISTS tmp_position_games;

