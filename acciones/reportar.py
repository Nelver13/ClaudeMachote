#!/usr/bin/env python3
"""
reportar.py — Bug reporter universal con hotkey.
Captura screenshots, permite anotar, y guarda en bugs/backlog.md.
Funciona con cualquier aplicación (OS-level).

Se activa automáticamente al iniciar sesión IA (auto_setup.py).
Hotkey: Alt+R

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
import tempfile
ACTIVO_FILE = Path(tempfile.gettempdir()) / "sistema_ia_activo.path"


def encontrar_raiz():
    """
    1. Lee archivo de proyecto activo (escrito por run.bat/run.sh)
    2. Si no existe, sube directorios buscando ESTADO.md
    3. Si no encuentra, devuelve None
    """
    if ACTIVO_FILE.exists():
        try:
            ruta = Path(ACTIVO_FILE.read_text(encoding="utf-8").strip())
            if (ruta / "ESTADO.md").exists():
                return ruta
        except Exception:
            pass

    current = SIA_DIR
    for _ in range(6):
        if (current / "ESTADO.md").exists():
            return current
        current = current.parent
    return None


ROOT = encontrar_raiz()

# Fallback: backlog global si no hay proyecto detectado
if ROOT is None:
    ROOT = Path.home() / ".sistema-ia-global"
    ROOT.mkdir(parents=True, exist_ok=True)
    BUGS_DIR = ROOT / "bugs"
    SCREENSHOTS_DIR = BUGS_DIR / "screenshots"
    BACKLOG_FILE = BUGS_DIR / "backlog.md"
    print("[reportar] ⚠ No se detectó proyecto activo. Usando backlog global.")
else:
    BUGS_DIR = ROOT / "sistema-ia" / "discusiones" / "bugs"
    SCREENSHOTS_DIR = BUGS_DIR / "screenshots"
    BACKLOG_FILE = BUGS_DIR / "backlog.md"
    print(f"[reportar] Proyecto activo: {ROOT.name}")

# ── SINGLETON: solo un reporter activo a la vez (sistema completo) ──────────
# El último proyecto en arrancar "gana". Si ya hay uno corriendo, lo mata.
import tempfile
PID_FILE = Path(tempfile.gettempdir()) / "reportar_bug_active.pid"

def tomar_control():
    """Mata cualquier reporter previo y registra este proceso como el activo."""
    if PID_FILE.exists():
        try:
            old_pid = int(PID_FILE.read_text().strip())
            if old_pid != os.getpid():
                import signal
                try:
                    if sys.platform == "win32":
                        import subprocess
                        subprocess.run(["taskkill", "/F", "/PID", str(old_pid)],
                                       capture_output=True)
                    else:
                        os.kill(old_pid, signal.SIGTERM)
                    print(f"[reportar] Reporter anterior (PID {old_pid}) detenido.")
                except Exception:
                    pass  # Ya estaba muerto
        except Exception:
            pass
    PID_FILE.write_text(str(os.getpid()))

def liberar_control():
    """Elimina el PID file al salir."""
    try:
        if PID_FILE.exists() and int(PID_FILE.read_text().strip()) == os.getpid():
            PID_FILE.unlink()
    except Exception:
        pass

# Asegurar que las carpetas existan desde que arranca el script
BUGS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
if not BACKLOG_FILE.exists():
    BACKLOG_FILE.write_text("# Bugs Reportados\n> Usa Alt+R para reportar bugs con screenshot y descripción.\n", encoding="utf-8")

# Diagnóstico visible al arrancar
print(f"[reportar] Raíz del proyecto : {ROOT}")
print(f"[reportar] Guardando bugs en  : {BUGS_DIR}")
print(f"[reportar] Backlog            : {BACKLOG_FILE}")


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
    """Muestra diálogo con preview del screenshot donde el usuario puede dibujar rectángulos rojos para marcar el bug."""
    try:
        import tkinter as tk
        from tkinter import scrolledtext
        from PIL import Image, ImageTk, ImageDraw

        ventana_activa = obtener_ventana_activa()

        # Cargar screenshot para preview
        img_original = None
        img_display = None
        scale_factor = 1.0
        if screenshot_path and screenshot_path.exists():
            img_original = Image.open(str(screenshot_path))
            # Escalar para que quepa en pantalla (max 900x500)
            max_w, max_h = 900, 500
            w, h = img_original.size
            scale_factor = min(max_w / w, max_h / h, 1.0)
            new_w, new_h = int(w * scale_factor), int(h * scale_factor)
            img_display = img_original.resize((new_w, new_h), Image.LANCZOS)

        root = tk.Tk()
        root.title(f"🐛 Bug #{bug_num} — Marca el problema y describe")
        root.attributes("-topmost", True)
        root.configure(bg="#1a1a2e")

        fg = "#e0e0e0"
        bg_color = "#1a1a2e"
        entry_bg = "#16213e"

        # Header
        header = tk.Frame(root, bg=bg_color)
        header.pack(fill="x", padx=10, pady=(8, 4))
        tk.Label(header, text=f"🐛 Bug #{bug_num}", font=("Segoe UI", 14, "bold"),
                 fg="#e94560", bg=bg_color).pack(side="left")
        tk.Label(header, text=f"  |  {ventana_activa[:50]}",
                 font=("Segoe UI", 9), fg="#7f8c8d", bg=bg_color).pack(side="left")
        tk.Label(header, text="Dibuja rectángulos rojos sobre el screenshot para señalar el bug",
                 font=("Segoe UI", 9, "italic"), fg="#27ae60", bg=bg_color).pack(side="right")

        # Canvas con screenshot
        canvas = None
        tk_img = None
        rects = []  # lista de rectángulos dibujados
        draw_data = {"start_x": 0, "start_y": 0, "current_rect": None}

        if img_display:
            canvas_frame = tk.Frame(root, bg="#000", bd=2, relief="sunken")
            canvas_frame.pack(fill="both", expand=True, padx=10, pady=4)

            tk_img = ImageTk.PhotoImage(img_display)
            canvas = tk.Canvas(canvas_frame, width=img_display.width, height=img_display.height,
                              bg="#000", highlightthickness=0, cursor="crosshair")
            canvas.pack()
            canvas.create_image(0, 0, anchor="nw", image=tk_img)

            def on_press(event):
                draw_data["start_x"] = event.x
                draw_data["start_y"] = event.y
                draw_data["current_rect"] = canvas.create_rectangle(
                    event.x, event.y, event.x, event.y,
                    outline="#ff0000", width=3
                )

            def on_drag(event):
                if draw_data["current_rect"]:
                    canvas.coords(draw_data["current_rect"],
                                  draw_data["start_x"], draw_data["start_y"],
                                  event.x, event.y)

            def on_release(event):
                if draw_data["current_rect"]:
                    x1 = int(draw_data["start_x"] / scale_factor)
                    y1 = int(draw_data["start_y"] / scale_factor)
                    x2 = int(event.x / scale_factor)
                    y2 = int(event.y / scale_factor)
                    
                    num = len(rects) + 1

                    def pedir_descripcion_marca(num):
                        dlg = tk.Toplevel(root)
                        dlg.title(f"Marca #{num}")
                        dlg.geometry("450x180")
                        dlg.attributes("-topmost", True)
                        dlg.configure(bg="#1a1a2e")
                        dlg.transient(root)
                        dlg.grab_set()

                        resultado = {"desc": None}

                        tk.Label(dlg, text=f"¿Qué señala esta marca #{num}?", font=("Segoe UI", 11), bg="#1a1a2e", fg="#e0e0e0").pack(pady=(15, 5))
                        
                        entry = tk.Entry(dlg, font=("Segoe UI", 11), bg="#16213e", fg="#e0e0e0", insertbackground="#e0e0e0")
                        entry.pack(pady=5, padx=20, fill="x")
                        entry.focus_set()

                        def btn_ok(event=None):
                            resultado["desc"] = entry.get().strip()
                            dlg.destroy()

                        def btn_dictar_marca():
                            if not hasattr(btn_dic, "is_recording"):
                                btn_dic.is_recording = False
                            
                            if not btn_dic.is_recording:
                                btn_dic.is_recording = True
                                btn_dic.audio_frames = []
                                btn_dic.config(text="🛑 Parar", bg="#ff0000")
                                
                                def record_thread():
                                    try:
                                        import pyaudio
                                        import speech_recognition as sr
                                        p = pyaudio.PyAudio()
                                        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
                                        while getattr(btn_dic, "is_recording", False):
                                            data = stream.read(1024, exception_on_overflow=False)
                                            btn_dic.audio_frames.append(data)
                                        stream.stop_stream()
                                        stream.close()
                                        p.terminate()
                                        
                                        btn_dic.config(text="⏳ Proc...", bg="#f39c12")
                                        dlg.update()
                                        
                                        audio_data = b''.join(btn_dic.audio_frames)
                                        if len(audio_data) > 0:
                                            audio = sr.AudioData(audio_data, 16000, 2)
                                            r = sr.Recognizer()
                                            txt = r.recognize_google(audio, language='es-ES')
                                            
                                            current = entry.get()
                                            entry.delete(0, tk.END)
                                            entry.insert(0, (current + " " + txt).strip())
                                    except Exception as e:
                                        print(f"Error dictando: {e}")
                                    finally:
                                        try:
                                            btn_dic.config(text="🎤 Dictar", bg="#2980b9")
                                        except tk.TclError:
                                            pass # La ventana podría haberse cerrado
                                
                                import threading
                                threading.Thread(target=record_thread, daemon=True).start()
                            else:
                                btn_dic.is_recording = False

                        frame_btns = tk.Frame(dlg, bg="#1a1a2e")
                        frame_btns.pack(pady=(10, 15), fill="x", padx=20)

                        tk.Button(frame_btns, text="Cancelar", command=dlg.destroy, bg="#2c3e50", fg="white", relief="flat", padx=10, pady=3).pack(side="right", padx=(5, 0))
                        tk.Button(frame_btns, text="Aceptar", command=btn_ok, bg="#e94560", fg="white", relief="flat", padx=10, font=("Segoe UI", 10, "bold"), pady=3).pack(side="right")
                        btn_dic = tk.Button(frame_btns, text="🎤 Dictar", command=btn_dictar_marca, bg="#2980b9", fg="white", relief="flat", padx=10, font=("Segoe UI", 10, "bold"), pady=3)
                        btn_dic.pack(side="left")

                        dlg.bind("<Return>", btn_ok)
                        
                        # Centrar la ventanita respecto a la ventana principal
                        dlg.update_idletasks()
                        x = root.winfo_x() + (root.winfo_width() // 2) - (dlg.winfo_width() // 2)
                        y = root.winfo_y() + (root.winfo_height() // 2) - (dlg.winfo_height() // 2)
                        dlg.geometry(f"+{x}+{y}")
                        
                        root.wait_window(dlg)
                        return resultado["desc"]

                    # Pedir descripción para la marca
                    desc_marca = pedir_descripcion_marca(num)
                    
                    if desc_marca:
                        rects.append((x1, y1, x2, y2, num))
                        
                        # Dibujar el número en el canvas
                        cx = min(draw_data["start_x"], event.x)
                        cy = max(draw_data["start_y"], event.y)
                        
                        # Sombra para el texto para que resalte
                        canvas.create_text(cx + 6, cy + 6, text=str(num), fill="black", font=("Arial", 16, "bold"), anchor="nw", tags="marks")
                        canvas.create_text(cx + 5, cy + 5, text=str(num), fill="#00ff00", font=("Arial", 16, "bold"), anchor="nw", tags="marks")
                        
                        # Añadir la descripción al text area automáticamente
                        current_text = texto.get("1.0", "end").strip()
                        nueva_linea = f"Marca #{num}: {desc_marca}"
                        if current_text:
                            texto.insert("end", f"\n{nueva_linea}")
                        else:
                            texto.insert("end", nueva_linea)
                    else:
                        # Si cancela, borrar el rectángulo del canvas
                        canvas.delete(draw_data["current_rect"])

                    draw_data["current_rect"] = None

            def undo(event=None):
                if rects:
                    rects.pop()
                    # Redibujar canvas
                    canvas.delete("all")
                    canvas.create_image(0, 0, anchor="nw", image=tk_img)
                    for (x1, y1, x2, y2, num) in rects:
                        canvas.create_rectangle(
                            int(x1 * scale_factor), int(y1 * scale_factor),
                            int(x2 * scale_factor), int(y2 * scale_factor),
                            outline="#ff0000", width=3
                        )
                        cx = min(int(x1 * scale_factor), int(x2 * scale_factor))
                        cy = max(int(y1 * scale_factor), int(y2 * scale_factor))
                        canvas.create_text(cx + 6, cy + 6, text=str(num), fill="black", font=("Arial", 16, "bold"), anchor="nw", tags="marks")
                        canvas.create_text(cx + 5, cy + 5, text=str(num), fill="#00ff00", font=("Arial", 16, "bold"), anchor="nw", tags="marks")

            canvas.bind("<ButtonPress-1>", on_press)
            canvas.bind("<B1-Motion>", on_drag)
            canvas.bind("<ButtonRelease-1>", on_release)
            root.bind("<Control-z>", undo)

        # Descripción
        desc_frame = tk.Frame(root, bg=bg_color)
        desc_frame.pack(fill="x", padx=10, pady=(4, 2))
        tk.Label(desc_frame, text="Descripción general:", font=("Segoe UI", 10),
                 fg=fg, bg=bg_color).pack(side="left")
        tk.Label(desc_frame, text="(Ctrl+Z = deshacer marca, Ctrl+Enter = enviar)",
                 font=("Segoe UI", 8), fg="#7f8c8d", bg=bg_color).pack(side="right")

        texto = scrolledtext.ScrolledText(root, height=5, font=("Segoe UI", 10),
                                           bg=entry_bg, fg=fg,
                                           insertbackground=fg,
                                           relief="flat", borderwidth=2)
        texto.pack(fill="x", padx=10, pady=(0, 4))
        texto.focus_set()

        resultado = {"descripcion": None}

        def enviar(event=None):
            desc = texto.get("1.0", "end").strip()
            if desc:
                resultado["descripcion"] = desc
                # Dibujar rectángulos en la imagen original y guardar
                if img_original and rects:
                    draw = ImageDraw.Draw(img_original)
                    from PIL import ImageFont
                    try:
                        font = ImageFont.truetype("arialbd.ttf", 32)
                    except IOError:
                        font = ImageFont.load_default()
                        
                    for (x1, y1, x2, y2, num) in rects:
                        draw.rectangle([x1, y1, x2, y2], outline="red", width=4)
                        cx = min(x1, x2)
                        cy = max(y1, y2)
                        # Shadow
                        draw.text((cx + 8, cy + 8), str(num), fill="black", font=font)
                        # Text
                        draw.text((cx + 5, cy + 5), str(num), fill="#00ff00", font=font)
                    img_original.save(str(screenshot_path))
            root.destroy()

        def cancelar():
            root.destroy()

        def dictar_audio():
            if not hasattr(btn_dictar, "is_recording"):
                btn_dictar.is_recording = False
            
            if not btn_dictar.is_recording:
                btn_dictar.is_recording = True
                btn_dictar.audio_frames = []
                btn_dictar.config(text="🛑 Parar", bg="#ff0000")
                
                def record_thread():
                    try:
                        import pyaudio
                        import speech_recognition as sr
                        p = pyaudio.PyAudio()
                        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
                        while getattr(btn_dictar, "is_recording", False):
                            data = stream.read(1024, exception_on_overflow=False)
                            btn_dictar.audio_frames.append(data)
                        stream.stop_stream()
                        stream.close()
                        p.terminate()
                        
                        btn_dictar.config(text="⏳ Procesando...", bg="#f39c12")
                        root.update()
                        
                        audio_data = b''.join(btn_dictar.audio_frames)
                        if len(audio_data) > 0:
                            audio = sr.AudioData(audio_data, 16000, 2)
                            r = sr.Recognizer()
                            texto_dictado = r.recognize_google(audio, language='es-ES')
                            
                            current_text = texto.get("1.0", "end").strip()
                            if current_text:
                                texto.insert("end", f" {texto_dictado}")
                            else:
                                texto.insert("end", texto_dictado)
                                
                    except Exception as e:
                        print(f"Error dictando: {e}")
                    finally:
                        try:
                            btn_dictar.config(text="🎤 Dictar", bg="#2980b9")
                        except tk.TclError:
                            pass

                import threading
                threading.Thread(target=record_thread, daemon=True).start()
            else:
                btn_dictar.is_recording = False

        frame_btns = tk.Frame(root, bg=bg_color)
        frame_btns.pack(fill="x", padx=10, pady=(0, 8))

        tk.Button(frame_btns, text="Cancelar", command=cancelar,
                  font=("Segoe UI", 10), bg="#2c3e50", fg=fg,
                  relief="flat", padx=12, pady=4).pack(side="right", padx=(5, 0))

        tk.Button(frame_btns, text="📤 Enviar", command=enviar,
                  font=("Segoe UI", 10, "bold"), bg="#e94560", fg="white",
                  relief="flat", padx=12, pady=4).pack(side="right", padx=(5, 0))
                  
        btn_dictar = tk.Button(frame_btns, text="🎤 Dictar", command=dictar_audio,
                  font=("Segoe UI", 10, "bold"), bg="#2980b9", fg="white",
                  relief="flat", padx=12, pady=4)
        btn_dictar.pack(side="left")

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
    print(f"[reportar] ↳ {BACKLOG_FILE}")


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
    """Inicia el listener de hotkey Alt+R."""
    try:
        from pynput import keyboard

        # Combinación: Alt + R
        current_keys = set()

        def on_press(key):
            current_keys.add(key)
            if keyboard.Key.alt_l in current_keys and keyboard.KeyCode.from_char('r') in current_keys:
                # Ejecutar en thread separado para no bloquear el listener
                threading.Thread(target=reportar_bug, daemon=True).start()

        def on_release(key):
            current_keys.discard(key)

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        print("[reportar] 🐛 Bug reporter activo — Alt+R para reportar")
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

    # Modo servidor: tomar control (mata reporter anterior si existe)
    import atexit
    tomar_control()
    atexit.register(liberar_control)

    # Escuchar hotkey indefinidamente
    iniciar_listener()


if __name__ == "__main__":
    main()
