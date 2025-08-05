# Sistema de Gestión de Resultados de Listas

## 📋 Descripción

Sistema modular para la gestión de resultados de listas de campañas, que permite cargar datos desde archivos CSV a PostgreSQL y exportar resultados filtrados por fecha.

## 🏗️ Estructura del Proyecto

```
CARGAR_DATA_POSTGRESQL/
├── main.py                    # 🎯 Script principal con menú interactivo
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py         # ⚙️ Configuración centralizada
│   ├── loaders/
│   │   ├── __init__.py
│   │   └── cargar_resultados.py  # 📤 Módulo de carga de datos
│   ├── extractors/
│   │   ├── __init__.py
│   │   └── descargar_resultados.py # 📥 Módulo de descarga de datos
│   └── utils/
│       ├── __init__.py
│       └── helpers.py        # 🛠️ Funciones de utilidad
├── data/
│   ├── input/                # 📁 Archivos CSV de entrada
│   ├── output/               # 📁 Archivos de salida
│   └── results/
│       └── descarga/         # 📁 Archivos de descarga
├── requirements.txt           # 📦 Dependencias
└── README.md                 # 📚 Documentación
```

## 🚀 Uso

### Ejecutar el sistema completo:
```bash
python main.py
```

### Ejecutar módulos individuales:
```bash
# Cargar datos desde CSV a PostgreSQL
python src/loaders/cargar_resultados.py

# Descargar datos desde PostgreSQL
python src/extractors/descargar_resultados.py
```

## 📊 Funcionalidades

### 1. Carga de Resultados (`src/loaders/cargar_resultados.py`)
- ✅ Procesa archivos CSV desde `data/input/`
- ✅ Valida estructura y contenido de archivos
- ✅ Detecta duplicados usando hashes MD5
- ✅ Inserta datos en PostgreSQL con transacciones
- ✅ Manejo de errores y rollback automático
- ✅ Progreso visual con tqdm
- ✅ Procesamiento en lotes (50,000 registros)

### 2. Descarga de Resultados (`src/extractors/descargar_resultados.py`)
- ✅ Exporta datos filtrados por día/mes
- ✅ Genera archivos en `data/results/descarga/`
- ✅ Formato de salida: pipe-separated values (|)
- ✅ Progreso visual con tqdm
- ✅ Validación de parámetros de entrada

### 3. Configuración (`src/core/config.py`)
- ✅ Variables de entorno de base de datos
- ✅ Configuración de columnas centralizada
- ✅ Rutas de directorios dinámicas
- ✅ Parámetros de procesamiento configurables

### 4. Utilidades (`src/utils/helpers.py`)
- ✅ Generación de hashes únicos para detección de duplicados
- ✅ Clasificación automática de teléfonos (TELEFONO/CELULAR/DESCONOCIDO)
- ✅ Validación de formatos de fecha
- ✅ Funciones auxiliares reutilizables

## 🎯 Menú Principal

```
============================================================
SISTEMA DE GESTIÓN DE RESULTADOS DE LISTAS
============================================================
1. Cargar resultados de listas
2. Descargar resultados de listas
3. Salir
============================================================
```

## 📁 Estructura de Datos

### Columnas Requeridas:
- `documento`: Número de documento
- `telefono`: Número de teléfono
- `start`: Fecha de inicio (formato: YYYY-MM-DD HH:MM:SS)

### Columnas Opcionales:
- `campana`: Nombre de la campaña
- `canal`: Canal de comunicación
- `cartera`: Tipo de cartera
- `estado`: Estado del registro
- `obs`: Observaciones (se genera automáticamente)

## 🔧 Configuración

### Variables de Entorno (.env):
```env
DB_NAME=nombre_base_datos
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=5432
```

### Parámetros de Procesamiento:
- `BATCH_SIZE`: 50,000 (registros por lote)
- `CHUNK_SIZE`: 10,000 (para archivos grandes)

## 📈 Características Técnicas

### Optimizaciones:
- ✅ Procesamiento en lotes para mejor rendimiento
- ✅ Detección de duplicados eficiente con hashes
- ✅ Transacciones para integridad de datos
- ✅ Manejo de memoria optimizado

### Validaciones:
- ✅ Estructura de archivos CSV
- ✅ Formato de fechas
- ✅ Columnas requeridas
- ✅ Conexión a base de datos

### Logging y Monitoreo:
- ✅ Progreso visual con barras de progreso
- ✅ Mensajes informativos detallados
- ✅ Manejo de errores robusto
- ✅ Estadísticas de procesamiento

## 📋 Requisitos

### Software:
- Python 3.7+
- PostgreSQL 10+
- pip (gestor de paquetes)

### Dependencias:
```
pandas>=1.3.0
psycopg2-binary>=2.9.0
python-dotenv>=0.19.0
tqdm>=4.62.0
```

### Instalación:
```bash
pip install -r requirements.txt
```

## 🔍 Ejemplos de Uso

### Cargar datos:
1. Coloca archivos CSV en `data/input/`
2. Ejecuta `python main.py`
3. Selecciona opción 1
4. Los datos se procesarán automáticamente

### Descargar datos:
1. Ejecuta `python main.py`
2. Selecciona opción 2
3. Ingresa día (ej: 31) y mes (ej: 07)
4. El archivo se generará en `data/results/descarga/`

## 🛠️ Mantenimiento

### Logs:
- Los logs se muestran en consola
- Información detallada de errores
- Estadísticas de procesamiento

### Backup:
- Se recomienda hacer backup antes de cargar datos
- Los datos existentes se verifican antes de insertar

### Monitoreo:
- Progreso visual en tiempo real
- Contadores de registros procesados
- Tiempo de procesamiento por archivo

## 📞 Soporte

Para reportar problemas o solicitar mejoras:
1. Revisa los logs de error
2. Verifica la configuración de la base de datos
3. Asegúrate de que los archivos CSV tengan el formato correcto

---

**Versión**: 1.0.0  
**Última actualización**: 2024  
**Autor**: Sistema de Gestión de Resultados 