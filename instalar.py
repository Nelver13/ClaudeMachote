#!/usr/bin/env python3
"""
instalar.py — Configura el sistema multi-IA en este proyecto.
Ejecuta esto después de clonar si no usas Claude Code.

Uso: python instalar.py
"""
from pathlib import Path

ROOT = Path(__file__).parent


def proteger_gitignore():
    gitignore = ROOT / ".gitignore"
    lineas = [
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
    agregar = [l for l in lineas if l not in existente]
    if agregar:
        with gitignore.open("a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(agregar) + "\n")
        print("OK: sistema-ia/ protegido en .gitignore")


def main():
    proteger_gitignore()
    # Crear carpetas vacías si no existen
    carpetas = [
        "sistema-ia/planes",
        "sistema-ia/discusiones",
        "sistema-ia/memoria/sesiones",
        "sistema-ia/handoff",
        "sistema-ia/logs",
    ]
    for c in carpetas:
        (ROOT / c).mkdir(parents=True, exist_ok=True)
        gitkeep = ROOT / c / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()

    print("OK: carpetas creadas.")
    print()
    print("Próximos pasos:")
    print("  1. Edita ESTADO.md → reemplaza NOMBRE_PROYECTO y ajusta roles")
    print("  2. Edita CLAUDE.md/KIMI.md/etc → reemplaza NOMBRE_PROYECTO")
    print("  3. Configura sistema-ia/acciones/credenciales.md")
    print("  4. Abre en Claude Code → arranca solo")


if __name__ == "__main__":
    main()
