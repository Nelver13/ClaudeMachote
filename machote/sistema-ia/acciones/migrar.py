#!/usr/bin/env python3
"""
migrar.py — Migra un proyecto con sistema IA viejo al nuevo.
Detecta archivos viejos, hace backup, instala estructura nueva.

Uso: python sistema-ia/acciones/migrar.py
"""
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parents[2]
BACKUP_DIR = ROOT / "sistema-ia" / "_backup_migracion"

# Archivos y carpetas del sistema VIEJO que ya no se usan
ARCHIVOS_VIEJOS = [
    "AGENT.md", "MAPA.md", "README.md",
    "estado.log", "ia_roles.json",
]
CARPETAS_VIEJAS = [
    "acciones", "benchmark", "discs", "logs", "backups",
    "machote-ia", "machote-ia-hooks",
]

# Archivos nuevos requeridos en raíz
ARCHIVOS_NUEVOS = [
    "INICIO.md", "AGENTS.md", "ESTADO.md",
    "CLAUDE.md", "KIMI.md", "CODEX.md", "GEMINI.md",
]


def backup_viejo():
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    backup = BACKUP_DIR / stamp
    backup.mkdir(parents=True, exist_ok=True)

    movidos = []
    for nombre in ARCHIVOS_VIEJOS:
        path = ROOT / nombre
        if path.exists():
            shutil.move(str(path), str(backup / nombre))
            movidos.append(nombre)

    for nombre in CARPETAS_VIEJAS:
        path = ROOT / nombre
        if path.exists():
            shutil.move(str(path), str(backup / nombre))
            movidos.append(nombre)

    return backup, movidos


def copiar_nuevos():
    src_dir = ROOT / "sistema-ia"
    copiados = []
    for nombre in ARCHIVOS_NUEVOS:
        src = src_dir / nombre
        dst = ROOT / nombre
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            copiados.append(nombre)
    return copiados


def verificar_gitignore():
    gitignore = ROOT / ".gitignore"
    entradas = ["sistema-ia/", "ESTADO.md", "INICIO.md", "AGENTS.md",
                "CLAUDE.md", "KIMI.md", "CODEX.md", "GEMINI.md"]
    existente = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    agregar = [e for e in entradas if e not in existente]
    if agregar:
        with gitignore.open("a", encoding="utf-8") as f:
            f.write("\n# Sistema IA local\n" + "\n".join(agregar) + "\n")
        return True
    return False


def main():
    print("=== Migración sistema IA ===")
    print(f"Proyecto: {ROOT.name}")
    print()

    # 1. Backup de lo viejo
    backup, movidos = backup_viejo()
    if movidos:
        print(f"Backup de {len(movidos)} archivos/carpetas viejos → {backup.name}/")
        for m in movidos:
            print(f"  - {m}")
    else:
        print("No se encontraron archivos viejos.")
    print()

    # 2. Copiar archivos nuevos a raíz
    copiados = copiar_nuevos()
    if copiados:
        print(f"Archivos nuevos copiados a raíz:")
        for c in copiados:
            print(f"  + {c}")
    print()

    # 3. Proteger gitignore
    if verificar_gitignore():
        print("OK: sistema-ia/ protegido en .gitignore")
    else:
        print("OK: .gitignore ya estaba configurado")

    print()
    print("Migración completa.")
    print("Próximo paso: abre el proyecto en Claude Code o pega PROMPT_INSTALAR.md en tu IA.")


if __name__ == "__main__":
    main()
