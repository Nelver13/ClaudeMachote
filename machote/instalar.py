#!/usr/bin/env python3
"""
instalar.py — Instala el sistema multi-IA en un proyecto.
Clonar + ejecutar esto = listo.

Uso:
  python sistema-ia/machote/instalar.py            → instala en directorio actual
  python sistema-ia/machote/instalar.py /ruta/     → instala en ruta específica
"""
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

MACHOTE_DIR = Path(__file__).parent   # sistema-ia/machote/


def instalar(destino: Path):
    print(f"Instalando sistema-ia en: {destino}")
    print()

    # 1. Archivos raíz (template del proyecto)
    raiz_files = ["INICIO.md", "AGENTS.md", "ESTADO.md",
                  "CLAUDE.md", "KIMI.md", "CODEX.md", "GEMINI.md"]
    for f in raiz_files:
        src = MACHOTE_DIR / f
        dst = destino / f
        if not src.exists():
            print(f"  SKIP (no en machote): {f}")
            continue
        if dst.exists():
            print(f"  SKIP (ya existe): {f}")
        else:
            shutil.copy2(src, dst)
            print(f"  OK: {f}")

    # 2. Carpetas sistema-ia/
    for c in ["planes", "discusiones", "discusiones/bugs", "discusiones/bugs/screenshots",
              "memoria/sesiones", "handoff", "logs"]:
        (destino / "sistema-ia" / c).mkdir(parents=True, exist_ok=True)
    print("  OK: carpetas sistema-ia/")

    # 3. .claude/settings.json en raíz del PROYECTO
    claude_dir = destino / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    settings_dst = claude_dir / "settings.json"

    settings = {
        "permissions": {
            "defaultMode": "acceptEdits",
            "allow": [
                "Bash(python*)",
                "Bash(python3*)",
                "Read(**)",
                "Write(sistema-ia/**)",
                "Write(discusiones/**)",
                "Write(planes/**)",
                "Write(memoria/**)",
                "Edit(sistema-ia/**)",
                "Edit(discusiones/**)",
                "Edit(planes/**)",
                "Edit(memoria/**)",
                "Edit(ESTADO.md)",
                "Edit(INICIO.md)",
                "Edit(AGENTS.md)",
                "Glob(**)",
                "Grep(**)"
            ]
        },
        "hooks": {
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python sistema-ia/acciones/auto_setup.py"
                        }
                    ]
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Edit|Write",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python sistema-ia/acciones/check_role.py"
                        }
                    ]
                }
            ]
        }
    }

    if not settings_dst.exists():
        settings_dst.write_text(
            json.dumps(settings, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"  OK: .claude/settings.json")
    else:
        print(f"  SKIP (ya existe): .claude/settings.json")

    # 4. Scripts — ya están en sistema-ia/acciones/ (git los trae)
    acciones_dir = destino / "sistema-ia" / "acciones"
    n_scripts = len(list(acciones_dir.glob("*.py"))) if acciones_dir.exists() else 0
    print(f"  OK: sistema-ia/acciones/ — {n_scripts} scripts")

    # 5. VERSION
    version_src = MACHOTE_DIR.parent / "VERSION"
    version_dst = destino / "sistema-ia" / "VERSION"
    if version_src.exists() and not version_dst.exists():
        shutil.copy2(version_src, version_dst)
        print(f"  OK: sistema-ia/VERSION")

    # 6. Borrar machote/ — ya no se necesita
    machote_dst = destino / "sistema-ia" / "machote"
    if machote_dst.exists():
        shutil.rmtree(machote_dst)
        print("  OK: sistema-ia/machote/ eliminado")

    # 7. BORRAR .git/ de sistema-ia — evita repo anidado
    git_dir = destino / "sistema-ia" / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)
        print("  OK: sistema-ia/.git/ eliminado (sin repo anidado)")

    # Borrar .gitignore del repo clonado (es del machote, no del proyecto)
    gitignore_sia = destino / "sistema-ia" / ".gitignore"
    if gitignore_sia.exists():
        gitignore_sia.unlink()
        print("  OK: sistema-ia/.gitignore eliminado")

    # 8. Configurar .gitignore del proyecto
    gitignore_dst = destino / ".gitignore"
    gitignore_rules = """
# ── Sistema IA ───────────────────────────────────────────
# Sube a git: discusiones, planes, ESTADO.md (el equipo los necesita)
# Oculta: scripts, memoria, logs, credenciales (local del dev)
sistema-ia/*
!sistema-ia/discusiones/
!sistema-ia/planes/

# Archivos IA locales (ESTADO.md sí sube)
INICIO.md
AGENTS.md
CLAUDE.md
KIMI.md
CODEX.md
GEMINI.md
RESUMEN.md
instalar.py
"""
    if not gitignore_dst.exists():
        gitignore_dst.write_text(gitignore_rules, encoding="utf-8")
        print("  OK: .gitignore creado")
    else:
        current = gitignore_dst.read_text(encoding="utf-8")
        if "sistema-ia" not in current:
            with open(gitignore_dst, "a", encoding="utf-8") as f:
                f.write("\n" + gitignore_rules)
            print("  OK: .gitignore actualizado")
        else:
            print("  SKIP: .gitignore ya tiene reglas sistema-ia")

    # 9. Crear discusión primaria 0-vision
    vision_dir = destino / "sistema-ia" / "discusiones" / "0-vision"
    vision_dir.mkdir(parents=True, exist_ok=True)
    vision_file = vision_dir / "v1.md"
    if not vision_file.exists():
        fecha = datetime.now().strftime("%Y-%m-%d")
        vision_file.write_text(f"""# Discusión: Visión del Proyecto
**Fecha:** {fecha}  **Estado:** En discusión

## Contexto
[Nombre y descripción del proyecto — se llena con el humano]

## Decisiones cerradas
(vacío)

## Tema actual
### 1. ¿Qué es este proyecto?
Describe en 1-2 líneas qué hace y para quién.

## Temas pendientes
- [ ] Stack tecnológico
- [ ] Módulos/etapas principales
- [ ] Orden de construcción (qué va primero)
- [ ] IAs que participan y sus roles
- [ ] Comando de ejecución del proyecto (para run.bat/run.sh)
""", encoding="utf-8")
        print("  OK: discusiones/0-vision/v1.md creada")

    # 10. Crear bugs backlog
    bugs_dir = destino / "sistema-ia" / "discusiones" / "bugs"
    bugs_dir.mkdir(parents=True, exist_ok=True)
    backlog = bugs_dir / "backlog.md"
    if not backlog.exists():
        backlog.write_text("""# Bugs Reportados

> Usa Ctrl+Shift+B para reportar bugs (requiere reportar.py activo).
> Los bugs se agregan automáticamente aquí.

""", encoding="utf-8")
        print("  OK: discusiones/bugs/backlog.md creada")

    screenshots_dir = bugs_dir / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    # 11. Crear run.bat y run.sh base
    run_bat = destino / "run.bat"
    run_sh = destino / "run.sh"
    if not run_bat.exists():
        run_bat.write_text("""@echo off
REM === Script de ejecución del proyecto ===
REM El arquitecto actualiza esto según el stack definido en 0-vision.
REM El dev solo ejecuta: run.bat

REM Iniciar el Bug Reporter en background
start /B python sistema-ia\\acciones\\reportar.py

echo [!] Configura este archivo con el comando de tu proyecto.
echo Ejemplo: npm run dev / python manage.py runserver / cargo tauri dev
pause
""", encoding="utf-8")
        print("  OK: run.bat creado")

    if not run_sh.exists():
        run_sh.write_text("""#!/bin/bash
# === Script de ejecución del proyecto ===
# El arquitecto actualiza esto según el stack definido en 0-vision.
# El dev solo ejecuta: ./run.sh

# Iniciar el Bug Reporter en background
python sistema-ia/acciones/reportar.py &

echo "[!] Configura este archivo con el comando de tu proyecto."
echo "Ejemplo: npm run dev / python manage.py runserver / cargo tauri dev"
""", encoding="utf-8")
        print("  OK: run.sh creado")

    # 12. Instalar dependencias del bug reporter
    print()
    print("Instalando dependencias del bug reporter...")
    import subprocess
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "Pillow", "pynput", "SpeechRecognition", "pyaudio", "--quiet"],
            check=True, timeout=120
        )
        print("  OK: Pillow + pynput + SpeechRecognition instalados")
def mostrar_guia_tkinter():
    try:
        import tkinter as tk
        from tkinter import font
        
        root = tk.Tk()
        root.title("🚀 ClaudeMachote Instalado con Éxito")
        root.geometry("600x550")
        root.configure(bg="#1a1a2e")
        root.attributes("-topmost", True)
        
        # Estilos
        bg_color = "#1a1a2e"
        fg_color = "#e0e0e0"
        accent_color = "#e94560"
        title_font = font.Font(family="Segoe UI", size=16, weight="bold")
        h2_font = font.Font(family="Segoe UI", size=12, weight="bold")
        text_font = font.Font(family="Segoe UI", size=10)
        
        # Contenedor principal con padding
        main_frame = tk.Frame(root, bg=bg_color, padx=30, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        tk.Label(main_frame, text="✅ Instalación Completa", font=title_font, fg=accent_color, bg=bg_color).pack(anchor="w", pady=(0, 15))
        
        # Sección 1
        tk.Label(main_frame, text="¿QUÉ ES ESTE SISTEMA?", font=h2_font, fg="#4facf7", bg=bg_color).pack(anchor="w", pady=(10, 5))
        desc = "Has configurado una arquitectura multi-IA (Arquitecto/Dev).\nEl sistema organiza el trabajo en: discusiones -> planes -> código.\nMantiene el estado guardado para que la IA nunca pierda contexto."
        tk.Label(main_frame, text=desc, font=text_font, fg=fg_color, bg=bg_color, justify="left").pack(anchor="w")
        
        # Sección 2
        tk.Label(main_frame, text="🐛 NUEVO: BUG REPORTER (v2.6)", font=h2_font, fg="#4facf7", bg=bg_color).pack(anchor="w", pady=(15, 5))
        bugs = "1. Presiona Alt+R en cualquier momento.\n2. Dibuja rectángulos rojos señalando el error en pantalla.\n3. Escribe qué falla (se guarda en: discusiones/bugs/backlog.md).\n4. La IA (Arquitecto) leerá los bugs para planear cómo arreglarlos."
        tk.Label(main_frame, text=bugs, font=text_font, fg=fg_color, bg=bg_color, justify="left").pack(anchor="w")
        
        # Sección 3
        tk.Label(main_frame, text="🔄 SCRIPTS DE EJECUCIÓN", font=h2_font, fg="#4facf7", bg=bg_color).pack(anchor="w", pady=(15, 5))
        scripts = "Usa siempre run.bat o ./run.sh para iniciar tu proyecto.\nEstos scripts arrancan tu app Y lanzan el Bug Reporter en background."
        tk.Label(main_frame, text=scripts, font=text_font, fg=fg_color, bg=bg_color, justify="left").pack(anchor="w")
        
        # Sección 4
        tk.Label(main_frame, text="📝 PRÓXIMOS PASOS (Obligatorio):", font=h2_font, fg=accent_color, bg=bg_color).pack(anchor="w", pady=(15, 5))
        pasos = "1. Abre ESTADO.md → reemplaza NOMBRE_PROYECTO y ajusta roles.\n2. Abre CLAUDE.md/KIMI.md/etc → reemplaza NOMBRE_PROYECTO.\n3. Abre tu editor (ej. Cursor/VSCode) e invoca a tu IA.\n4. Pega el PROMPT DE INSTALACIÓN (está en el README de GitHub).\n5. Sigue las instrucciones de la IA para iniciar la visión (0-vision)."
        tk.Label(main_frame, text=pasos, font=text_font, fg=fg_color, bg=bg_color, justify="left").pack(anchor="w")
        
        # Botón cerrar
        btn_frame = tk.Frame(main_frame, bg=bg_color)
        btn_frame.pack(fill="x", pady=(25, 0))
        tk.Button(btn_frame, text="Entendido, ¡A codear!", command=root.destroy, 
                  font=h2_font, bg=accent_color, fg="white", relief="flat", padx=20, pady=8).pack()
        
        # Centrar ventana
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        root.mainloop()
    except Exception as e:
        print("\n¡Instalación completa! (Error lanzando interfaz gráfica)")

def main():
    destino = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not destino.exists():
        print(f"ERROR: No existe {destino}")
        sys.exit(1)
    instalar(destino)
    mostrar_guia_tkinter()


if __name__ == "__main__":
    main()
