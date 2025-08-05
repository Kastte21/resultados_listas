import re
import hashlib
from core.config import COLUMN_NAMES

def generar_hash_fila(row):
    """Genera hash único para una fila de datos"""
    campos_hash = [str(row.get(c, '')).strip() for c in COLUMN_NAMES]
    return hashlib.md5('|'.join(campos_hash).encode()).hexdigest()

def clasificar_telefono(telefono):
    """Clasifica el tipo de teléfono según su formato"""
    telefono_limpio = re.sub(r'\D', '', str(telefono))
    
    if len(telefono_limpio) == 7:
        return "TELEFONO"
    elif len(telefono_limpio) == 9 and telefono_limpio.startswith("9"):
        if telefono_limpio not in ["999999999", "900000000"]:
            return "CELULAR"
    return "DESCONOCIDO"

def validar_fecha_start(start_value):
    """Valida el formato de fecha en campo start"""
    start = str(start_value)
    return isinstance(start, str) and len(start) >= 10

def extraer_fecha_info(start_value):
    """Extrae día y mes de la fecha start"""
    start = str(start_value)
    if validar_fecha_start(start):
        return start[8:10], start[5:7]
    return None, None 