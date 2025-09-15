import psycopg2
import logging
from contextlib import contextmanager
from . import settings

logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(**settings.DB_CONFIG)
        #logger.info("Database connection established.")
        yield conn
    except psycopg2.OperationalError as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        raise
    finally:
        if conn:
            conn.close()
            #logger.info("Database connection closed.")