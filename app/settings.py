import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT")
}

TABLE_NAME = "resultados_listas"

INPUT_CSV_COLUMNS = [
    'documento', 'telefono', 'campana', 'canal', 'cartera', 'idcliente', 'start',
    'subcartera', 'supervisor', 'anexo', 'causa', 'corta', 'disposition',
    'duration', 'estado', 'gestion'
]

REQUIRED_INPUT_COLUMNS = ['documento', 'telefono', 'start']

FINAL_TABLE_COLUMNS = [
    'documento', 'telefono', 'campana', 'canal', 'cartera', 'idcliente', 'start',
    'subcartera', 'supervisor', 'anexo', 'causa', 'corta', 'disposition',
    'duration', 'estado', 'gestion', 'dia', 'mes', 'obs', 'hash_fila'
]

BATCH_SIZE = 100_000

INPUT_DATA_DIR = BASE_DIR / "data" / "input"
OUTPUT_DATA_DIR = BASE_DIR / "data" / "output"