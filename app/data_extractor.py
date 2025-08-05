import polars as pl
import logging
from datetime import date

from . import settings
from .database import get_db_connection

logger = logging.getLogger(__name__)

def export_results(day: str, month: str):
    logger.info(f"Starting export for day: {day}, month: {month}")

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
            logger.warning("No records found for the specified day and month. No file will be created.")
            return

        output_filename = f"r_{day}_{month}_{date.today().strftime('%Y%m%d')}.txt"
        output_path = settings.OUTPUT_DATA_DIR / output_filename
        
        df.write_csv(output_path, separator="|")
        
        logger.info(f"✅ Export successful. {df.height} records saved to {output_path}")

    except Exception as e:
        logger.error(f"❌ An error occurred during data export: {e}", exc_info=True)