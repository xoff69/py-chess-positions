-- Nettoyage
DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS positions CASCADE;
DROP TABLE IF EXISTS position_games CASCADE;
DROP TABLE IF EXISTS tmp_position_games;

-- ==============================
-- 1️⃣  Tables principales
-- ==============================

CREATE TABLE games (
    id BIGSERIAL PRIMARY KEY,
    file_name TEXT,
    game_index INT,
    event TEXT,
    site TEXT,
    date TEXT,
    round TEXT,
    white TEXT,
    black TEXT,
    result TEXT,
    eco TEXT,
    moves TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE positions (
    id BIGSERIAL PRIMARY KEY,
    zobrist NUMERIC(20,0) UNIQUE
);

CREATE TABLE position_games (
    position_id BIGINT REFERENCES positions(id),
    game_id BIGINT REFERENCES games(id),
    fen TEXT,
    white_queens INT,
    black_queens INT,
    white_rooks INT,
    black_rooks INT,
    white_bishops INT,
    black_bishops INT,
    white_knights INT,
    black_knights INT,
    white_pawns INT,
    black_pawns INT,
    isGrandRoqueBlanc BOOLEAN,
    isGrandRoqueNoir BOOLEAN,
    isPetitRoqueBlanc BOOLEAN,
    isPetitRoqueNoir BOOLEAN,
    bxf7 BOOLEAN,
    bxh6 BOOLEAN,
    bxf2 BOOLEAN,
    bxh3 BOOLEAN,
    doublecheck BOOLEAN,
    ep BOOLEAN,
    foudecouleuropposee BOOLEAN,
    pat BOOLEAN,
    pionsdoubles BOOLEAN,
    pionstriples BOOLEAN
);

-- ==============================
-- 2️⃣  Table temporaire
-- ==============================

DROP TABLE IF EXISTS tmp_position_games;

CREATE TABLE tmp_position_games (
    zobrist NUMERIC(20,0),
    game_id BIGINT,
    fen TEXT,
    white_queens SMALLINT,
    black_queens SMALLINT,
    white_rooks SMALLINT,
    black_rooks SMALLINT,
    white_bishops SMALLINT,
    black_bishops SMALLINT,
    white_knights SMALLINT,
    black_knights SMALLINT,
    white_pawns SMALLINT,
    black_pawns SMALLINT,

    -- Flags logiques
    isGrandRoqueBlanc BOOLEAN,
    isGrandRoqueNoir BOOLEAN,
    isPetitRoqueBlanc BOOLEAN,
    isPetitRoqueNoir BOOLEAN,
    bxf7 BOOLEAN,
    bxh6 BOOLEAN,
    bxf2 BOOLEAN,
    bxh3 BOOLEAN,
    doublecheck BOOLEAN,
    ep BOOLEAN,
    foudecouleuropposee BOOLEAN,
    pat BOOLEAN,
    pionsdoubles BOOLEAN,
    pionstriples BOOLEAN
);


-- ==============================
-- 3️⃣  Index utiles
-- ==============================

DROP INDEX IF EXISTS idx_positions_zobrist;
DROP INDEX IF EXISTS idx_position_games_position_id;
DROP INDEX IF EXISTS idx_position_games_game_id;

CREATE INDEX idx_positions_zobrist ON positions(zobrist);
CREATE INDEX idx_position_games_position_id ON position_games(position_id);
CREATE INDEX idx_position_games_game_id ON position_games(game_id);
