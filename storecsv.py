import os
import csv
import chess
import chess.pgn
import zipfile
from time import time
import random
from io import StringIO

# ------------------------------
# Zobrist table stable
# ------------------------------
random.seed(12345)
zob_table = [[random.getrandbits(64) for _ in range(12)] for _ in range(64)]
side_to_move = random.getrandbits(64)

piece_index = {
    'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
    'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11
}

def zobrist_hash(board):
    h = 0
    for square in range(64):
        piece = board.piece_at(square)
        if piece:
            idx = piece_index[piece.symbol()]
            h ^= zob_table[square][idx]
    if board.turn == chess.BLACK:
        h ^= side_to_move
    return h

# ------------------------------
# Matériel par couleur
# ------------------------------
def get_material(board):
    counts = {
        "white_queens": len(board.pieces(chess.QUEEN, chess.WHITE)),
        "black_queens": len(board.pieces(chess.QUEEN, chess.BLACK)),
        "white_rooks": len(board.pieces(chess.ROOK, chess.WHITE)),
        "black_rooks": len(board.pieces(chess.ROOK, chess.BLACK)),
        "white_bishops": len(board.pieces(chess.BISHOP, chess.WHITE)),
        "black_bishops": len(board.pieces(chess.BISHOP, chess.BLACK)),
        "white_knights": len(board.pieces(chess.KNIGHT, chess.WHITE)),
        "black_knights": len(board.pieces(chess.KNIGHT, chess.BLACK)),
        "white_pawns": len(board.pieces(chess.PAWN, chess.WHITE)),
        "black_pawns": len(board.pieces(chess.PAWN, chess.BLACK)),
    }
    return counts

# ------------------------------
# Flags logiques
# ------------------------------
def compute_flags(board):
    flags = {}
    flags["isGrandRoqueBlanc"] = board.has_queenside_castling_rights(chess.WHITE)
    flags["isGrandRoqueNoir"] = board.has_queenside_castling_rights(chess.BLACK)
    flags["isPetitRoqueBlanc"] = board.has_kingside_castling_rights(chess.WHITE)
    flags["isPetitRoqueNoir"] = board.has_kingside_castling_rights(chess.BLACK)
    flags["ep"] = board.ep_square is not None
    flags["pat"] = board.is_stalemate()

    # Pions triplés
    flags["pionstriples"] = False
    flags["pionsdoubles"] = False
    for color in [chess.WHITE, chess.BLACK]:
        pawns = board.pieces(chess.PAWN, color)
        files = [chess.square_file(sq) for sq in pawns]
        if any(files.count(f) >= 3 for f in set(files)):
            flags["pionstriples"] = True
        if any(files.count(f) == 2 for f in set(files)):
            flags["pionsdoubles"] = True

    # Cases vides pour bxf7, etc. (simplifié)
    flags["bxf7"] = False
    flags["bxh6"] = False
    flags["bxf2"] = False
    flags["bxh3"] = False
    flags["doublecheck"] = False
    flags["foudecouleuropposee"] = False

    return flags

# ------------------------------
# Parsing PGN
# ------------------------------
def process_pgn_stream(stream, filename, game_id_start):
    games_list = []
    pos_list = []
    game_index = 0
    game_id = game_id_start

    while True:
        game = chess.pgn.read_game(stream)
        if game is None:
            break

        game_index += 1
        game_id += 1
        headers = game.headers

        # moves text
        moves_text = ""
        board = game.board()
        for move in game.mainline_moves():
            moves_text += board.san(move) + " "
            board.push(move)

        # positions
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            zob = zobrist_hash(board)
            material = get_material(board)
            flags = compute_flags(board)

            pos_list.append([
                zob, game_id, board.fen(),
                material["white_queens"], material["black_queens"],
                material["white_rooks"], material["black_rooks"],
                material["white_bishops"], material["black_bishops"],
                material["white_knights"], material["black_knights"],
                material["white_pawns"], material["black_pawns"],
                flags["isGrandRoqueBlanc"], flags["isGrandRoqueNoir"],
                flags["isPetitRoqueBlanc"], flags["isPetitRoqueNoir"],
                flags["bxf7"], flags["bxh6"], flags["bxf2"], flags["bxh3"],
                flags["doublecheck"], flags["ep"], flags["foudecouleuropposee"],
                flags["pat"], flags["pionsdoubles"], flags["pionstriples"]
            ])

        # game info
        games_list.append([
            filename, game_index,
            headers.get("Event",""),
            headers.get("Site",""),
            headers.get("Date",""),
            headers.get("Round",""),
            headers.get("White",""),
            headers.get("Black",""),
            headers.get("Result",""),
            headers.get("ECO",""),
            moves_text.strip()
        ])

    return games_list, pos_list, game_id

# ------------------------------
# Traitement fichier
# ------------------------------
def process_file(path, game_id_start):
    games_list_total = []
    pos_list_total = []
    game_id = game_id_start

    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path, "r") as z:
            for name in z.namelist():
                if not name.lower().endswith(".pgn"):
                    continue
                with z.open(name) as f:
                    text = f.read().decode("utf-8", errors="ignore")
                    games, pos, game_id = process_pgn_stream(StringIO(text), name, game_id)
                    games_list_total.extend(games)
                    pos_list_total.extend(pos)
    else:
        with open(path, encoding="utf-8", errors="ignore") as f:
            games, pos, game_id = process_pgn_stream(f, os.path.basename(path), game_id)
            games_list_total.extend(games)
            pos_list_total.extend(pos)

    return games_list_total, pos_list_total, game_id

# ------------------------------
# Génération CSV
# ------------------------------
def generate_csvs(root_dir):
    start_time = time()
    game_id = 0
    out_dir = os.path.join(os.getcwd(), "csv")
    os.makedirs(out_dir, exist_ok=True)

    for subdir, _, files in os.walk(root_dir):
        pgn_files = [os.path.join(subdir, f) for f in files if f.lower().endswith((".pgn", ".zip"))]
        if not pgn_files:
            continue

        sub_name = os.path.basename(os.path.normpath(subdir))
        games_csv = os.path.join(out_dir, f"games_{sub_name}.csv")
        posgames_csv = os.path.join(out_dir, f"position_games_{sub_name}.csv")

        with open(games_csv, "w", newline="", encoding="utf-8") as gfile, \
             open(posgames_csv, "w", newline="", encoding="utf-8") as pgfile:

            game_writer = csv.writer(gfile)
            pos_writer = csv.writer(pgfile)

            # entêtes CSV
            game_writer.writerow([
                "file_name","game_index","event","site","date","round",
                "white","black","result","eco","moves"
            ])

            pos_writer.writerow([
                "zobrist","game_id","fen",
                "white_queens","black_queens","white_rooks","black_rooks",
                "white_bishops","black_bishops","white_knights","black_knights",
                "white_pawns","black_pawns",
                "isGrandRoqueBlanc","isGrandRoqueNoir","isPetitRoqueBlanc","isPetitRoqueNoir",
                "bxf7","bxh6","bxf2","bxh3",
                "doublecheck","ep","foudecouleuropposee",
                "pat","pionsdoubles","pionstriples"
            ])

            for fpath in pgn_files:
                print(f"Processing {fpath}...")
                try:
                    games_list, pos_list, game_id = process_file(fpath, game_id)
                    game_writer.writerows(games_list)
                    pos_writer.writerows(pos_list)
                except Exception as e:
                    print(f"⚠️ Erreur dans {fpath}: {e}")

        elapsed = time() - start_time
        m, s = divmod(elapsed, 60)
        print(f"✅ Sous-répertoire {subdir} terminé : {len(pgn_files)} fichiers, temps écoulé {int(m)}m{s:.1f}s")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage : python generate_csvs_zobrist_flags.py <root_pgn_dir>")
        sys.exit(1)
    generate_csvs(sys.argv[1])
