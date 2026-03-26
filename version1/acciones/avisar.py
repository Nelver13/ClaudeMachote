#!/usr/bin/env python3
# ARCHIVO: avisar.py
# QUÉ HACE: Aviso doble — reproduce MP3 + manda WhatsApp vía Callmebot
# CÓMO ENCAJA: Claude lo llama al terminar pasos, etapas o ante errores
# PARA EDITAR: Credenciales de Callmebot en claude/credenciales.md (sección ## Callmebot)
# DEPENDENCIAS: solo librería estándar Python

import sys
import os
import re
import subprocess
import urllib.request
import urllib.parse

# ─── Paths ───────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# credenciales.md vive junto al script (en acciones/ o en claude/acciones/)
POSIBLES_CREDS = [
    os.path.join(SCRIPT_DIR, 'credenciales.md'),
]

# ─── Sonido ──────────────────────────────────────────────────────────────────

def play_mp3(tipo):
    mp3 = os.path.join(SCRIPT_DIR, f'aviso_{tipo}.mp3')
    if not os.path.exists(mp3):
        print(f'[avisar] MP3 no encontrado: {mp3}')
        return
    # Reproduce en background sin abrir ventana
    subprocess.Popen(
        ['powershell', '-c',
         f'Add-Type -AssemblyName presentationCore; '
         f'$p = New-Object System.Windows.Media.MediaPlayer; '
         f'$p.Open([System.Uri]"{mp3}"); '
         f'$p.Play(); '
         f'Start-Sleep -s 6'],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

# ─── Credenciales ────────────────────────────────────────────────────────────

def leer_seccion_callmebot():
    """Extrae PHONE y API_KEY de la sección ## Callmebot en credenciales.md"""
    for ruta in POSIBLES_CREDS:
        if not os.path.exists(ruta):
            continue
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()

        # Buscar sección ## Callmebot
        match = re.search(r'##\s*Callmebot(.+?)(?=\n##|\Z)', contenido, re.DOTALL | re.IGNORECASE)
        if not match:
            return None, None

        seccion = match.group(1)

        phone   = re.search(r'-\s*PHONE\s*:\s*(.+)',   seccion, re.IGNORECASE)
        apikey  = re.search(r'-\s*API_KEY\s*:\s*(.+)', seccion, re.IGNORECASE)
        estado  = re.search(r'-\s*Estado\s*:\s*(.+)',  seccion, re.IGNORECASE)

        if estado and 'expirada' in estado.group(1).lower():
            print('[avisar] Callmebot: credencial expirada — solo sonido')
            return None, None

        p = phone.group(1).strip()  if phone  else None
        k = apikey.group(1).strip() if apikey else None
        return p, k

    return None, None

# ─── WhatsApp ─────────────────────────────────────────────────────────────────

EMOJI = {'suave': '💬', 'normal': '✅', 'urgente': '🚨'}

def send_whatsapp(mensaje, tipo):
    phone, apikey = leer_seccion_callmebot()
    if not phone or not apikey:
        print('[avisar] Callmebot: sin credenciales en credenciales.md — solo sonido')
        return

    texto  = f"{EMOJI.get(tipo, '🔔')} Claude: {mensaje}"
    params = urllib.parse.urlencode({'phone': phone, 'text': texto, 'apikey': apikey})
    url    = f'https://api.callmebot.com/whatsapp.php?{params}'

    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            print(f'[avisar] WhatsApp enviado — status {r.status}')
    except Exception as e:
        print(f'[avisar] WhatsApp falló: {e}')

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print('Uso: python avisar.py "mensaje" suave|normal|urgente')
        sys.exit(1)

    mensaje = sys.argv[1]
    tipo    = sys.argv[2].lower()

    if tipo not in ('suave', 'normal', 'urgente'):
        print(f'[avisar] Tipo inválido "{tipo}". Opciones: suave, normal, urgente')
        sys.exit(1)

    print(f'[avisar] {tipo.upper()} — {mensaje}')
    play_mp3(tipo)
    send_whatsapp(mensaje, tipo)

if __name__ == '__main__':
    main()
