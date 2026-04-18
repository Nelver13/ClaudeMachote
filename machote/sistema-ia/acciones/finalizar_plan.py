#!/usr/bin/env python3
"""
finalizar_plan.py
El dev ejecuta esto al completar TODO el plan.
Uso: python ./acciones/finalizar_plan.py [modulo] [version]

Ejemplo:
  python ./acciones/finalizar_plan.py facturacion v1
"""
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

def main():
    if len(sys.argv) < 3:
        print("Uso: python ./acciones/finalizar_plan.py [modulo] [version]")
        sys.exit(1)
    
    modulo, version = sys.argv[1], sys.argv[2]
    
    os.system(f'python "{SCRIPT_DIR}/avisar.py" "PLAN COMPLETO: {modulo}/{version} — revisa resultado" normal')
    
    print(f"\n✅ Plan {modulo}/{version} ejecutado completo")
    print("📋 Revisa todo el código/archivos generados")
    print("🔧 Si hay algo mal: dime qué arreglar (misma sesión)")
    print("🆗 Si todo OK: cerramos y empezamos nuevo plan\n")

if __name__ == '__main__':
    main()
