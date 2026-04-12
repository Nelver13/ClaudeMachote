#!/usr/bin/env python3
"""
finalizar_discusion.py
Cierra discusion modo:arquitecto. 
Uso: python ./acciones/finalizar_discusion.py [modulo] [version]

Ejemplo:
  python ./acciones/finalizar_discusion.py facturacion v1
"""
import sys
import os
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent

def main():
    if len(sys.argv) < 3:
        print("Uso: python ./acciones/finalizar_discusion.py [modulo] [version]")
        print("Ejemplo: python ./acciones/finalizar_discusion.py facturacion v1")
        sys.exit(1)
    
    modulo, version = sys.argv[1], sys.argv[2]
    
    # Solo avisar que la discusion esta lista para revisar
    os.system(f'python "{SCRIPT_DIR}/avisar.py" "DISC: {modulo}/{version} lista — revisa y dime ok" normal')
    
    print(f"\n✅ Discusión {modulo}/{version} cerrada.")
    print("📋 Tú revisas el plan en discs/ o planes/")
    print("🚀 Cuando quieras empezar: dame el prompt para modo:dev\n")

if __name__ == '__main__':
    main()
