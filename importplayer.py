import pandas as pd
from sqlalchemy import create_engine
import numpy as np

# --- CONFIGURATION ---
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5434/postgres")

# Définir les colonnes et les positions fixes (colspecs)
colspecs = [
    (0, 10), (10, 50), (50, 54), (54, 56), (56, 60), (60, 64),
    (64, 70), (70, 74), (74, 79), (79, 83), (83, 87), (87, 92),
    (92, 96), (96, 100), (100, 104), (104, 108), (108, 112), (112, 116), (116, 120)
]

names = [
    "fide_id", "name", "fed", "sex", "tit", "wtit", "otit", "foa",
    "srtng", "sgm", "sk", "rrtng", "rgm", "rk", "brtng", "bgm", "bk", "b_day", "flag"
]

# --- FONCTIONS UTILES ---
def clean_value(val, col=None):
    """Nettoyer les valeurs, convertir les nombres et gérer les NaN."""
    if isinstance(val, str):
        val = val.strip()
        if val == "" or val.upper() in ["NA", "NAN"]:
            return None
    if col in ["fide_id", "foa", "srtng", "sgm", "sk", "rrtng", "rgm", "rk", "brtng", "bgm", "bk", "b_day", "flag"]:
        try:
            return int(val)
        except (ValueError, TypeError):
            return None
    return val

# --- LECTURE DU FICHIER ---
df = pd.read_fwf(
    r"C:\developpement\chessvger\players_list_foa.txt",
    colspecs=colspecs,
    names=names,
    skiprows=1
)

# Nettoyage
for col in df.columns:
    df[col] = df[col].apply(lambda x: clean_value(x, col))

# Supprimer les doublons de fide_id
df = df.drop_duplicates(subset=['fide_id'])

# --- INSERTION DANS POSTGRESQL EN BATCH ---
# On convertit explicitement les colonnes int pour éviter les erreurs
int_cols = ["fide_id", "foa", "srtng", "sgm", "sk", "rrtng", "rgm", "rk", "brtng", "bgm", "bk", "b_day", "flag"]
for col in int_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')  # nullable int pour Postgres

# Inserer par batch
chunksize = 500
with engine.begin() as conn:  # gestion transaction automatique
    for start in range(0, len(df), chunksize):
        df.iloc[start:start+chunksize].to_sql(
            'player',
            conn,
            if_exists='append',
            index=False
        )

print("Import terminé, nombre de joueurs insérés :", len(df))
