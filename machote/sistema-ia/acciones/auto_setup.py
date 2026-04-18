#!/usr/bin/env python3
"""
auto_setup.py — Se ejecuta al abrir el proyecto (SessionStart hook).
Detecta si el sistema ya está configurado. Si no → arranca setup automático.
Detecta también si hay nueva versión del machote disponible.
"""
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parents[2]  # acciones → sistema-ia → raíz
SIA = ROOT / "sistema-ia"
ESTADO = ROOT / "ESTADO.md"
SESIONES_DIR = SIA / "memoria" / "sesiones"
VERSION_FILE = SIA / "VERSION"


def proteger_gitignore():
    """Asegura que sistema-ia/ esté en .gitignore del proyecto."""
    gitignore = ROOT / ".gitignore"
    lineas_requeridas = [
        "# Sistema IA — local only, nunca subir a git",
        "sistema-ia/",
        "INICIO.md",
        "AGENTS.md",
        "ESTADO.md",
        "CLAUDE.md",
        "KIMI.md",
        "CODEX.md",
        "GEMINI.md",
        "RESUMEN.md",
        "instalar.py",
    ]

    existente = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    agregar = [l for l in lineas_requeridas if l not in existente]

    if agregar:
        with gitignore.open("a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(agregar) + "\n")


def proyecto_configurado() -> bool:
    if not ESTADO.exists():
        return False
    contenido = ESTADO.read_text(encoding="utf-8")
    return "NOMBRE_PROYECTO" not in contenido and "[PROJ:" in contenido


def leer_estado() -> dict:
    if not ESTADO.exists():
        return {}
    data = {}
    for linea in ESTADO.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if linea.startswith("[") and ":" in linea:
            clave = linea[1:linea.index(":")]
            valor = linea[linea.index(":")+1:].rstrip("]").strip()
            data[clave] = valor
    return data


def leer_ultima_sesion() -> str:
    if not SESIONES_DIR.exists():
        return ""
    sesiones = sorted(SESIONES_DIR.glob("*.md"), reverse=True)
    if not sesiones:
        return ""
    return sesiones[0].read_text(encoding="utf-8")[-500:]


def detectar_version_desfase() -> str | None:
    """
    Compara VERSION local con VERSION en origin/main del repo sistema-ia.
    Devuelve string de aviso si hay desfase, o None en cualquier otro caso.
    Silencioso si no hay git, red, o VERSION.
    """
    try:
        if not VERSION_FILE.exists():
            return None
        local = VERSION_FILE.read_text(encoding="utf-8").strip()

        # sistema-ia debe ser un repo git propio (clonado)
        git_dir = SIA / ".git"
        if not git_dir.exists():
            return None

        # fetch silencioso con timeout corto
        try:
            subprocess.run(
                ["git", "-C", str(SIA), "fetch", "--quiet"],
                timeout=5,
                capture_output=True,
                check=False,
            )
        except Exception:
            return None

        # leer VERSION remoto
        try:
            r = subprocess.run(
                ["git", "-C", str(SIA), "show", "origin/main:VERSION"],
                timeout=5,
                capture_output=True,
                text=True,
                check=False,
            )
            if r.returncode != 0:
                return None
            remoto = r.stdout.strip()
        except Exception:
            return None

        if not remoto or remoto == local:
            return None

        return (
            f"⚠ ACTUALIZACIÓN DISPONIBLE — machote v{remoto} (local v{local}). "
            f"Ejecuta: cd sistema-ia && git pull && cd .. && python sistema-ia/acciones/migrar.py"
        )
    except Exception:
        return None


def main():
    proteger_gitignore()

    if not proyecto_configurado():
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": """SISTEMA-IA: Proyecto recién clonado o no configurado.

ACCIÓN REQUERIDA — haz esto ANTES de cualquier otra cosa:
1. Pregunta al humano (UNA por UNA):
   - "Nombre del proyecto?"
   - "Stack? (backend/frontend/fullstack/mobile)"
   - "IAs que van a trabajar? (Claude/Kimi/Codex/Gemini)"
   - "Rol de cada IA hoy?"
2. Con esas respuestas actualiza ESTADO.md (reemplaza NOMBRE_PROYECTO y ajusta roles)
3. Actualiza CLAUDE.md/KIMI.md/etc con el nombre real
4. Avisa: "Listo — [proyecto] configurado — revisa."

No hagas nada más hasta completar la configuración."""
            }
        }
    else:
        estado = leer_estado()
        ultima = leer_ultima_sesion()
        aviso_version = detectar_version_desfase()

        proj    = estado.get("PROJ", "?")
        modulo  = estado.get("MODULO", "ninguno")
        plan    = estado.get("PLAN", "ninguno")
        progreso= estado.get("PROGRESO", "0%")
        checkpoint = estado.get("CHECKPOINT", "nunca")
        last_aviso = estado.get("LAST_AVISO", "ninguno")
        next_task  = estado.get("NEXT_TASK", "ninguno")
        estado_plan= estado.get("ESTADO_PLAN", "")

        sesion_ctx = f"\nÚltima sesión:\n{ultima}" if ultima else ""
        update_ctx = f"\n\n{aviso_version}\n" if aviso_version else ""

        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"""SISTEMA-IA CARGADO — {proj}
Checkpoint: {checkpoint}
Módulo: {modulo} | Plan: {plan} | Progreso: {progreso}
Estado plan: {estado_plan}
Último aviso: {last_aviso}
Próxima tarea: {next_task}{sesion_ctx}{update_ctx}

Lee INICIO.md → detecta tu rol → confirma con una línea y espera instrucciones."""
            }
        }

    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
