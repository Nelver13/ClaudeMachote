#!/usr/bin/env python3
"""
auto_setup.py — Se ejecuta al abrir el proyecto (SessionStart hook).
Detecta si el sistema ya está configurado. Si no → arranca setup automático.
"""
import sys
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parents[2]  # acciones → sistema-ia → raíz
ESTADO = ROOT / "ESTADO.md"
SESIONES_DIR = ROOT / "sistema-ia" / "memoria" / "sesiones"


def proteger_gitignore():
    """
    Asegura que sistema-ia/ esté en .gitignore del proyecto.
    Se ejecuta siempre al abrir — silencioso si ya está protegido.
    """
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
    return sesiones[0].read_text(encoding="utf-8")[-500:]  # últimas 500 chars


def main():
    proteger_gitignore()  # siempre — silencioso si ya está protegido

    if not proyecto_configurado():
        # Proyecto recién clonado — necesita configuración
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
        # Proyecto ya configurado — carga contexto de la última sesión
        estado = leer_estado()
        ultima = leer_ultima_sesion()

        proj    = estado.get("PROJ", "?")
        modulo  = estado.get("MODULO", "ninguno")
        plan    = estado.get("PLAN", "ninguno")
        progreso= estado.get("PROGRESO", "0%")
        checkpoint = estado.get("CHECKPOINT", "nunca")
        last_aviso = estado.get("LAST_AVISO", "ninguno")
        next_task  = estado.get("NEXT_TASK", "ninguno")
        estado_plan= estado.get("ESTADO_PLAN", "")

        sesion_ctx = f"\nÚltima sesión:\n{ultima}" if ultima else ""

        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"""SISTEMA-IA CARGADO — {proj}
Checkpoint: {checkpoint}
Módulo: {modulo} | Plan: {plan} | Progreso: {progreso}
Estado plan: {estado_plan}
Último aviso: {last_aviso}
Próxima tarea: {next_task}{sesion_ctx}

Lee INICIO.md → detecta tu rol → confirma con una línea y espera instrucciones."""
            }
        }

    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
