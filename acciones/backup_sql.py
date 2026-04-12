#!/usr/bin/env python3
# ARCHIVO: backup_sql.py
# QUÉ HACE: Hace dump de PostgreSQL y lo guarda en claude/backups/sql/
# CÓMO ENCAJA: Claude lo llama al cerrar etapas en proyectos con DB
# PARA EDITAR: Credenciales de DB en .env del proyecto (lee DATABASE_URL)
# DEPENDENCIAS: pg_dump instalado, python-dotenv opcional

import sys
import os
import re
import subprocess
from datetime import datetime

# ─── Paths ───────────────────────────────────────────────────────────────────

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
BACKUPS_BASE = os.path.join(SCRIPT_DIR, '..', 'backups', 'sql')
ENV_PATH     = os.path.join(SCRIPT_DIR, '..', '..', '.env')  # raíz del proyecto

# ─── Leer DATABASE_URL del .env ───────────────────────────────────────────────

def leer_database_url():
    """Lee DATABASE_URL desde el .env del proyecto."""
    if not os.path.exists(ENV_PATH):
        print(f'[backup_sql] .env no encontrado en {ENV_PATH}')
        return None

    with open(ENV_PATH, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if linea.startswith('DATABASE_URL'):
                partes = linea.split('=', 1)
                if len(partes) == 2:
                    return partes[1].strip().strip('"').strip("'")

    print('[backup_sql] DATABASE_URL no encontrado en .env')
    return None

def parsear_url(url):
    """
    Parsea postgresql://usuario:password@host:port/nombre_db
    Retorna dict con los componentes.
    """
    match = re.match(
        r'postgres(?:ql)?://([^:]+):([^@]+)@([^:/]+):?(\d*)/(.+)',
        url
    )
    if not match:
        print(f'[backup_sql] No se pudo parsear DATABASE_URL: {url}')
        return None

    return {
        'user':     match.group(1),
        'password': match.group(2),
        'host':     match.group(3),
        'port':     match.group(4) or '5432',
        'db':       match.group(5),
    }

# ─── Backup ───────────────────────────────────────────────────────────────────

def hacer_backup(numero_etapa):
    db_url = leer_database_url()
    if not db_url:
        return

    creds = parsear_url(db_url)
    if not creds:
        return

    os.makedirs(BACKUPS_BASE, exist_ok=True)

    fecha   = datetime.now().strftime('%Y-%m-%d_%H%M')
    archivo = os.path.join(BACKUPS_BASE, f'etapa_{numero_etapa}_{fecha}_{creds["db"]}.sql')

    env = os.environ.copy()
    env['PGPASSWORD'] = creds['password']

    cmd = [
        'pg_dump',
        '-h', creds['host'],
        '-p', creds['port'],
        '-U', creds['user'],
        '-d', creds['db'],
        '-f', archivo,
        '--no-password',
    ]

    print(f'[backup_sql] Haciendo dump de {creds["db"]}...')

    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if result.returncode == 0:
            size = os.path.getsize(archivo) // 1024
            print(f'[backup_sql] Backup completo → {archivo} ({size} KB)')
        else:
            print(f'[backup_sql] Error en pg_dump: {result.stderr}')
    except FileNotFoundError:
        print('[backup_sql] pg_dump no encontrado — instalá PostgreSQL client tools')

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print('Uso: python backup_sql.py [numero_etapa]')
        sys.exit(1)

    hacer_backup(sys.argv[1])

if __name__ == '__main__':
    main()
