#!/usr/bin/env python3
"""
auto_setup.py — SessionStart hook.
- Detecta si el proyecto esta configurado.
- Si hay version nueva: hace git pull automatico + lee NOVEDADES.md
- Inyecta instrucciones de actualizacion para que la IA las ejecute sola.
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
    return Path(__file__).parents[2]


ROOT         = _encontrar_raiz()
SIA          = ROOT / "sistema-ia"
ESTADO       = ROOT / "ESTADO.md"
SESIONES_DIR = SIA / "memoria" / "sesiones"
VERSION_FILE = SIA / "VERSION"
NOVEDADES    = SIA / "NOVEDADES.md"


def proteger_gitignore():
    gitignore = ROOT / ".gitignore"
    lineas_requeridas = [
        "# Sistema IA -- local only, nunca subir a git",
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


def leer_comandos_pendientes() -> str:
    """Lee comandos enviados desde la app móvil (handoff/comando_*.md)."""
    handoff = SIA / "handoff"
    if not handoff.exists():
        return ""
    comandos = sorted(handoff.glob("comando_*.md"))
    if not comandos:
        return ""
    partes = []
    for c in comandos:
        try:
            partes.append(c.read_text(encoding="utf-8"))
            # Mover a procesados para no repetir
            proc = handoff / "procesados"
            proc.mkdir(exist_ok=True)
            c.rename(proc / c.name)
        except Exception:
            pass
    return "\n---\n".join(partes)


def auto_actualizar() -> str | None:
    """
    Si hay version nueva en origin:
    1. Hace git pull automatico en sistema-ia/
    2. Lee NOVEDADES.md
    3. Devuelve las instrucciones para que la IA las ejecute.
    Silencioso si no hay red, git, o VERSION.
    """
    try:
        if not VERSION_FILE.exists():
            return None
        git_dir = SIA / ".git"
        if not git_dir.exists():
            return None

        local = VERSION_FILE.read_text(encoding="utf-8").strip()

        # Fetch silencioso
        try:
            subprocess.run(
                ["git", "-C", str(SIA), "fetch", "--quiet"],
                timeout=5, capture_output=True, check=False,
            )
        except Exception:
            return None

        # Leer VERSION remota
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

        # Hay version nueva — hacer pull automatico
        try:
            pull = subprocess.run(
                ["git", "-C", str(SIA), "pull", "--ff-only", "--quiet"],
                timeout=15, capture_output=True, text=True, check=False,
            )
            pull_ok = pull.returncode == 0
        except Exception:
            pull_ok = False

        if not pull_ok:
            return (
                f"ACTUALIZACION DISPONIBLE v{remoto} (local v{local}) -- "
                f"pull fallo, ejecuta manualmente: cd sistema-ia && git pull"
            )

        # Pull exitoso — borrar machote/ (solo ruido durante el trabajo)
        try:
            import shutil
            machote_dir = SIA / "machote"
            if machote_dir.exists():
                shutil.rmtree(machote_dir)
        except Exception:
            pass

        # Pull exitoso — leer NOVEDADES.md
        novedades_txt = ""
        if NOVEDADES.exists():
            novedades_txt = NOVEDADES.read_text(encoding="utf-8")

        bloque = f"SISTEMA-IA ACTUALIZADO v{local} -> v{remoto}\n"
        if novedades_txt:
            bloque += f"\nINSTRUCCIONES DE ACTUALIZACION — ejecuta esto AHORA antes de continuar:\n\n{novedades_txt}"
        else:
            bloque += "\nNo hay instrucciones de actualizacion pendientes."

        return bloque

    except Exception:
        return None


def limpiar_machote():
    """Borra sistema-ia/machote/ si existe — siempre, no solo al actualizar."""
    try:
        import shutil
        machote_dir = SIA / "machote"
        if machote_dir.exists():
            shutil.rmtree(machote_dir)
    except Exception:
        pass


def main():
    proteger_gitignore()
    limpiar_machote()

    if not proyecto_configurado():
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": """SISTEMA-IA: Proyecto recien clonado o no configurado.

ACCION REQUERIDA:
1. Pregunta (UNA por UNA): nombre del proyecto, stack, IAs, rol de cada una
2. Actualiza ESTADO.md
3. Actualiza CLAUDE.md/KIMI.md/etc
4. Avisa: "Listo -- [proyecto] configurado"

No hagas nada mas hasta completar la configuracion."""
            }
        }
    else:
        estado       = leer_estado()
        ultima       = leer_ultima_sesion()
        actualizacion = auto_actualizar()
        comandos     = leer_comandos_pendientes()

        proj       = estado.get("PROJ", "?")
        modulo     = estado.get("MODULO", "ninguno")
        plan       = estado.get("PLAN", "ninguno")
        progreso   = estado.get("PROGRESO", "0%")
        checkpoint = estado.get("CHECKPOINT", "nunca")
        last_aviso = estado.get("LAST_AVISO", "ninguno")
        next_task  = estado.get("NEXT_TASK", "ninguno")
        estado_plan= estado.get("ESTADO_PLAN", "")

        sesion_ctx  = f"\nUltima sesion:\n{ultima}" if ultima else ""
        update_ctx  = f"\n\n{'='*50}\n{actualizacion}\n{'='*50}" if actualizacion else ""
        cmd_ctx     = f"\n\n{'='*50}\nCOMANDOS PENDIENTES DESDE APP MOVIL:\n{comandos}\n{'='*50}" if comandos else ""

        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"""SISTEMA-IA CARGADO -- {proj}
Checkpoint: {checkpoint}
Modulo: {modulo} | Plan: {plan} | Progreso: {progreso}
Estado plan: {estado_plan}
Ultimo aviso: {last_aviso}
Proxima tarea: {next_task}{sesion_ctx}{update_ctx}{cmd_ctx}

Lee INICIO.md -> detecta tu rol -> confirma con una linea y espera instrucciones."""
            }
        }

    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
