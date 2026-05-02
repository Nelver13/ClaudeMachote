#!/usr/bin/env python3
# ARCHIVO: finalizar_etapa.py
# QUE HACE: Cierre de etapa — actualiza ESTADO.md (raiz), RESUMEN.md y avisa
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

    # Actualizar ESTADO.md en raiz
    estado_path = CLAUDE_DIR.parent / 'ESTADO.md'
    if estado_path.exists():
        content = estado_path.read_text(encoding='utf-8')
        lines = content.strip().split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('[ESTADO_PLAN:'):
                new_lines.append('[ESTADO_PLAN: En revision]')
            elif line.startswith('[LAST_TASK:'):
                new_lines.append(f'[LAST_TASK: {etapa} — completada {ahora}]')
            elif line.startswith('[NEXT_TASK:'):
                new_lines.append('[NEXT_TASK: Esperando OK del arquitecto]')
            elif line.startswith('[CHECKPOINT:'):
                new_lines.append(f'[CHECKPOINT: {ahora[:10]}]')
            else:
                new_lines.append(line)
        estado_path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    else:
        # Fallback: crear ESTADO.md basico si no existe
        estado_path.write_text(
            f'[PROJ: Keyons]\n'
            f'[STACK: ver proyecto activo]\n'
            f'[PLAN: {ultimo_plan}]\n'
            f'[LAST_TASK: {etapa} — completada {ahora}]\n'
            f'[NEXT_TASK: Esperando OK del arquitecto]\n'
            f'[CHECKPOINT: {ahora[:10]}]\n'
            f'[DB: 0]\n'
            f'[DEBT: L]\n',
            encoding='utf-8'
        )
    print(f'[finalizar_etapa] ESTADO.md actualizado')

    # Actualizar RESUMEN.md
    resumen_path = CLAUDE_DIR / 'RESUMEN.md'
    resumen_path.write_text(
        f'# RESUMEN — Proyecto\n\n'
        f'Ultima etapa completada: {etapa} ({ahora})\n'
        f'Plan: {ultimo_plan}\n'
        f'Estado: esperando siguiente plan.\n',
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
