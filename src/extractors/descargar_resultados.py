import os
import psycopg2
from datetime import date, datetime
from dotenv import load_dotenv
from tqdm import tqdm

def descargar_resultados():
    inicio = datetime.now()
    dia = input("Ingresa el día (ej. 31): ")
    mes = input("Ingresa el mes (ej. 07): ")
    fecha_actual = date.today().strftime('%Y%m%d')

    # Obtener ruta desde el directorio raíz del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", "..")
    descarga_dir = os.path.join(project_root, "data", "results", "descarga")
    os.makedirs(descarga_dir, exist_ok=True)
    outpath = os.path.join(descarga_dir, f"r_{dia}_{mes}_{fecha_actual}.txt")
    column_order = ['documento', 'telefono', 'start', 'estado', 'obs', 'dia']

    print("=" * 60)
    print("EXPORTACIÓN DE RESULTADOS DE CAMPAÑAS")
    print("=" * 60)
    print(f"Inicio del proceso: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"→ Día solicitado: {dia} | Mes solicitado: {mes}")
    print("\nBuscando registros en base de datos...\n")

    try:
        load_dotenv()

        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        query = """
            SELECT documento, telefono, start, estado, obs, dia
            FROM resultados_listas
            WHERE campana IS NOT NULL
            AND documento IS NOT NULL
            AND telefono IS NOT NULL
            AND estado IS NOT NULL
            AND dia = %s
            AND mes = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, (dia, mes))
            rows = cursor.fetchall()

            with open(outpath, "w", encoding="utf-8") as f:
                f.write("|".join(column_order) + "\n")
                for row in tqdm(rows, desc="Procesando filas", unit="fila"):
                    row_clean = [str(value).replace("\n", " ").strip() for value in row]
                    f.write("|".join(row_clean) + "\n")

        fin = datetime.now()
        duracion = str(fin - inicio).split('.')[0]

        print("\nRESUMEN DE EXPORTACIÓN:")
        print(f" → Registros exportados: {len(rows)}")
        print(f" → Duración total: {duracion}")
        print(f" → Finalización: {fin.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR DURANTE LA EXPORTACIÓN")
        print("=" * 60)
        print(f"→ Detalle: {e}")
        print(f"→ Proceso abortado en: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

    finally:
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == "__main__":
    descargar_resultados()