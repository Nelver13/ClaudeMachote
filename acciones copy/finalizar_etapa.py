#!/usr/bin/env python3
# ARCHIVO: finalizar_etapa.py
# QUE HACE: Cierre de etapa — actualiza estado.log, RESUMEN.md y avisa
# COMO ENCAJA: Claude lo llama al terminar todas las tareas de un plan
# DEPENDENCIAS: solo stdlib Python + avisar.py

import sys
import subprocess
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
CLAUDE_DIR  = SCRIPT_DIR.parent

def main():
    etapa = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'etapa sin nombre'
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M')

    # Contar planes completados
    planes_dir = CLAUDE_DIR / 'planes'
    planes = sorted(planes_dir.glob('plan_*.md')) if planes_dir.exists() else []
    ultimo_plan = planes[-1].name if planes else 'ninguno'

    # Actualizar estado.log
    estado_path = CLAUDE_DIR / 'estado.log'
    estado_path.write_text(
        f'[PROJ: ClaudeMachote]\n'
        f'[STACK: ver proyecto activo]\n'
        f'[PLAN: {ultimo_plan}]\n'
        f'[LAST_TASK: {etapa} — completada {ahora}]\n'
        f'[NEXT: abrir Claude con Opus para el proximo plan]\n'
        f'[DB: 0]\n'
        f'[DEBT: L]\n',
        encoding='utf-8'
    )
    print(f'[finalizar_etapa] estado.log actualizado')

    # Actualizar RESUMEN.md
    resumen_path = CLAUDE_DIR / 'RESUMEN.md'
    resumen_path.write_text(
        f'# RESUMEN — ClaudeMachote\n\n'
        f'Ultima etapa completada: {etapa} ({ahora})\n'
        f'Plan: {ultimo_plan}\n'
        f'Estado: abrir Claude con Opus para el proximo plan.\n',
        encoding='utf-8'
    )
    print(f'[finalizar_etapa] RESUMEN.md actualizado')

    # Avisar
    try:
        subprocess.run(
            ['python', str(SCRIPT_DIR / 'avisar.py'),
             f'Etapa "{etapa}" terminada — revisa para continuar', 'normal'],
            check=False
        )
    except Exception as e:
        print(f'[finalizar_etapa] Aviso fallido: {e}')

if __name__ == '__main__':
    main()
