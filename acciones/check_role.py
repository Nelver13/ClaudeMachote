#!/usr/bin/env python3
"""
check_role.py — PreToolUse hook para Claude Code en Keyons
Input: JSON via stdin. Exit 0: permitir | Exit 2: bloquear.
"""
import sys
import json
from pathlib import Path

# acciones/ → ia/ → .claude/ → sistema-ia/ → raíz del proyecto
ROOT = Path(__file__).parents[4]


def leer_rol() -> str | None:
    """Lee [ROL_CLAUDE:] de ESTADO.md o estado.log."""
    candidatos = [
        ROOT / "ESTADO.md",
        ROOT / "sistema-ia" / ".claude" / "ia" / "estado.log",
    ]
    for f in candidatos:
        if f.exists():
            for linea in f.read_text(encoding="utf-8").splitlines():
                if "[ROL_CLAUDE:" in linea:
                    return linea.split(":", 1)[1].strip().rstrip("]").strip()
    return None


def leer_config() -> dict | None:
    """Lee ia_roles.json con reglas por rol."""
    cfg = ROOT / "sistema-ia" / ".claude" / "ia" / "ia_roles.json"
    if cfg.exists():
        return json.loads(cfg.read_text(encoding="utf-8"))
    return None


def main():
    raw = sys.stdin.read() or "{}"
    data = json.loads(raw)

    if data.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    try:
        rel = str(Path(file_path).relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        rel = file_path.replace("\\", "/")

    rol = leer_rol()
    config = leer_config()

    if not rol or not config:
        sys.exit(0)

    reglas = config.get("roles", {}).get(rol.upper(), {})

    # Bloquear escritura en dirs prohibidos
    for p in reglas.get("block_write", []):
        if rel.startswith(p):
            print(f"[ROLE BLOCK] ROL_CLAUDE={rol} no puede escribir en '{p}'")
            print("Cambia tu rol: python sistema-ia/.claude/ia/acciones/cambiar_rol.py claude dev")
            sys.exit(2)

    # En dirs de solo-edición, bloquear creación de archivos nuevos
    for p in reglas.get("allow_existing_only", []):
        if rel.startswith(p) and not Path(file_path).exists():
            print(f"[ROLE BLOCK] ROL_CLAUDE={rol} no puede CREAR archivos nuevos en '{p}'")
            print("Solo puedes editar archivos existentes (ej: marcar [x] en un plan).")
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
