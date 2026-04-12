#!/usr/bin/env python3
"""
avisar.py
Uso: python ./claude/acciones/avisar.py "mensaje" [suave|normal|urgente]

Cuándo usa esto la IA:
  normal  → tarea lista / plan listo
  urgente → hay algo que el humano DEBE revisar antes de continuar
  suave   → info menor (raro)
"""
import sys, os, json, datetime, subprocess, urllib.request

DIR = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(DIR, "..", "logs", "notificaciones.log")
CREDS = os.path.join(DIR, "credenciales.md")
SOUNDS = {
    "suave":   os.path.join(DIR, "aviso_suave.mp3"),
    "normal":  os.path.join(DIR, "aviso_normal.mp3"),
    "urgente": os.path.join(DIR, "aviso_urgente.mp3"),
}

def cred(clave):
    try:
        for l in open(CREDS, encoding="utf-8"):
            if clave in l and "TU_" not in l:
                p = l.strip().split(": ", 1)
                if len(p) == 2: return p[1].strip()
    except: pass
    return None

def sonido(tipo):
    p = SOUNDS.get(tipo, SOUNDS["normal"])
    if not os.path.exists(p): return
    try:
        if sys.platform == "win32":
            import winsound; winsound.PlaySound(p, winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif sys.platform == "darwin":
            subprocess.Popen(["afplay", p])
        else:
            subprocess.Popen(["mpg123", "-q", p])
    except: pass

def popup(msg, tipo):
    t = {"suave":"Info","normal":"Tarea lista","urgente":"REVISAR"}.get(tipo,"Aviso")
    try:
        if sys.platform == "win32":
            import ctypes; ctypes.windll.user32.MessageBoxW(0, msg, t, 0x40)
        elif sys.platform == "darwin":
            subprocess.run(["osascript","-e",f'display dialog "{msg}" with title "{t}" buttons {{"OK"}} default button "OK"'])
        else:
            subprocess.run(["zenity","--info",f"--title={t}",f"--text={msg}"], capture_output=True)
    except: pass

def discord(msg, tipo):
    url = cred("URL: https://discord.com")
    if not url: return
    e = {"suave":"🔔","normal":"✅","urgente":"🚨"}.get(tipo,"📢")
    try:
        r = urllib.request.Request(url, json.dumps({"content":f"{e} {msg}"}).encode(),
                                   {"Content-Type":"application/json"})
        urllib.request.urlopen(r, timeout=5)
    except: pass

def ntfy(msg, tipo):
    url = cred("URL: https://ntfy.sh")
    if not url: return
    p = {"suave":"low","normal":"default","urgente":"high"}.get(tipo,"default")
    try:
        r = urllib.request.Request(url, msg.encode(), {"Priority":p,"Title":"Agente IA"})
        urllib.request.urlopen(r, timeout=5)
    except: pass

def log(msg, tipo):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    open(LOG,"a",encoding="utf-8").write(f"[{ts}] [{tipo.upper()}] {msg}\n")

msg  = sys.argv[1] if len(sys.argv) > 1 else "Aviso"
tipo = sys.argv[2].lower() if len(sys.argv) > 2 else "normal"
if tipo not in SOUNDS: tipo = "normal"

print(f"[{tipo.upper()}] {msg}")
sonido(tipo); popup(msg, tipo); discord(msg, tipo); ntfy(msg, tipo); log(msg, tipo)
