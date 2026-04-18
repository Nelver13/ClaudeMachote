#!/usr/bin/env python3
"""
completar_tarea.py
Marca tarea completada y decide siguiente paso.
Uso: python ./acciones/completar_tarea.py [N] [total]

Ejemplos:
  python ./acciones/completar_tarea.py 3 5    # Tarea 3 de 5 lista, avisa y sigue
  python ./acciones/completar_tarea.py 5 5    # Ultima tarea, avisa PLAN COMPLETO
"""
import sys
import os
import re
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
ESTADO_FILE = ROOT_DIR.parent / "ESTADO.md"

def parse_estado():
    data = {}
    if ESTADO_FILE.exists():
        content = ESTADO_FILE.read_text(encoding='utf-8')
        for line in content.strip().split('\n'):
            if '[' in line and ']' in line:
                key = line.split('[')[1].split(']')[0]
                val = line.split(': ', 1)[1] if ': ' in line else ''
                data[key] = val.strip()
    return data

def update_estado(nueva_tarea, progreso):
    if not ESTADO_FILE.exists():
        return
    
    content = ESTADO_FILE.read_text(encoding='utf-8')
    lines = content.strip().split('\n')
    new_lines = []
    
    for line in lines:
        if line.startswith('[TAREA_ACTUAL:'):
            new_lines.append(f'[TAREA_ACTUAL: {nueva_tarea}]')
        elif line.startswith('[PROGRESO:'):
            new_lines.append(f'[PROGRESO: {progreso}]')
        elif line.startswith('[CHECKPOINT:'):
            new_lines.append(f'[CHECKPOINT: {datetime.now().strftime("%Y-%m-%d %H:%M")}]')
        else:
            new_lines.append(line)
    
    ESTADO_FILE.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')

def main():
    if len(sys.argv) < 3:
        print("Uso: python ./acciones/completar_tarea.py [N] [total]")
        print("Ejemplo: python ./acciones/completar_tarea.py 3 5")
        sys.exit(1)
    
    actual = int(sys.argv[1])
    total = int(sys.argv[2])
    estado = parse_estado()
    modulo = estado.get('MODULO', 'proyecto')
    
    # Calcular progreso
    progreso = int((actual / total) * 100)
    
    if actual >= total:
        # ULTIMA TAREA - PLAN COMPLETADO
        update_estado(actual, f"{progreso}%")
        os.system(f'python "{SCRIPT_DIR}/avisar.py" "🎉 PLAN COMPLETO: {modulo} — {actual}/{total} tareas" normal')
        print(f"\n🎉 PLAN COMPLETADO: {actual}/{total} tareas")
        print("📋 Revisar resultado y decidir siguiente plan\n")
    else:
        # TAREA COMPLETADA - SIGUIENTE
        siguiente = actual + 1
        update_estado(siguiente, f"{progreso}%")
        os.system(f'python "{SCRIPT_DIR}/avisar.py" "Tarea {actual}/{total} lista — siguiente: {siguiente}" normal')
        print(f"\n✅ Tarea {actual}/{total} completada")
        print(f"🚀 Siguiente: Tarea {siguiente}")
        print("📋 Actualiza ESTADO.md si hay cambios\n")

if __name__ == '__main__':
    main()
