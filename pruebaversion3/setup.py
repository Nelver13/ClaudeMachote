#!/usr/bin/env python3
# ARCHIVO: setup.py
# QUÉ HACE: Punto de entrada único — crea entorno, instala deps, inicia dashboard
# CÓMO ENCAJA: Se ejecuta UNA vez para configurar, y luego cada vez para abrir
# PARA EDITAR: nada
# DEPENDENCIAS: Python 3.10+

import os
import sys
import subprocess
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).parent
VENV_DIR = BASE_DIR / '.venv'
PORT     = 5000

# ─── Python del venv ──────────────────────────────────────────────────────────

def venv_python():
    if sys.platform == 'win32':
        return VENV_DIR / 'Scripts' / 'python.exe'
    return VENV_DIR / 'bin' / 'python'

def venv_pip():
    if sys.platform == 'win32':
        return VENV_DIR / 'Scripts' / 'pip.exe'
    return VENV_DIR / 'bin' / 'pip'

# ─── Pasos ────────────────────────────────────────────────────────────────────

def paso(n, texto):
    print(f'\n[{n}] {texto}')

def crear_venv():
    if VENV_DIR.exists():
        print('[1] Entorno virtual ya existe — OK')
        return
    paso(1, 'Creando entorno virtual...')
    subprocess.run([sys.executable, '-m', 'venv', str(VENV_DIR)], check=True)
    print('    Creado en .venv/')

def instalar_deps():
    req = BASE_DIR / 'claude' / 'dashboard' / 'requirements.txt'
    paso(2, 'Instalando dependencias...')
    subprocess.run(
        [str(venv_pip()), 'install', '-r', str(req), '-q'],
        check=True
    )
    print('    Flask instalado OK')

def init_db():
    db_path = BASE_DIR / 'claude' / 'datos.db'
    if db_path.exists():
        print('[3] Base de datos ya existe — OK')
        return
    paso(3, 'Inicializando base de datos SQLite...')
    subprocess.run(
        [str(venv_python()), str(BASE_DIR / 'claude' / 'acciones' / 'init_db.py')],
        cwd=str(BASE_DIR),
        check=True
    )

def dashboard_corriendo():
    try:
        urllib.request.urlopen(f'http://localhost:{PORT}', timeout=1)
        return True
    except Exception:
        return False

def iniciar_dashboard():
    if dashboard_corriendo():
        print(f'[4] Dashboard ya corriendo en http://localhost:{PORT}')
        return
    paso(4, 'Iniciando dashboard...')
    subprocess.Popen(
        [str(venv_python()), str(BASE_DIR / 'claude' / 'dashboard' / 'app.py')],
        cwd=str(BASE_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    import time
    for _ in range(8):
        time.sleep(0.8)
        if dashboard_corriendo():
            break
    if dashboard_corriendo():
        print(f'    Dashboard listo -> http://localhost:{PORT}')
    else:
        print('    ADVERTENCIA: dashboard no respondio — revisar manualmente')

def abrir_browser():
    paso(5, f'Abriendo dashboard en el browser...')
    subprocess.Popen(
        [sys.executable, '-m', 'webbrowser', f'http://localhost:{PORT}'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f'    http://localhost:{PORT}')

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print('=' * 50)
    print('  modo ia — setup')
    print('=' * 50)

    try:
        crear_venv()
        instalar_deps()
        init_db()
        iniciar_dashboard()
        abrir_browser()
    except subprocess.CalledProcessError as e:
        print(f'\nERROR en paso: {e}')
        sys.exit(1)

    print('\n' + '=' * 50)
    print('  Listo. Desde el dashboard:')
    print('  -> Tab "Inicio" -> boton "Abrir Editor"')
    print('=' * 50 + '\n')

if __name__ == '__main__':
    main()
