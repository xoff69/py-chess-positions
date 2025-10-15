import os
import time
import chess.pgn
import io
import zipfile


def count_parts_and_fens_in_stream(stream, source_name):
    """Compte le nombre de parties et de positions (FEN) à partir d’un flux PGN."""
    games = 0
    positions = 0
    while True:
        game = chess.pgn.read_game(stream)
        if game is None:
            break
        games += 1
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            positions += 1
    return games, positions


def count_parts_and_fens_in_file(file_path):
    """Traite un fichier .pgn normal."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return count_parts_and_fens_in_stream(f, file_path)


def count_parts_and_fens_in_zip(zip_path):
    """Parcourt un .zip et compte les parties/positions dans chaque .pgn à l’intérieur."""
    total_games = 0
    total_positions = 0

    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            if not name.lower().endswith(".pgn"):
                continue
            with z.open(name) as f:
                # Décodage du flux binaire vers texte
                text_stream = io.TextIOWrapper(f, encoding="utf-8", errors="ignore")
                games, positions = count_parts_and_fens_in_stream(text_stream, name)
                total_games += games
                total_positions += positions
    return total_games, total_positions


def count_all(root_dir):
    """Parcourt récursivement un répertoire et compte les parties et positions dans tous les fichiers PGN et ZIP."""
    total_games = 0
    total_positions = 0
    all_files = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".pgn") or filename.lower().endswith(".zip"):
                all_files.append(os.path.join(dirpath, filename))

    for idx, file_path in enumerate(all_files, 1):
        try:
            if file_path.lower().endswith(".pgn"):
                games, positions = count_parts_and_fens_in_file(file_path)
            else:  # ZIP
                games, positions = count_parts_and_fens_in_zip(file_path)

            total_games += games
            total_positions += positions
            avg = positions / games if games > 0 else 0
            print(f"[{idx}/{len(all_files)}] {os.path.basename(file_path)}: "
                  f"{games} parties, {positions} positions (≈ {avg:.1f} pos/partie)")
        except Exception as e:
            print(f"⚠️ Erreur dans {file_path}: {e}")

    print("\n📊 Résumé global")
    print(f"  • Fichiers analysés : {len(all_files)}")
    print(f"  • Parties totales   : {total_games:,}")
    print(f"  • Positions totales : {total_positions:,}")
    avg_total = total_positions / total_games if total_games > 0 else 0
    print(f"  • Moyenne            : {avg_total:.1f} positions/partie")

    return total_games, total_positions


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage : python fencount.py <repertoire_pgn>")
        sys.exit(1)

    root = sys.argv[1]
    start_time = time.time()
    count_all(root)
    elapsed = time.time() - start_time
    minutes, seconds = divmod(elapsed, 60)
    print(f"  • Temps total       : {int(minutes)} min {seconds:.2f} s")
