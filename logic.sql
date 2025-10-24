DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS positions CASCADE;
DROP TABLE IF EXISTS position_games CASCADE;

-- Table des parties (id auto)
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

-- Table des positions uniques
CREATE TABLE positions (
    id BIGSERIAL PRIMARY KEY,
    zobrist NUMERIC(20,0) UNIQUE
);

-- Table de liaison position ↔ partie
CREATE TABLE position_games (
    position_id BIGINT REFERENCES positions(id),
    game_id BIGINT REFERENCES games(id),
    fen TEXT
);
DROP INDEX idx_positions_zobrist;
DROP INDEX idx_position_games_position_id;
DROP INDEX idx_position_games_game_id;

-- Index utiles
CREATE INDEX idx_positions_zobrist ON positions(zobrist);
CREATE INDEX idx_position_games_position_id ON position_games(position_id);
CREATE INDEX idx_position_games_game_id ON position_games(game_id);
DROP TABLE IF EXISTS tmp_position_games;
CREATE TABLE tmp_position_games (
  zobrist NUMERIC(20,0),
  game_id BIGINT,
  fen TEXT
);