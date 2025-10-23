#app/utils.py
import polars as pl
import hashlib

def classify_phone_type(series: pl.Series) -> pl.Series:
    phone_str = series.fill_null("").cast(pl.Utf8).str.replace_all(r"\D", "")

    return (
        pl.when(phone_str.str.len_chars() == 7)
        .then(pl.lit("TELEFONO"))
        .when(
            (phone_str.str.len_chars() == 9) & (phone_str.str.starts_with("9")) &
            (~phone_str.is_in(["999999999", "900000000"]))
        )
        .then(pl.lit("CELULAR"))
        .otherwise(pl.lit("DESCONOCIDO"))
    )

def generate_row_hash(df: pl.DataFrame, columns_to_hash: list) -> pl.Series:
    hash_source = pl.concat_str(
        [pl.col(c).cast(pl.Utf8).fill_null("").str.strip_chars() for c in columns_to_hash],
        separator='|'
    )
    return hash_source.map_elements(lambda x: hashlib.md5(x.encode()).hexdigest(), return_dtype=pl.Utf8)
    