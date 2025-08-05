import polars as pl

def pl_info(df: pl.DataFrame):
    print("DataFrame Info")
    print("━━━━━━━━━━━━━━━━━━")
    print(f"Shape: {df.shape[0]} filas x {df.shape[1]} columns\n")

    print("Columnas:")
    for name, dtype in zip(df.columns, df.dtypes):
        col = df[name]
        nulls = col.null_count()
        unique_vals = col.n_unique()
        print(f"  └─ {name:<20} Tipo: {str(dtype):<10} Nulos: {nulls:<5} Únicos: {unique_vals}")

def summ_stats(df: pl.DataFrame):
    numerics = [col for col, dtype in zip(df.columns, df.dtypes) if dtype in [pl.Int64, pl.Float64]]
    summ = df.select(numerics).describe()
    print("Estadísticas resumidas:")
    print(summ)
