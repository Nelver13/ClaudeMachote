#!/usr/bin/env python3
# ARCHIVO: avisar.py
# QUÉ HACE: Aviso multi-canal — sonido + Windows + ntfy + webhook + checkpoint
# CÓMO ENCAJA: Cualquier IA lo llama al terminar pasos, etapas o ante errores
# PARA EDITAR: Credenciales en sistema-ia/acciones/credenciales.md
# DEPENDENCIAS: solo librería estándar Python

import sys
import os
import re
import subprocess
import urllib.request
import json
from datetime import datetime
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# logs quedan junto a acciones en sistema-ia/logs
SISTEMA_IA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
LOG_DIR = os.path.join(SISTEMA_IA_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'notificaciones.log')

POSIBLES_CREDS = [
    os.path.join(SCRIPT_DIR, 'credenciales.md'),
]

# ─── Log ─────────────────────────────────────────────────────────────────────

def log_event(msg):
    os.makedirs(LOG_DIR, exist_ok=True)
    stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{stamp}] {msg}'
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

# ─── Sonido ──────────────────────────────────────────────────────────────────

def play_mp3(tipo):
    mp3 = os.path.join(SCRIPT_DIR, f'aviso_{tipo}.mp3')
    if not os.path.exists(mp3):
        try:
            import winsound
            winsound.PlaySound('SystemNotification', winsound.SND_ALIAS | winsound.SND_ASYNC)
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            log_event('[avisar] Sonido fallback: SystemNotification')
            return
        except Exception as e:
            log_event(f'[avisar] No se pudo reproducir fallback de sonido: {e}')
            return
    try:
        subprocess.Popen(
            ['powershell', '-NoProfile', '-Command',
             f'Add-Type -AssemblyName presentationCore; '
             f'$p = New-Object System.Windows.Media.MediaPlayer; '
             f'$p.Open([System.Uri]"{mp3}"); '
             f'$p.Volume = 1.0; '
             f'$p.Play(); '
             f'Start-Sleep -s 6'],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        log_event(f'[avisar] MP3 reproducido: aviso_{tipo}.mp3')
    except Exception as e:
        log_event(f'[avisar] Error reproduciendo MP3: {e}')

# ─── Credenciales ────────────────────────────────────────────────────────────

def _limpiar_valor(v: str) -> str:
    if not v:
        return ''
    return v.strip().strip('"').strip("'")

def _es_placeholder(v: str) -> bool:
    t = (v or '').strip().lower()
    return (
        ('[tu ' in t)
        or ('[valor]' in t)
        or (t == '')
        or ('reemplazar' in t)
        or (t.startswith('[') and t.endswith(']'))
    )

def _leer_seccion(nombre: str):
    for ruta in POSIBLES_CREDS:
        if not os.path.exists(ruta):
            continue
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        match = re.search(rf'##\s*{re.escape(nombre)}\s*(.+?)(?=\n##|\Z)', contenido, re.DOTALL | re.IGNORECASE)
        if not match:
            continue
        seccion = match.group(1)
        estado = re.search(r'-\s*Estado\s*:\s*(.+)', seccion, re.IGNORECASE)
        if estado and 'expirada' in estado.group(1).lower():
            return None
        return seccion
    return None

def send_ntfy(mensaje, tipo):
    seccion = _leer_seccion('ntfy')
    if not seccion:
        return False
    url = re.search(r'-\s*URL\s*:\s*(.+)', seccion, re.IGNORECASE)
    token = re.search(r'-\s*TOKEN\s*:\s*(.+)', seccion, re.IGNORECASE)
    u = _limpiar_valor(url.group(1)) if url else ''
    t = _limpiar_valor(token.group(1)) if token else ''
    if _es_placeholder(u) or not u:
        log_event('[avisar] ntfy: URL invalida o placeholder')
        return False
    try:
        headers = {
            'Title': f'Claude {tipo}',
            'Priority': '5' if tipo == 'urgente' else '3',
            'Tags': 'robot,computer',
        }
        if t and not _es_placeholder(t):
            headers['Authorization'] = f'Bearer {t}'
        data = mensaje.encode('utf-8')
        req = urllib.request.Request(u, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode('utf-8', errors='ignore').strip()
            if r.status == 200:
                log_event(f'[avisar] ntfy enviado — status {r.status} body="{body[:100]}"')
                return True
            log_event(f'[avisar] ntfy error — status {r.status} body="{body[:120]}"')
    except Exception as e:
        log_event(f'[avisar] ntfy fallo: {e}')
    return False

def send_webhook(mensaje, tipo):
    seccion = _leer_seccion('Webhook')
    if not seccion:
        return False
    url = re.search(r'-\s*URL\s*:\s*(.+)', seccion, re.IGNORECASE)
    u = _limpiar_valor(url.group(1)) if url else ''
    if _es_placeholder(u) or not u:
        log_event('[avisar] Webhook: URL invalida o placeholder')
        return False
    payload = {'content': f'[{tipo.upper()}] Claude: {mensaje}'}
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            u, data=data, method='POST',
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'ClaudeMachote/avisar.py',
            }
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode('utf-8', errors='ignore').strip()
            if 200 <= r.status < 300:
                log_event(f'[avisar] Webhook enviado — status {r.status} body="{body[:100]}"')
                return True
            log_event(f'[avisar] Webhook error — status {r.status} body="{body[:120]}"')
    except Exception as e:
        log_event(f'[avisar] Webhook fallo: {e}')
    return False

# ─── Windows popup ───────────────────────────────────────────────────────────

EMOJI = {'suave': '💬', 'normal': '✅', 'urgente': '🚨'}

def send_windows_notification(mensaje, tipo):
    safe_msg_ps = mensaje.replace("'", "''")
    titulo = f'Claude ({tipo.upper()})'
    popup = (
        "$wshell = New-Object -ComObject WScript.Shell;"
        f"$null = $wshell.Popup('{safe_msg_ps}', 0, '{titulo}', 0x40);"
    )
    try:
        subprocess.Popen(
            ['powershell', '-NoProfile', '-Command', popup],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        log_event('[avisar] Popup Windows enviado — espera click')
    except Exception as e:
        log_event(f'[avisar] Popup Windows fallo: {e}')

# ─── Checkpoint ──────────────────────────────────────────────────────────────

def _encontrar_estado() -> Path | None:
    """Sube hasta 6 niveles buscando el primer dir con ESTADO.md."""
    actual = Path(SCRIPT_DIR).resolve()
    for _ in range(6):
        cand = actual / 'ESTADO.md'
        if cand.exists():
            return cand
        if actual.parent == actual:
            break
        actual = actual.parent
    return None

def guardar_checkpoint(mensaje: str, tipo: str):
    """Actualiza ESTADO.md con checkpoint + último aviso antes de notificar."""
    try:
        estado_file = _encontrar_estado()
        if not estado_file:
            log_event('[avisar] ESTADO.md no encontrado — checkpoint omitido')
            return

        contenido = estado_file.read_text(encoding='utf-8')
        stamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        lineas = []
        found_checkpoint = False
        found_last = False

        for linea in contenido.splitlines():
            if linea.strip().startswith('[CHECKPOINT:'):
                lineas.append(f'[CHECKPOINT: {stamp}]')
                found_checkpoint = True
            elif linea.strip().startswith('[LAST_AVISO:'):
                lineas.append(f'[LAST_AVISO: {tipo.upper()} — {mensaje}]')
                found_last = True
            else:
                lineas.append(linea)

        if not found_checkpoint:
            lineas.append(f'[CHECKPOINT: {stamp}]')
        if not found_last:
            lineas.append(f'[LAST_AVISO: {tipo.upper()} — {mensaje}]')

        estado_file.write_text('\n'.join(lineas) + '\n', encoding='utf-8')
        log_event(f'[avisar] Checkpoint guardado — {stamp}')
    except Exception as e:
        log_event(f'[avisar] Checkpoint falló: {e}')


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) >= 2 and sys.argv[1] == '--test':
        mensaje = 'Prueba de notificaciones'
        tipo = 'normal'
        log_event('[avisar] Ejecutando prueba completa')
        guardar_checkpoint(mensaje, tipo)
        play_mp3(tipo)
        send_windows_notification(mensaje, tipo)
        send_webhook(mensaje, tipo)
        send_ntfy(mensaje, tipo)
        return

    if len(sys.argv) < 3:
        print('Uso: python avisar.py "mensaje" suave|normal|urgente')
        print('     python avisar.py --test')
        sys.exit(1)

    mensaje = sys.argv[1]
    tipo    = sys.argv[2].lower()

    if tipo not in ('suave', 'normal', 'urgente'):
        print(f'[avisar] Tipo inválido "{tipo}". Opciones: suave, normal, urgente')
        sys.exit(1)

    log_event(f'[avisar] {tipo.upper()} — {mensaje}')
    guardar_checkpoint(mensaje, tipo)
    play_mp3(tipo)
    send_windows_notification(mensaje, tipo)
    send_webhook(mensaje, tipo)
    send_ntfy(mensaje, tipo)

if __name__ == '__main__':
    main()
