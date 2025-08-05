"""
Configuración centralizada para el sistema de gestión de resultados
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de base de datos
DB_CONFIG = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT")
}

# Configuración de columnas
COLUMN_NAMES = [
    'documento', 'telefono', 'campana', 'canal', 'cartera', 'idcliente', 'start',
    'subcartera', 'supervisor', 'anexo', 'causa', 'corta', 'disposition',
    'duration', 'estado', 'gestion', 'dia', 'mes', 'obs'
]

REQUIRED_COLUMNS = ['documento', 'telefono', 'start']

# Configuración de procesamiento
BATCH_SIZE = 50000
CHUNK_SIZE = 10000

# Rutas de directorios
def get_data_paths():
    """Obtiene las rutas de los directorios de datos desde el directorio raíz"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", "..")
    
    return {
        'input': os.path.join(project_root, "data", "input"),
        'output': os.path.join(project_root, "data", "output"),
        'results': os.path.join(project_root, "data", "results"),
        'descarga': os.path.join(project_root, "data", "results", "descarga")
    }