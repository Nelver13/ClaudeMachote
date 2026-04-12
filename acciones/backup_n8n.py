#!/usr/bin/env python3
# ARCHIVO: backup_n8n.py
# QUÉ HACE: Exporta todos los flujos de n8n a JSON y los guarda en claude/backups/n8n/
# CÓMO ENCAJA: Claude lo llama al cerrar cada etapa
# PARA EDITAR: URL y API_KEY de n8n en acciones/credenciales.md
# DEPENDENCIAS: solo librería estándar Python

import sys
import os
import re
import json
import urllib.request
from datetime import datetime

# ─── Paths ───────────────────────────────────────────────────────────────────

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
CREDS_PATH   = os.path.join(SCRIPT_DIR, 'credenciales.md')
BACKUPS_BASE = os.path.join(SCRIPT_DIR, '..', 'backups', 'n8n')

# ─── Credenciales ────────────────────────────────────────────────────────────

def leer_n8n_creds():
    """Lee URL y API_KEY de la sección ## n8n en credenciales.md"""
    if not os.path.exists(CREDS_PATH):
        print('[backup_n8n] credenciales.md no encontrado')
        return None, None

    with open(CREDS_PATH, 'r', encoding='utf-8') as f:
        contenido = f.read()

    match = re.search(r'##\s*n8n(.+?)(?=\n##|\Z)', contenido, re.DOTALL | re.IGNORECASE)
    if not match:
        print('[backup_n8n] Sección ## n8n no encontrada en credenciales.md')
        return None, None

    seccion = match.group(1)
    url    = re.search(r'-\s*URL\s*:\s*(.+)',     seccion, re.IGNORECASE)
    apikey = re.search(r'-\s*API_KEY\s*:\s*(.+)', seccion, re.IGNORECASE)
    estado = re.search(r'-\s*Estado\s*:\s*(.+)',  seccion, re.IGNORECASE)

    if estado and 'inactiva' in estado.group(1).lower():
        print('[backup_n8n] n8n marcado como inactivo en credenciales.md — omitiendo backup')
        return None, None

    u = url.group(1).strip()    if url    else None
    k = apikey.group(1).strip() if apikey else None

    if not u or not k:
        print('[backup_n8n] URL o API_KEY vacíos en credenciales.md')
        return None, None

    return u, k

# ─── Backup ───────────────────────────────────────────────────────────────────

def hacer_backup(numero_etapa):
    n8n_url, api_key = leer_n8n_creds()
    if not n8n_url or not api_key:
        return

    fecha     = datetime.now().strftime('%Y-%m-%d')
    carpeta   = os.path.join(BACKUPS_BASE, f'etapa_{numero_etapa}_{fecha}')
    os.makedirs(carpeta, exist_ok=True)

    # Obtener lista de flujos
    req = urllib.request.Request(
        f'{n8n_url}/api/v1/workflows',
        headers={'X-N8N-API-KEY': api_key, 'Accept': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data   = json.loads(r.read())
            flujos = data.get('data', [])
    except Exception as e:
        print(f'[backup_n8n] Error al conectar con n8n: {e}')
        return

    if not flujos:
        print('[backup_n8n] No se encontraron flujos en n8n')
        return

    # Guardar cada flujo
    resumen = []
    for flujo in flujos:
        nombre   = re.sub(r'[^\w\-]', '_', flujo.get('name', 'sin_nombre'))
        archivo  = os.path.join(carpeta, f'{nombre}.json')
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(flujo, f, indent=2, ensure_ascii=False)
        resumen.append(f"- {flujo.get('name')} → {nombre}.json")
        print(f'[backup_n8n] Guardado: {nombre}.json')

    # Escribir resumen
    resumen_path = os.path.join(carpeta, 'resumen.md')
    with open(resumen_path, 'w', encoding='utf-8') as f:
        f.write(f'# Backup n8n — Etapa {numero_etapa}\n')
        f.write(f'**Fecha:** {fecha}\n')
        f.write(f'**Flujos guardados:** {len(flujos)}\n\n')
        f.write('\n'.join(resumen))

    print(f'[backup_n8n] Backup completo — {len(flujos)} flujos en {carpeta}')

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print('Uso: python backup_n8n.py [numero_etapa]')
        sys.exit(1)

    hacer_backup(sys.argv[1])

if __name__ == '__main__':
    main()
