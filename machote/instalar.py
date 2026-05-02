#!/usr/bin/env python3
"""
instalar.py — Instala el sistema multi-IA en un proyecto.
Clonar + ejecutar esto = listo. No necesitas que la IA complete nada manualmente.

Uso:
  # Después de clonar como sistema-ia/
  python sistema-ia/instalar.py

  # O especificando ruta
  python sistema-ia/instalar.py /ruta/al/proyecto
"""
import os
import shutil
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime


def _detectar_destino() -> Path:
    """Detecta la raíz del proyecto a instalar."""
    script_dir = Path(__file__).parent.resolve()

    # Si estamos en sistema-ia/ o sistema-ia/machote/ → proyecto es abuelo o bisabuelo
    if script_dir.name == "sistema-ia":
        return script_dir.parent
    if script_dir.name == "machote":
        return script_dir.parent.parent  # machote/ está dentro de sistema-ia/
    if script_dir.name == "acciones":
        # podría ser sistema-ia/acciones/
        return script_dir.parent.parent

    # Default: directorio actual, o argumento
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    return Path.cwd().resolve()


MACHOTE_DIR = Path(__file__).parent.resolve()


def instalar(destino: Path):
    print(f"=== Instalando sistema-IA en: {destino} ===")
    print()

    sia = destino / "sistema-ia"

    # ── 1. Archivos raíz (templates del proyecto) ─────────────────────────────
    raiz_files = ["INICIO.md", "AGENTS.md", "ESTADO.md",
                  "CLAUDE.md", "KIMI.md", "CODEX.md", "GEMINI.md"]
    for f in raiz_files:
        src = MACHOTE_DIR / f
        if not src.exists() and MACHOTE_DIR.name == "acciones":
            # Si estamos en sistema-ia/acciones/, subir a buscar en raíz del machote
            src = MACHOTE_DIR.parent.parent / f
        if not src.exists() and MACHOTE_DIR.name == "machote":
            src = MACHOTE_DIR / f
        if not src.exists():
            # Crear template mínimo inline si no existe físico
            src = None

        dst = destino / f
        if dst.exists():
            print(f"  SKIP (ya existe): {f}")
            continue

        if src and src.exists():
            shutil.copy2(src, dst)
        else:
            # Template inline mínimo
            nombre_proyecto = destino.name
            templates_inline = {
                "INICIO.md": f"""# {nombre_proyecto}

[Descripción, stack, arquitectura]

## Cómo empezar
Lee: AGENTS.md → ESTADO.md → sistema-ia/PROMPT_MAESTRO.md
""",
                "AGENTS.md": """# Reglas para todas las IAs

[Reglas universales del proyecto]

Lee: sistema-ia/PROMPT_MAESTRO.md para la estructura de trabajo.
""",
                "ESTADO.md": f"""[PROJ: {nombre_proyecto}]
[STACK: ]
[DESC: ]

[ROL_CLAUDE: ARQUITECTO]
[ROL_KIMI: DESARROLLADOR]
[ROL_CODEX: DESARROLLADOR]
[ROL_GEMINI: DESARROLLADOR]

[MODULO: ]
[PLAN: ]
[ESTADO_PLAN: ]
[TAREA_ACTUAL: ]
[TOTAL_TAREAS: ]
[PROGRESO: 0%]
[LAST_TASK: ]
[NEXT_TASK: ]
[CHECKPOINT: ]
[LAST_AVISO: ]

[HISTORIAL_PLANES:]
""",
                "CLAUDE.md": """# Claude — Instrucciones

[Comportamiento esperado de Claude en este proyecto]

Lee primero: INICIO.md → AGENTS.md → sistema-ia/PROMPT_MAESTRO.md
""",
                "KIMI.md": """# Kimi — Instrucciones

[Comportamiento esperado de Kimi en este proyecto]

Lee primero: INICIO.md → AGENTS.md → sistema-ia/PROMPT_MAESTRO.md
""",
                "CODEX.md": """# Codex — Instrucciones

[Comportamiento esperado de Codex en este proyecto]

Lee primero: INICIO.md → AGENTS.md → sistema-ia/PROMPT_MAESTRO.md
""",
                "GEMINI.md": """# Gemini — Instrucciones

[Comportamiento esperado de Gemini en este proyecto]

Lee primero: INICIO.md → AGENTS.md → sistema-ia/PROMPT_MAESTRO.md
""",
            }
            dst.write_text(templates_inline.get(f, f"# {f}\n"), encoding="utf-8")
        print(f"  OK: {f}")

    # ── 2. Carpetas sistema-ia/ ───────────────────────────────────────────────
    carpetas = [
        "planes", "discusiones", "discusiones/bugs",
        "discusiones/bugs/screenshots", "memoria/sesiones",
        "handoff", "logs", "complemento", "complemento/investigaciones",
        "complemento/guias", "complemento/ideas", "complemento/referencias",
        "app",
    ]
    for c in carpetas:
        (sia / c).mkdir(parents=True, exist_ok=True)
        gitkeep = sia / c / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
    print("  OK: carpetas sistema-ia/")

    # ── 3. .claude/settings.json en raíz del PROYECTO ─────────────────────────
    claude_dir = destino / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    settings_dst = claude_dir / "settings.json"
    settings = {
        "permissions": {
            "defaultMode": "acceptEdits",
            "allow": [
                "Bash(python*)", "Bash(python3*)", "Read(**)",
                "Write(sistema-ia/**)", "Write(discusiones/**)",
                "Write(planes/**)", "Write(memoria/**)",
                "Edit(sistema-ia/**)", "Edit(discusiones/**)",
                "Edit(planes/**)", "Edit(memoria/**)",
                "Edit(ESTADO.md)", "Edit(INICIO.md)", "Edit(AGENTS.md)",
                "Glob(**)", "Grep(**)"
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
        print("  OK: .claude/settings.json")
    else:
        print("  SKIP (ya existe): .claude/settings.json")

    # ── 4. VERSION ────────────────────────────────────────────────────────────
    version_src = None
    for candidato in [
        MACHOTE_DIR / "VERSION",
        MACHOTE_DIR.parent / "VERSION",
        MACHOTE_DIR.parent.parent / "VERSION",
    ]:
        if candidato.exists():
            version_src = candidato
            break
    version_dst = sia / "VERSION"
    if version_src and not version_dst.exists():
        shutil.copy2(version_src, version_dst)
        print("  OK: sistema-ia/VERSION")

    # ── 5. Scripts del sistema ────────────────────────────────────────────────
    # Si estamos en raíz del machote, copiar acciones/ a sistema-ia/acciones/
    acciones_src = None
    for candidato in [
        MACHOTE_DIR / "acciones",
        MACHOTE_DIR / "sistema-ia" / "acciones",
        MACHOTE_DIR.parent / "acciones",
    ]:
        if candidato.exists() and candidato.is_dir():
            acciones_src = candidato
            break

    acciones_dst = sia / "acciones"
    if acciones_src and acciones_src.resolve() != acciones_dst.resolve():
        if acciones_dst.exists():
            shutil.rmtree(acciones_dst)
        shutil.copytree(acciones_src, acciones_dst)
        n_scripts = len(list(acciones_dst.glob("*.py")))
        print(f"  OK: sistema-ia/acciones/ — {n_scripts} scripts copiados")
    elif acciones_dst.exists():
        n_scripts = len(list(acciones_dst.glob("*.py")))
        print(f"  OK: sistema-ia/acciones/ — {n_scripts} scripts ya presentes")

    # Copiar skills
    skills_src = None
    for candidato in [
        MACHOTE_DIR / ".claude" / "skills",
        MACHOTE_DIR.parent / ".claude" / "skills",
        MACHOTE_DIR.parent.parent / ".claude" / "skills",
    ]:
        if candidato.exists() and candidato.is_dir():
            skills_src = candidato
            break

    skills_dst = destino / ".claude" / "skills"
    if skills_src and skills_src.resolve() != skills_dst.resolve():
        if skills_dst.exists():
            shutil.rmtree(skills_dst)
        shutil.copytree(skills_src, skills_dst)
        print("  OK: .claude/skills/ copiados")
    elif skills_dst.exists():
        print("  OK: .claude/skills/ ya presentes")

    # Copiar app/
    app_src = None
    for candidato in [
        MACHOTE_DIR / "app",
        MACHOTE_DIR.parent / "app",
        MACHOTE_DIR.parent.parent / "app",
    ]:
        if candidato.exists() and candidato.is_dir():
            app_src = candidato
            break

    app_dst = sia / "app"
    if app_src and app_src.resolve() != app_dst.resolve():
        if app_dst.exists():
            shutil.rmtree(app_dst)
        shutil.copytree(app_src, app_dst)
        print("  OK: sistema-ia/app/ copiada")
    elif app_dst.exists():
        print("  OK: sistema-ia/app/ ya presente")

    # ── 6. Docs del sistema ───────────────────────────────────────────────────
    docs = ["PROMPT_MAESTRO.md", "ROADMAP.md", "README.md",
            "PLANTILLA_OTROS_PROYECTOS.md", "CHANGELOG.md", "NOVEDADES.md"]
    for doc in docs:
        src = None
        for candidato in [
            MACHOTE_DIR / doc,
            MACHOTE_DIR / "sistema-ia" / doc,
            MACHOTE_DIR.parent / doc,
            MACHOTE_DIR.parent / "sistema-ia" / doc,
        ]:
            if candidato.exists():
                src = candidato
                break
        dst = sia / doc
        if src and not dst.exists():
            shutil.copy2(src, dst)
            print(f"  OK: sistema-ia/{doc}")

    # ── 7. Limpiar residuos del machote ───────────────────────────────────────
    def _rmrf(path: Path):
        if sys.platform == "win32":
            import stat
            def _onexc(func, p, exc):
                os.chmod(p, stat.S_IWRITE)
                func(p)
            shutil.rmtree(path, onexc=_onexc)
        else:
            shutil.rmtree(path)

    for residuo in ["machote", ".git", ".gitignore"]:
        p = sia / residuo
        if p.exists():
            if p.is_dir():
                _rmrf(p)
            else:
                p.unlink()
            print(f"  OK: sistema-ia/{residuo} eliminado")

    # ── 8. .gitignore del proyecto ────────────────────────────────────────────
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

    # ── 9. Discusión 0-vision ─────────────────────────────────────────────────
    vision_dir = sia / "discusiones" / "0-vision"
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

## Ideas Futuras (A consideración)
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

    # ── 10. Backlog bugs ──────────────────────────────────────────────────────
    bugs_dir = sia / "discusiones" / "bugs"
    bugs_dir.mkdir(parents=True, exist_ok=True)
    backlog = bugs_dir / "backlog.md"
    if not backlog.exists():
        backlog.write_text("""# Bugs Reportados

> Usa Alt+R para reportar bugs con screenshot y descripción.
> Los bugs se agregan automáticamente aquí.

""", encoding="utf-8")
        print("  OK: discusiones/bugs/backlog.md creada")
    (bugs_dir / "screenshots").mkdir(parents=True, exist_ok=True)

    # ── 11. run.bat y run.sh ──────────────────────────────────────────────────
    run_bat = destino / "run.bat"
    run_sh = destino / "run.sh"
    if not run_bat.exists():
        run_bat.write_text("""@echo off
REM === Script de ejecución del proyecto ===
REM El arquitecto actualiza esto según el stack definido en 0-vision.
REM El dev solo ejecuta: run.bat

REM Registrar proyecto activo para el bug reporter
echo %CD%> %TEMP%\\sistema_ia_activo.path

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

# Registrar proyecto activo para el bug reporter
pwd > /tmp/sistema_ia_activo.path

# Iniciar el Bug Reporter en background
python sistema-ia/acciones/reportar.py &

echo "[!] Configura este archivo con el comando de tu proyecto."
echo "Ejemplo: npm run dev / python manage.py runserver / cargo tauri dev"
""", encoding="utf-8")
        print("  OK: run.sh creado")

    # ── 12. Dependencias ──────────────────────────────────────────────────────
    print()
    print("Instalando dependencias del bug reporter...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "Pillow", "pynput",
             "SpeechRecognition", "pyaudio", "--quiet"],
            check=True, timeout=120
        )
        print("  OK: Pillow + pynput + SpeechRecognition + pyaudio instalados")
    except Exception as e:
        print(f"  WARN: No se pudo instalar dependencias automáticamente: {e}")
        print("  → Ejecuta manualmente: pip install Pillow pynput SpeechRecognition pyaudio")

    print()
    print("=== Listo ===")
    print("Siguiente paso: la IA te preguntará nombre, stack y roles.")


def mostrar_guia():
    guia = _detectar_destino() / "sistema-ia" / "acciones" / "guia.py"
    if guia.exists():
        try:
            subprocess.run([sys.executable, str(guia)], check=False)
        except Exception:
            pass


if __name__ == "__main__":
    destino = _detectar_destino()
    if not destino.exists():
        print(f"ERROR: No existe {destino}")
        sys.exit(1)
    instalar(destino)
    mostrar_guia()
