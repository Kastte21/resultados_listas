# Sistema de Gestión de Resultados de Listas

## Descripción

Sistema modular para la gestión de resultados de listas de campañas, que permite cargar datos desde archivos CSV a PostgreSQL y exportar resultados filtrados por fecha.

## Estructura del Proyecto

```
├── app/
│   ├── data_loader.py       # Procesa y carga archivos CSV
│   ├── data_extractor.py    # Exporta resultados filtrados
│   ├── database.py          # Manejo de conexión PostgreSQL
│   ├── settings.py          # Configuraciones globales
│   └── utils.py             # Funciones auxiliares
├── data/
│   ├── input/               # CSVs de entrada
│   └── output/              # TXTs exportados
├── main.py                  # Menú CLI principal
└── .env                     # Configuración privada
```

## Uso

### Ejecutar el sistema completo:

```bash
python main.py
```

## Funcionalidades

- Procesamiento de archivos CSV con validaciones
- Clasificación automática de teléfonos (CELULAR / TELEFONO / DESCONOCIDO)
- Eliminación de duplicados usando hash MD5 por fila
- Exportación por día/mes en formato `.txt`
- Logging detallado para seguimiento en consola

## Menú Principal

```
============================================================
	SISTEMA DE GESTIÓN DE RESULTADOS (OPTIMIZADO)
============================================================
1. Cargar resultados de listas desde CSV
2. Descargar resultados de listas a TXT
3. Salir
============================================================
```

## Variables de Entorno (.env):

```env
DB_NAME=nombre_base_datos
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=5432
```

### Dependencias:

```
polars>=0.20.0
psycopg2-binary>=2.9.0
python-dotenv>=1.0.0
tqdm>=4.65.0
pandas>=2.0.0
```

### Instalación:

```bash
pip install -r requirements.txt
```

## Ejemplos de Uso

### Cargar datos:

1. Coloca archivos CSV en `data/input/`
2. Ejecuta `python main.py`
3. Selecciona opción 1
4. Los datos se procesarán automáticamente

### Descargar datos:

1. Ejecuta `python main.py`
2. Selecciona opción 2
3. Ingresa día (ej: 31) y mes (ej: 07)
4. El archivo se generará en `data/output/`

---
