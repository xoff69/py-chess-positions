import os
import chess.pgn
from collections import defaultdict
import zipfile
import io
import chess.polyglot

def fens_in_stream(stream, filename_hint=""):
    """Retourne un set de FEN uniques à partir d'un flux texte PGN (fichier ouvert ou contenu zip)."""
    fens = set()
    try:
        while True:
            game = chess.pgn.read_game(stream)
            if game is None:
                break
            board = game.board()
            for move in game.mainline_moves():
                board.push(move)
                fens.add(board.fen())
    except Exception as e:
        print(f"⚠️ Erreur dans {filename_hint}: {e}")
    return fens

def fens_in_file_or_zip(file_path):
    """Lit un fichier .pgn normal ou un .zip contenant des .pgn."""
    fens = set()
    if file_path.lower().endswith(".zip"):
        try:
            with zipfile.ZipFile(file_path, 'r') as z:
                for name in z.namelist():
                    if not name.lower().endswith(".pgn"):
                        continue
                    with z.open(name) as f:
                        content = io.TextIOWrapper(f, encoding="utf-8", errors="ignore")
                        fens |= fens_in_stream(content, filename_hint=f"{file_path}:{name}")
        except Exception as e:
            print(f"⚠️ Erreur lecture zip {file_path}: {e}")
    else:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                fens |= fens_in_stream(f, filename_hint=file_path)
        except Exception as e:
            print(f"⚠️ Erreur lecture fichier {file_path}: {e}")
    return fens

def estimate_fen_distribution(root_dir):
    fen_to_files = defaultdict(set)
    total_files = 0

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if not (file.lower().endswith(".pgn") or file.lower().endswith(".zip")):
                continue
            total_files += 1
            path = os.path.join(subdir, file)
            fens = fens_in_file_or_zip(path)
            for fen in fens:
                fen_to_files[fen].add(file)

    counts = [len(v) for v in fen_to_files.values()]
    moyenne = sum(counts) / len(counts)
    print("\n📊 Résumé global")
    print(f"  • Fichiers analysés : {total_files}")
    print(f"  • FEN uniques       : {len(fen_to_files):,}")
    print(f"  • Moyenne           : {moyenne:.2f} fichiers par position")

if __name__ == "__main__":
    estimate_fen_distribution("C:\\home\\echecs\\pgn\\2015")
