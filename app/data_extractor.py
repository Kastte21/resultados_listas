#app/data_extractor.py
import polars as pl
import logging
from datetime import date

from . import settings
from .database import get_db_connection

logger = logging.getLogger(__name__)

def export_results(day: str, month: str):
    logger.info(f" Iniciando exportación para el día:  {day}, mes: {month}")

    query = f"""
        SELECT documento, telefono, start, estado, obs, dia
        FROM {settings.TABLE_NAME}
        WHERE dia = %s AND mes = %s
        AND campana IS NOT NULL
        AND documento IS NOT NULL
        AND telefono IS NOT NULL
        AND estado IS NOT NULL
    """
    
    try:
        with get_db_connection() as conn:
            df = pl.read_database(
                query=query,
                connection=conn,
                execute_options={"parameters": (day, month)}
            )
        
        if df.is_empty():
            logger.warning("\u26A0\uFE0F No se encontraron registros para el día y mes especificados. No se creará ningún archivo.")
            return

        output_filename = f"r_{day}_{month}_{date.today().strftime('%Y%m%d')}.txt"
        output_path = settings.OUTPUT_DATA_DIR / output_filename
        
        df.write_csv(output_path, separator="|")
        
        logger.info(f"\u2705 Exportación exitosa. Se guardaron {df.height} registros en {output_path}.")

    except Exception as e:
        logger.error(f"\u274C Ocurrió un error durante la exportación de datos: {e}", exc_info=True)