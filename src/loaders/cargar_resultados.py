import os
import re
import hashlib
import pandas as pd
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from tqdm import tqdm

column_names = [
    'documento', 'telefono', 'campana', 'canal', 'cartera', 'idcliente', 'start',
    'subcartera', 'supervisor', 'anexo', 'causa', 'corta', 'disposition',
    'duration', 'estado', 'gestion', 'dia', 'mes', 'obs'
]

# Función para generar hash único
def generar_hash_fila(row):
    campos_hash = [str(row.get(c, '')).strip() for c in column_names]
    return hashlib.md5('|'.join(campos_hash).encode()).hexdigest()

def cargar_resultados():
    print("=" * 60)
    print("CARGA DE RESULTADOS LISTAS")
    print("=" * 60)
    print(f"Inicio del proceso: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Obtener ruta desde el directorio raíz del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", "..")
    path = os.path.join(project_root, "data", "input")
    
    files_csv = [f for f in os.listdir(path) if f.endswith('.csv')]
    print(f"Directorio de entrada: {path}")
    print(f"📂 Archivos CSV encontrados: {len(files_csv)}\n")

    load_dotenv()
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = connection.cursor()

    total_insertados = 0
    archivos_procesados = 0

    try:
        for file in files_csv:
            archivo_inicio = datetime.now()
            file_path = os.path.join(path, file)
            print("-" * 60)
            print(f"Archivo: {file}")
            df = pd.read_csv(file_path, low_memory=False)
            print(f"Filas en archivo: {len(df)}")

            if df.empty:
                print("→ Archivo vacío. Se omite.\n")
                continue

            required = ['documento', 'telefono', 'start']
            if not set(required).issubset(df.columns):
                print("→ Error: faltan columnas requeridas. Se omite.\n")
                continue

            start = str(df.iloc[0].get("start", ""))
            if not isinstance(start, str) or len(start) < 10:
                print("→ Error: valor inválido en campo 'start'. Se omite.\n")
                continue

            dia = start[8:10]
            mes = start[5:7]
            campana = str(df.iloc[0].get("campana", "")).strip()

            cursor.execute("""
                SELECT COUNT(*) FROM resultados_listas
                WHERE dia = %s AND mes = %s AND campana = %s
            """, (dia, mes, campana))
            registros_previos = cursor.fetchone()[0]
            filas_csv = len(df)

            print(f"Campaña detectada: '{campana}' | Día: {dia} / Mes: {mes}")
            print(f"Registros ya existentes en BD: {registros_previos}")

            if registros_previos > 0 and registros_previos == filas_csv:
                print("↪ Se omite la carga: coincidencia exacta de registros.\n")
                continue

            print("Verificando duplicados...")
            df['dia'] = df['start'].str[8:10]
            df['mes'] = df['start'].str[5:7]

            obs_list = []
            hash_list = []
            for _, row in df.iterrows():
                telefono = re.sub(r'\D', '', str(row.get("telefono", "")))
                if len(telefono) == 7:
                    obs = "TELEFONO"
                elif len(telefono) == 9 and telefono.startswith("9") and telefono not in ["999999999", "900000000"]:
                    obs = "CELULAR"
                else:
                    obs = "DESCONOCIDO"
                obs_list.append(obs)
                hash_list.append(generar_hash_fila(row))

            df['obs'] = obs_list
            df['hash_fila'] = hash_list

            hashes_csv = tuple(set(df['hash_fila']))
            cursor.execute("SELECT hash_fila FROM resultados_listas WHERE hash_fila IN %s", (hashes_csv,))
            hashes_existentes = set([r[0] for r in cursor.fetchall()])
            print(f"→ Duplicados encontrados en BD: {len(hashes_existentes)}")

            column_names_with_hash = column_names + ['hash_fila']
            query = f"""
                INSERT INTO resultados_listas ({', '.join(column_names_with_hash)})
                VALUES ({', '.join(['%s'] * len(column_names_with_hash))})
            """
            batch_values = []
            rows_to_insert = 0

            for _, row in tqdm(df.iterrows(), total=len(df), desc="→ Filtrado e inserción", leave=False):
                hash_fila = row['hash_fila']
                if hash_fila in hashes_existentes:
                    continue

                values = []
                for col in column_names:
                    value = row.get(col, None)
                    values.append(None if pd.isna(value) else str(value).strip())
                values.append(hash_fila)

                batch_values.append(values)
                rows_to_insert += 1

                if len(batch_values) == 50000:
                    cursor.executemany(query, batch_values)
                    connection.commit()
                    batch_values = []

            if batch_values:
                cursor.executemany(query, batch_values)
                connection.commit()

            print(f"→ Registros insertados: {rows_to_insert}")
            archivo_fin = datetime.now()
            duracion = archivo_fin - archivo_inicio
            print(f"Tiempo de procesamiento: {duracion}\n")

            total_insertados += rows_to_insert
            archivos_procesados += 1

    except Exception as e:
        print("Error durante el proceso:")
        print(f"→ {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

        print("=" * 60)
        print("RESUMEN FINAL")
        print("=" * 60)
        print(f"Archivos procesados: {archivos_procesados}")
        print(f"Total de registros nuevos insertados: {total_insertados}")
        print(f"Finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

if __name__ == "__main__":
    cargar_resultados()