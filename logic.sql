-- ===========================================
-- 1️⃣ Table principale des parties
-- ===========================================

CREATE TABLE IF NOT EXISTS games (
    id BIGINT PRIMARY KEY,
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
    moves TEXT,            -- format PGN
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_games_white_black ON games(white, black);
CREATE INDEX IF NOT EXISTS idx_games_date ON games(date);
CREATE INDEX IF NOT EXISTS idx_games_eco ON games(eco);


-- ===========================================
-- 2️⃣ Table des positions uniques
-- ===========================================

CREATE TABLE IF NOT EXISTS positions (
    id BIGSERIAL PRIMARY KEY,
    zobrist NUMERIC(20,0) UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_positions_zobrist ON positions(zobrist);


-- ===========================================
-- 3️⃣ Table de liaison position ↔ partie
-- ===========================================

DROP TABLE IF EXISTS position_games CASCADE;

CREATE TABLE position_games (
    position_id BIGINT REFERENCES positions(id) ON DELETE CASCADE,
    game_id BIGINT REFERENCES games(id) ON DELETE CASCADE,
    fen TEXT,
    PRIMARY KEY (position_id, game_id)
);

CREATE INDEX idx_position_games_position_id ON position_games(position_id);
CREATE INDEX idx_position_games_game_id ON position_games(game_id);
CREATE INDEX idx_position_games_fen ON position_games(fen);


-- ===========================================
-- 4️⃣ Import temporaire depuis CSV
-- ===========================================

DROP TABLE IF EXISTS tmp_position_games;

CREATE TABLE tmp_position_games (
  zobrist NUMERIC(20,0),
  game_id BIGINT,
  fen TEXT
);

-- ⚙️ Import (adapter le chemin)
\COPY games (id, file_name, game_index, event, site, date, round, white, black, result, eco, moves)
FROM '/data/games_2015.csv'
WITH (FORMAT csv, HEADER true);

\COPY tmp_position_games FROM '/data/position_games_2015.csv' WITH (FORMAT csv, HEADER true);


-- ===========================================
-- 5️⃣ Injection dans les vraies tables
-- ===========================================

-- 🔸 Ajouter les positions uniques
INSERT INTO positions (zobrist)
SELECT DISTINCT zobrist
FROM tmp_position_games
ON CONFLICT DO NOTHING;

-- 🔸 Créer les liens position ↔ partie
INSERT INTO position_games (position_id, game_id, fen)
SELECT p.id, t.game_id, t.fen
FROM tmp_position_games t
JOIN positions p ON p.zobrist = t.zobrist
ON CONFLICT DO NOTHING;


-- ===========================================
-- 6️⃣ Nettoyage (optionnel)
-- ===========================================
DROP TABLE IF EXISTS tmp_position_games;

VACUUM ANALYZE;
