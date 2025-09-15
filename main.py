import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

try:
    from app import data_loader, data_extractor
except ImportError:
    logging.error("\u274C No se pudieron importar los módulos de la aplicación. Verifica que el directorio 'app' sea correcto.")
    exit(1)

def show_menu():
    print("\n" + "="*60)
    print("      SISTEMA DE RESULTADOS LISTAS UCM")
    print("="*60)
    print(" 1. Cargar resultados de listas desde CSV")
    print(" 2. Descargar resultados de listas a TXT")
    print(" 3. Salir")
    print("="*60)

def main():
    logging.info(f"Inicio del sistema: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    while True:
        show_menu()
        
        try:
            option = input("\nSelecciona una opción (1-3): ").strip()
            
            if option == "1":
                logging.info("\n\U0001F504 Iniciando proceso de CARGA...")
                data_loader.process_and_load_files()
                input("\nProceso de carga finalizado. Presiona Enter para continuar...")
                
            elif option == "2":
                logging.info("\n\U0001F4E5 Iniciando proceso de DESCARGA...")
                day = input("  → Ingresa el día (ej. 31): ")
                month = input("  → Ingresa el mes (ej. 07): ")
                if day and month:
                    data_extractor.export_results(day=day, month=month)
                else:
                    logging.warning("Día y mes son requeridos. Operación cancelada.")
                input("\nProceso de descarga finalizado. Presiona Enter para continuar...")
                
            elif option == "3":
                print("\n\U0001F44B ¡Hasta luego!")
                break
                
            else:
                logging.warning("\n\u274C Opción inválida. Por favor selecciona 1, 2 o 3.")
                input("Presiona Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n Proceso interrumpido por el usuario.")
            break
        except Exception as e:
            logging.error(f"\n\u274C Error inesperado en el menú principal: {e}", exc_info=True)
            input("Presiona Enter para continuar...")

    logging.info(f"Finalización del sistema: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()