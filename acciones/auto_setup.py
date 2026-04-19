#!/usr/bin/env python3
"""
auto_setup.py — SessionStart hook.
Detecta si el proyecto está configurado. Si no → arranca setup.
Detecta versión nueva en git remoto y avisa.

Fix B: Scripts en acciones/ a raíz del repo — git pull los actualiza directo.
"""
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


def _encontrar_raiz() -> Path:
    """Sube hasta 6 niveles buscando el primer dir con ESTADO.md."""
    actual = Path(__file__).parent.resolve()
    for _ in range(6):
        if (actual / 'ESTADO.md').exists():
            return actual
        if actual.parent == actual:
            break
        actual = actual.parent
    return Path(__file__).parents[2]  # fallback


ROOT = _encontrar_raiz()
SIA = ROOT / "sistema-ia"
ESTADO = ROOT / "ESTADO.md"
SESIONES_DIR = SIA / "memoria" / "sesiones"
VERSION_FILE = SIA / "VERSION"


def proteger_gitignore():
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
    """Compara VERSION local vs origin/main. Silencioso si falla."""
    try:
        if not VERSION_FILE.exists():
            return None
        local = VERSION_FILE.read_text(encoding="utf-8").strip()

        git_dir = SIA / ".git"
        if not git_dir.exists():
            return None

        try:
            subprocess.run(
                ["git", "-C", str(SIA), "fetch", "--quiet"],
                timeout=5, capture_output=True, check=False,
            )
        except Exception:
            return None

        try:
            r = subprocess.run(
                ["git", "-C", str(SIA), "show", "origin/main:VERSION"],
                timeout=5, capture_output=True, text=True, check=False,
            )
            if r.returncode != 0:
                return None
            remoto = r.stdout.strip()
        except Exception:
            return None

        if not remoto or remoto == local:
            return None

        return (
            f"⚠ ACTUALIZACIÓN — machote v{remoto} disponible (local v{local}). "
            f"Ejecuta: cd sistema-ia && git pull"
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

ACCIÓN REQUERIDA:
1. Pregunta (UNA por UNA): nombre del proyecto, stack, IAs, rol de cada una
2. Actualiza ESTADO.md
3. Actualiza CLAUDE.md/KIMI.md/etc
4. Avisa: "Listo — [proyecto] configurado"

No hagas nada más hasta completar la configuración."""
            }
        }
    else:
        estado = leer_estado()
        ultima = leer_ultima_sesion()
        aviso_version = detectar_version_desfase()

        proj       = estado.get("PROJ", "?")
        modulo     = estado.get("MODULO", "ninguno")
        plan       = estado.get("PLAN", "ninguno")
        progreso   = estado.get("PROGRESO", "0%")
        checkpoint = estado.get("CHECKPOINT", "nunca")
        last_aviso = estado.get("LAST_AVISO", "ninguno")
        next_task  = estado.get("NEXT_TASK", "ninguno")
        estado_plan= estado.get("ESTADO_PLAN", "")

        sesion_ctx = f"\nÚltima sesión:\n{ultima}" if ultima else ""
        update_ctx = f"\n\n{aviso_version}" if aviso_version else ""

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
