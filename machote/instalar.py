#!/usr/bin/env python3
"""
instalar.py — Instala el sistema multi-IA en un proyecto.
Copia todos los archivos del machote al proyecto destino.

Uso:
  python instalar.py                        → instala en directorio actual
  python instalar.py /ruta/a/mi-proyecto    → instala en ruta específica
"""
import sys
import shutil
from pathlib import Path

MACHOTE_DIR = Path(__file__).parent
ACCIONES_SRC = MACHOTE_DIR.parent / "sistema-ia" / ".claude" / "ia" / "acciones"
SKILLS_SRC   = MACHOTE_DIR.parent / "sistema-ia" / ".claude" / "skills"


def instalar(destino: Path):
    print(f"Instalando sistema-ia en: {destino}")
    print()

    # 1. Archivos raíz
    raiz_files = ["INICIO.md", "AGENTS.md", "ESTADO.md",
                  "CLAUDE.md", "KIMI.md", "CODEX.md", "GEMINI.md"]
    for f in raiz_files:
        src = MACHOTE_DIR / f
        dst = destino / f
        if dst.exists():
            print(f"  SKIP (existe): {f}")
        else:
            shutil.copy2(src, dst)
            print(f"  OK: {f}")

    # 2. estructura sistema-ia/
    carpetas = ["planes", "discusiones", "memoria", "handoff", "acciones"]
    for c in carpetas:
        (destino / "sistema-ia" / c).mkdir(parents=True, exist_ok=True)

    # 3. Copiar acciones (scripts)
    if ACCIONES_SRC.exists():
        for script in ACCIONES_SRC.iterdir():
            dst = destino / "sistema-ia" / "acciones" / script.name
            if not dst.exists():
                shutil.copy2(script, dst)
                print(f"  OK: sistema-ia/acciones/{script.name}")
    else:
        print("  AVISO: No se encontró carpeta de acciones en el machote.")

    # 4. .claude/settings.json
    claude_dir = destino / "sistema-ia" / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    settings_src = MACHOTE_DIR / "sistema-ia" / ".claude" / "settings.json"
    settings_dst = claude_dir / "settings.json"
    if not settings_dst.exists():
        shutil.copy2(settings_src, settings_dst)
        print(f"  OK: sistema-ia/.claude/settings.json")

    # 5. Skills
    if SKILLS_SRC.exists():
        skills_dst = claude_dir / "skills"
        if not skills_dst.exists():
            shutil.copytree(SKILLS_SRC, skills_dst)
            print(f"  OK: sistema-ia/.claude/skills/")
    else:
        print("  AVISO: No se encontró carpeta de skills.")

    print()
    print("Listo. Próximos pasos:")
    print("  1. Edita ESTADO.md → pon nombre del proyecto y roles de IAs")
    print("  2. Edita CLAUDE.md / KIMI.md etc. → reemplaza NOMBRE_PROYECTO")
    print("  3. Pega INICIO.md en la IA que vas a usar")
    print("  4. Configura credenciales en sistema-ia/acciones/credenciales.md")


def main():
    destino = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not destino.exists():
        print(f"ERROR: No existe {destino}")
        sys.exit(1)
    instalar(destino)


if __name__ == "__main__":
    main()
