#!/usr/bin/env python3
"""
reportar.py — Bug reporter universal con hotkey.
Captura screenshots, permite anotar, y guarda en bugs/backlog.md.
Funciona con cualquier aplicación (OS-level).

Se activa automáticamente al iniciar sesión IA (auto_setup.py).
Hotkey: Ctrl+Shift+B

Dependencias: pip install Pillow pynput
"""
import sys
import os
import json
import threading
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
SIA_DIR = SCRIPT_DIR.parent

# Buscar raíz del proyecto (donde vive ESTADO.md)
def encontrar_raiz():
    current = SIA_DIR
    for _ in range(6):
        if (current / "ESTADO.md").exists():
            return current
        current = current.parent
    return SIA_DIR.parent

ROOT = encontrar_raiz()
BUGS_DIR = ROOT / "sistema-ia" / "discusiones" / "bugs"
SCREENSHOTS_DIR = BUGS_DIR / "screenshots"
BACKLOG_FILE = BUGS_DIR / "backlog.md"


def contar_bugs():
    """Cuenta bugs existentes para generar el siguiente número."""
    if not BACKLOG_FILE.exists():
        return 0
    contenido = BACKLOG_FILE.read_text(encoding="utf-8")
    import re
    nums = re.findall(r'## Bug #(\d+)', contenido)
    return max(int(n) for n in nums) if nums else 0


def capturar_screenshot(bug_num):
    """Captura screenshot de la pantalla activa."""
    try:
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        path = SCREENSHOTS_DIR / f"bug-{bug_num:03d}.png"
        screenshot.save(str(path))
        return path
    except Exception as e:
        print(f"[reportar] Error capturando screenshot: {e}")
        return None


def obtener_ventana_activa():
    """Intenta obtener el título de la ventana activa (Windows)."""
    try:
        import ctypes
        user32 = ctypes.windll.user32
        h_wnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(h_wnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(h_wnd, buf, length + 1)
        return buf.value or "Desconocida"
    except Exception:
        return "Desconocida"


def mostrar_dialogo(screenshot_path, bug_num):
    """Muestra un diálogo tkinter para que el usuario describa el bug."""
    try:
        import tkinter as tk
        from tkinter import scrolledtext

        ventana_activa = obtener_ventana_activa()

        root = tk.Tk()
        root.title(f"🐛 Reportar Bug #{bug_num}")
        root.geometry("500x350")
        root.attributes("-topmost", True)
        root.configure(bg="#1a1a2e")

        # Estilo
        fg = "#e0e0e0"
        bg = "#1a1a2e"
        entry_bg = "#16213e"

        tk.Label(root, text=f"Bug #{bug_num}", font=("Segoe UI", 16, "bold"),
                 fg="#e94560", bg=bg).pack(pady=(15, 5))

        tk.Label(root, text=f"Ventana: {ventana_activa[:60]}",
                 font=("Segoe UI", 9), fg="#7f8c8d", bg=bg).pack()

        if screenshot_path:
            tk.Label(root, text=f"📸 Screenshot guardado",
                     font=("Segoe UI", 9), fg="#27ae60", bg=bg).pack(pady=(5, 0))

        tk.Label(root, text="Descripción del bug:",
                 font=("Segoe UI", 10), fg=fg, bg=bg, anchor="w").pack(
                     fill="x", padx=20, pady=(15, 5))

        texto = scrolledtext.ScrolledText(root, height=6, font=("Segoe UI", 10),
                                           bg=entry_bg, fg=fg,
                                           insertbackground=fg,
                                           relief="flat", borderwidth=2)
        texto.pack(fill="both", expand=True, padx=20)
        texto.focus_set()

        resultado = {"descripcion": None}

        def enviar(event=None):
            desc = texto.get("1.0", "end").strip()
            if desc:
                resultado["descripcion"] = desc
            root.destroy()

        def cancelar():
            root.destroy()

        frame_btns = tk.Frame(root, bg=bg)
        frame_btns.pack(fill="x", padx=20, pady=15)

        tk.Button(frame_btns, text="Cancelar", command=cancelar,
                  font=("Segoe UI", 10), bg="#2c3e50", fg=fg,
                  relief="flat", padx=15, pady=5).pack(side="right", padx=(5, 0))

        tk.Button(frame_btns, text="📤 Enviar", command=enviar,
                  font=("Segoe UI", 10, "bold"), bg="#e94560", fg="white",
                  relief="flat", padx=15, pady=5).pack(side="right")

        root.bind("<Control-Return>", enviar)
        root.mainloop()

        return resultado["descripcion"], ventana_activa

    except Exception as e:
        print(f"[reportar] Error mostrando diálogo: {e}")
        return None, "Desconocida"


def guardar_bug(bug_num, descripcion, ventana, screenshot_path):
    """Guarda el bug en backlog.md."""
    BUGS_DIR.mkdir(parents=True, exist_ok=True)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    screenshot_rel = f"screenshots/bug-{bug_num:03d}.png" if screenshot_path else "(sin screenshot)"

    entrada = f"""
## Bug #{bug_num} — {fecha}
- **Ventana:** {ventana}
- **Descripción:** {descripcion}
- **Screenshot:** {screenshot_rel}
- **Estado:** pendiente

"""

    if not BACKLOG_FILE.exists():
        BACKLOG_FILE.write_text(f"# Bugs Reportados\n{entrada}", encoding="utf-8")
    else:
        with open(BACKLOG_FILE, "a", encoding="utf-8") as f:
            f.write(entrada)

    print(f"[reportar] Bug #{bug_num} guardado en backlog.md")


def reportar_bug():
    """Flujo completo de reporte de bug."""
    bug_num = contar_bugs() + 1
    print(f"[reportar] Capturando bug #{bug_num}...")

    # Capturar screenshot
    screenshot_path = capturar_screenshot(bug_num)

    # Mostrar diálogo
    descripcion, ventana = mostrar_dialogo(screenshot_path, bug_num)

    if not descripcion:
        # Usuario canceló
        if screenshot_path and screenshot_path.exists():
            screenshot_path.unlink()
        print("[reportar] Reporte cancelado.")
        return

    # Guardar
    guardar_bug(bug_num, descripcion, ventana, screenshot_path)

    # Notificación
    try:
        import subprocess
        subprocess.Popen(
            ["powershell", "-NoProfile", "-Command",
             f"$wshell = New-Object -ComObject WScript.Shell;"
             f"$null = $wshell.Popup('Bug #{bug_num} reportado', 3, 'Bug Reporter', 0x40);"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception:
        pass


def iniciar_listener():
    """Inicia el listener de hotkey Ctrl+Shift+B."""
    try:
        from pynput import keyboard

        # Combinación: Ctrl + Shift + B
        COMBO = {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode.from_char('b')}
        current_keys = set()

        def on_press(key):
            current_keys.add(key)
            if all(k in current_keys for k in COMBO):
                # Ejecutar en thread separado para no bloquear el listener
                threading.Thread(target=reportar_bug, daemon=True).start()

        def on_release(key):
            current_keys.discard(key)

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        print("[reportar] 🐛 Bug reporter activo — Ctrl+Shift+B para reportar")
        listener.join()

    except ImportError:
        print("[reportar] ERROR: pynput no instalado. Ejecuta: pip install pynput")
        sys.exit(1)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("[reportar] Ejecutando reporte de prueba...")
        reportar_bug()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # Solo verificar que todo funciona
        try:
            from PIL import ImageGrab
            from pynput import keyboard
            print("[reportar] OK: dependencias instaladas")
        except ImportError as e:
            print(f"[reportar] FALTA: {e}")
            print("Ejecuta: pip install Pillow pynput")
        return

    # Modo servidor: escuchar hotkey indefinidamente
    iniciar_listener()


if __name__ == "__main__":
    main()
