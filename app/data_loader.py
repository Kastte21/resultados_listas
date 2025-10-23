#app/data_loader.py
import polars as pl
import logging
from io import StringIO
import pandas as pd
import hashlib

from . import settings, utils
from .database import get_db_connection

logger = logging.getLogger(__name__)

def process_and_load_files():
    input_files = list(settings.INPUT_DATA_DIR.glob("*.csv"))
    logger.info(f"\U0001F4C1 Se encontraron {len(input_files)} archivos CSV en {settings.INPUT_DATA_DIR}.")

    total_inserted = 0
    for file_path in input_files:
        logger.info("=" * 60)
        logger.info(f"Procesando archivo: {file_path.name}")
        try:
            inserted_count = _process_single_file(file_path)
            total_inserted += inserted_count
            logger.info(f"\u2705 Se insertaron correctamente {inserted_count} nuevos registros desde {file_path.name}.")
        except Exception as e:
            logger.warning(f"\u26A0\uFE0F Error con Polars en {file_path.name}. Reintentando con Pandas. Error: {e}")
            try:
                inserted_count = _process_file_with_pandas(file_path)
                total_inserted += inserted_count
                logger.info(f"\u2705 Se insertaron correctamente {inserted_count} registros desde {file_path.name} usando Pandas.")
            except Exception as e2:
                logger.error(f"\u274C Error al procesar el archivo {file_path.name} incluso con Pandas. Error: {e2}", exc_info=True)

    logger.info("=" * 60)
    logger.info(f"\U0001F4C4 Proceso finalizado. Total de nuevos registros insertados: {total_inserted}.")

def _process_single_file(file_path: settings.Path) -> int:
    df = _read_and_transform_csv(file_path)

    if "campana" in df.columns:
        valid_campana = df["campana"].drop_nulls()
        if valid_campana.len() > 0:
            name_campana = valid_campana.unique().item(0)
            logger.info(f"Campaña detectada: {name_campana}")
        else:
            name_campana = "Unknown"
            logger.warning("\u26A0\uFE0F La columna 'campana' existe pero está vacía o contiene solo valores nulos.")
    else:
        name_campana = "Unknown"
        logger.warning("\u26A0\uFE0F No se encontró la columna 'campana' en el archivo.")

    if df.is_empty():
        logger.warning("\u26A0\uFE0F El archivo está vacío o es inválido. Se omitirá.")
        return 0

    with get_db_connection() as conn:
        df_to_insert = _filter_existing_records(df, conn)
    
    if df_to_insert.is_empty():
        logger.info("↪ No hay nuevos registros para insertar. Todos ya existen en la base de datos.")
        return 0

    with get_db_connection() as conn:
        record_count = _load_data_with_copy(df_to_insert, conn)
    
    return record_count

def _read_and_transform_csv(file_path: settings.Path) -> pl.DataFrame:
    df = pl.read_csv(file_path, dtypes={col: pl.Utf8 for col in settings.INPUT_CSV_COLUMNS}, ignore_errors=True)

    if not all(col in df.columns for col in settings.REQUIRED_INPUT_COLUMNS):
        raise ValueError("Faltan columnas requeridas en el archivo CSV.")
    
    logger.info(f"Se leyeron {df.height} filas desde el archivo.")

    df = df.with_columns(
        pl.col("start").str.slice(8, 2).alias("dia"),
        pl.col("start").str.slice(5, 2).alias("mes"),
        
        utils.classify_phone_type(pl.col("telefono")).alias("obs"),
    ).with_columns(
        utils.generate_row_hash(df, settings.INPUT_CSV_COLUMNS).alias("hash_fila")
    )
    return df

def _filter_existing_records(df: pl.DataFrame, conn) -> pl.DataFrame:
    hashes_in_df = df.get_column("hash_fila").to_list()
    
    query = f"SELECT hash_fila FROM {settings.TABLE_NAME} WHERE hash_fila = ANY(%s)"
    with conn.cursor() as cursor:
        cursor.execute(query, (hashes_in_df,))
        existing_hashes = {row[0] for row in cursor.fetchall()}

    logger.info(f"Se encontraron {len(existing_hashes)} registros duplicados en la base de datos. Serán ignorados.")
    
    return df.filter(~pl.col("hash_fila").is_in(existing_hashes))

def _load_data_with_copy(df: pl.DataFrame, conn) -> int:
    s_buf = StringIO()
    
    df.select(settings.FINAL_TABLE_COLUMNS).write_csv(s_buf)
    s_buf.seek(0)
    
    with conn.cursor() as cursor:
        copy_sql = f"COPY {settings.TABLE_NAME} ({','.join(settings.FINAL_TABLE_COLUMNS)}) FROM STDIN WITH (FORMAT CSV)"
        cursor.copy_expert(sql=copy_sql, file=s_buf)
        conn.commit()
        return cursor.rowcount
    
def _process_file_with_pandas(file_path: settings.Path) -> int:
    df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")

    if not all(col in df.columns for col in settings.REQUIRED_INPUT_COLUMNS):
        raise ValueError("Faltan columnas requeridas en el archivo CSV.")

    logger.info(f"\U0001F4C4 [Pandas] Se leyeron {len(df)} filas desde el archivo.")

    df["dia"] = df["start"].astype(str).str[8:10]
    df["mes"] = df["start"].astype(str).str[5:7]
    df["obs"] = df["telefono"].apply(lambda x: "CELULAR" if str(x).startswith("9") and len(str(x)) == 9 else "TELEFONO")
    df["hash_fila"] = df[settings.INPUT_CSV_COLUMNS].fillna("").astype(str).agg('|'.join, axis=1).apply(
        lambda x: hashlib.md5(x.encode()).hexdigest()
    )

    with get_db_connection() as conn:
        hashes = df["hash_fila"].tolist()
        query = f"SELECT hash_fila FROM {settings.TABLE_NAME} WHERE hash_fila = ANY(%s)"
        with conn.cursor() as cursor:
            cursor.execute(query, (hashes,))
            existing = {row[0] for row in cursor.fetchall()}
        df_to_insert = df[~df["hash_fila"].isin(existing)]

    if df_to_insert.empty:
        logger.info("↪ [Pandas] No hay nuevos registros para insertar.")
        return 0

    s_buf = StringIO()
    df_to_insert[settings.FINAL_TABLE_COLUMNS].to_csv(s_buf, index=False)
    s_buf.seek(0)

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            copy_sql = f"COPY {settings.TABLE_NAME} ({','.join(settings.FINAL_TABLE_COLUMNS)}) FROM STDIN WITH (FORMAT CSV)"
            cursor.copy_expert(sql=copy_sql, file=s_buf)
            conn.commit()
            return cursor.rowcount
