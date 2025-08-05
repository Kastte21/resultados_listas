import polars as pl
import logging
from io import StringIO
from tqdm import tqdm

from . import settings, utils
from .database import get_db_connection

logger = logging.getLogger(__name__)

def process_and_load_files():
    input_files = list(settings.INPUT_DATA_DIR.glob("*.csv"))
    logger.info(f"📂 Found {len(input_files)} CSV files in {settings.INPUT_DATA_DIR}.")

    total_inserted = 0
    for file_path in input_files:
        logger.info("-" * 60)
        logger.info(f"Processing file: {file_path.name}")
        try:
            inserted_count = _process_single_file(file_path)
            total_inserted += inserted_count
            logger.info(f"✅ Successfully inserted {inserted_count} new records from {file_path.name}.")
        except Exception as e:
            logger.error(f"❌ Failed to process file {file_path.name}. Error: {e}", exc_info=True)
    
    logger.info("=" * 60)
    logger.info(f"🏁 Process finished. Total new records inserted: {total_inserted}.")

def _process_single_file(file_path: settings.Path) -> int:
    df = _read_and_transform_csv(file_path)

    if "campana" in df.columns:
        valid_campana = df["campana"].drop_nulls()
        if valid_campana.len() > 0:
            name_campana = valid_campana.unique().item(0)
            logger.info(f"Campaign detected: {name_campana}")
        else:
            name_campana = "Unknown"
            logger.warning("The 'campana' column exists but is empty or contains only null values.")
    else:
        name_campana = "Unknown"
        logger.warning("The 'campana' column was not found in the file.")

    if df.is_empty():
        logger.warning("→ File is empty or invalid. Skipping.")
        return 0

    with get_db_connection() as conn:
        df_to_insert = _filter_existing_records(df, conn)
    
    if df_to_insert.is_empty():
        logger.info("↪ No new records to insert. All records already exist in the database.")
        return 0

    with get_db_connection() as conn:
        record_count = _load_data_with_copy(df_to_insert, conn)

    return record_count

def _read_and_transform_csv(file_path: settings.Path) -> pl.DataFrame:
    df = pl.read_csv(file_path, dtypes={col: pl.Utf8 for col in settings.INPUT_CSV_COLUMNS}, ignore_errors=True)

    if not all(col in df.columns for col in settings.REQUIRED_INPUT_COLUMNS):
        raise ValueError("Missing required columns in CSV.")
    
    logger.info(f"Read {df.height} rows from file.")

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

    logger.info(f"Found {len(existing_hashes)} duplicate records in the database. They will be ignored.")
    
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