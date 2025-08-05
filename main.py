#!/usr/bin/env python3
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.loaders.cargar_resultados import cargar_resultados
from src.extractors.descargar_resultados import descargar_resultados

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*60)
    print("SISTEMA DE GESTIÓN DE RESULTADOS DE LISTAS")
    print("="*60)
    print("1. Cargar resultados de listas")
    print("2. Descargar resultados de listas")
    print("3. Salir")
    print("="*60)

def main():
    """Función principal con menú interactivo"""
    print(f"Inicio del sistema: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSelecciona una opción (1-3): ").strip()
            
            if opcion == "1":
                print("\n🔄 Iniciando proceso de CARGA...")
                cargar_resultados()
                input("\nPresiona Enter para continuar...")
                
            elif opcion == "2":
                print("\n📥 Iniciando proceso de DESCARGA...")
                descargar_resultados()
                input("\nPresiona Enter para continuar...")
                
            elif opcion == "3":
                print("\n👋 ¡Hasta luego!")
                print(f"Finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                break
                
            else:
                print("\n❌ Opción inválida. Por favor selecciona 1, 2 o 3.")
                input("Presiona Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n Proceso interrumpido por el usuario.")
            print("👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main() 