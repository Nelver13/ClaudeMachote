#!/usr/bin/env python3
"""
instalar.py — Instala el sistema multi-IA en un proyecto.
Los scripts ya viven en sistema-ia/acciones/ (directamente en git).
Este script solo crea: archivos raíz, carpetas, .claude/settings.json en raíz del proyecto.

Uso:
  python sistema-ia/machote/instalar.py            → instala en directorio actual
  python sistema-ia/machote/instalar.py /ruta/     → instala en ruta específica
"""
import sys
import shutil
import json
from pathlib import Path

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
    for c in ["planes", "discusiones", "memoria/sesiones", "handoff", "logs"]:
        (destino / "sistema-ia" / c).mkdir(parents=True, exist_ok=True)
    print("  OK: carpetas sistema-ia/")

    # 3. .claude/settings.json en raíz del PROYECTO (no en sistema-ia/)
    #    Los hooks usan rutas relativas a la raíz del proyecto.
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

    # 4. Scripts — ya están en sistema-ia/acciones/ (git los trae directamente)
    acciones_dir = destino / "sistema-ia" / "acciones"
    n_scripts = len(list(acciones_dir.glob("*.py"))) if acciones_dir.exists() else 0
    print(f"  OK: sistema-ia/acciones/ — {n_scripts} scripts (git-tracked)")

    # 5. VERSION
    version_src = MACHOTE_DIR.parent / "VERSION"
    version_dst = destino / "sistema-ia" / "VERSION"
    if version_src.exists() and not version_dst.exists():
        shutil.copy2(version_src, version_dst)
        print(f"  OK: sistema-ia/VERSION")

    print()
    print("Listo. Próximos pasos:")
    print("  1. Edita ESTADO.md → nombre del proyecto y roles")
    print("  2. Edita CLAUDE.md / KIMI.md etc. → reemplaza NOMBRE_PROYECTO")
    print("  3. Configura sistema-ia/acciones/credenciales.md (ntfy/webhook)")
    print("  4. Abre Claude Code — auto_setup.py carga el contexto solo")


def main():
    destino = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not destino.exists():
        print(f"ERROR: No existe {destino}")
        sys.exit(1)
    instalar(destino)


if __name__ == "__main__":
    main()
