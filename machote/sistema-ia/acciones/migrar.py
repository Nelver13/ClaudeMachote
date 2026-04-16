#!/usr/bin/env python3
"""
migrar.py — Actualiza sistema IA a la versión más reciente.
Detecta versión actual y actualiza SOLO scripts/skills.
NUNCA toca: planes/, discusiones/, memoria/, ESTADO.md — trabajo activo intacto.

Uso: python sistema-ia/acciones/migrar.py
"""
import shutil
from pathlib import Path
from datetime import datetime

ROOT       = Path(__file__).parents[2]   # acciones → sistema-ia → raíz
SIA        = ROOT / "sistema-ia"
BACKUP_DIR = SIA / "_backup_migracion"
VERSION_FILE = SIA / "VERSION"

# Scripts que SE ACTUALIZAN siempre (sobrescriben)
SCRIPTS_ACTUALIZAR = [
    "avisar.py",
    "cambiar_rol.py",
    "cerrar_sesion.py",
    "comprimir_discusion.py",
    "finalizar_discusion.py",
    "finalizar_plan.py",
    "check_role.py",
    "completar_tarea.py",
    "actualizar_mapa.py",
    "actualizar_checklist.py",
    "auto_setup.py",
    "migrar.py",
]

# Skills que SE ACTUALIZAN siempre
SKILLS_ACTUALIZAR = [
    ".claude/skills/modo-dev/SKILL.md",
    ".claude/skills/modo-arquitecto/SKILL.md",
    ".claude/skills/caveman/SKILL.md",
]

# Settings que SE ACTUALIZA (merge seguro)
SETTINGS = ".claude/settings.json"

# Archivos viejos de sistema pre-v2.0
ARCHIVOS_VIEJOS = ["AGENT.md", "MAPA.md", "estado.log", "ia_roles.json"]
CARPETAS_VIEJAS = ["acciones", "benchmark", "discs", "logs", "backups", "machote-ia-hooks"]

# NUNCA tocar
PROTEGIDOS = ["planes", "discusiones", "memoria", "handoff", "ESTADO.md"]


def version_actual() -> str:
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    # Detectar v2.0 por estructura
    if (SIA / "acciones").exists():
        return "2.0"
    return "1.x"


def version_nueva() -> str:
    src = Path(__file__).parent / ".." / ".." / "VERSION"
    if src.exists():
        return src.read_text(encoding="utf-8").strip()
    return "2.1"


def backup(archivos: list, tag: str):
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    dest = BACKUP_DIR / f"{stamp}_{tag}"
    dest.mkdir(parents=True, exist_ok=True)
    for p in archivos:
        if p.exists():
            shutil.copy2(str(p), str(dest / p.name))


def limpiar_viejos():
    movidos = []
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    bk = BACKUP_DIR / f"{stamp}_pre2"
    for nombre in ARCHIVOS_VIEJOS:
        p = ROOT / nombre
        if p.exists():
            bk.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(bk / nombre))
            movidos.append(nombre)
    for nombre in CARPETAS_VIEJAS:
        p = ROOT / nombre
        if p.exists():
            bk.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(bk / nombre))
            movidos.append(nombre)
    return movidos


def actualizar_scripts():
    src_acciones = Path(__file__).parent  # la carpeta acciones del machote clonado
    dst_acciones = SIA / "acciones"
    dst_acciones.mkdir(parents=True, exist_ok=True)

    actualizados = []
    for nombre in SCRIPTS_ACTUALIZAR:
        src = src_acciones / nombre
        dst = dst_acciones / nombre
        if src.exists():
            # Backup del viejo antes de sobrescribir
            if dst.exists():
                backup([dst], "scripts")
            shutil.copy2(str(src), str(dst))
            actualizados.append(nombre)
    return actualizados


def actualizar_skills():
    src_base = Path(__file__).parents[1]  # sistema-ia/ del machote
    dst_base = SIA
    actualizados = []

    for skill_path in SKILLS_ACTUALIZAR:
        src = src_base / skill_path
        dst = dst_base / skill_path
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                backup([dst], "skills")
            shutil.copy2(str(src), str(dst))
            actualizados.append(skill_path)
    return actualizados


def actualizar_version(nueva: str):
    VERSION_FILE.write_text(nueva + "\n", encoding="utf-8")


def main():
    v_actual = version_actual()
    v_nueva  = version_nueva()

    print(f"=== Migración sistema IA {v_actual} → {v_nueva} ===")
    print(f"Proyecto: {ROOT.name}")
    print()

    if v_actual == v_nueva:
        print(f"Ya en v{v_nueva}. Nada que hacer.")
        return

    # 1. Limpiar archivos pre-v2.0 si existen
    viejos = limpiar_viejos()
    if viejos:
        print(f"Archivos pre-v2.0 movidos a backup: {', '.join(viejos)}")

    # 2. Actualizar scripts
    scripts = actualizar_scripts()
    print(f"Scripts actualizados ({len(scripts)}): {', '.join(scripts)}")

    # 3. Actualizar skills
    skills = actualizar_skills()
    print(f"Skills actualizados ({len(skills)}): {', '.join(skills)}")

    # 4. Crear carpetas faltantes (sin tocar existentes)
    for carpeta in ["planes", "discusiones", "memoria/sesiones", "handoff", "logs"]:
        p = SIA / carpeta
        p.mkdir(parents=True, exist_ok=True)

    # 5. Actualizar VERSION
    actualizar_version(v_nueva)
    print(f"\nVersión actualizada: {v_actual} → {v_nueva}")

    print()
    print("INTACTO (trabajo activo no tocado):")
    for p in PROTEGIDOS:
        estado = "existe" if (SIA / p).exists() or (ROOT / p).exists() else "no existe"
        print(f"  {p}: {estado}")

    print()
    print(f"Migración completa. Sistema en v{v_nueva}.")
    print("Backups en: sistema-ia/_backup_migracion/")


if __name__ == "__main__":
    main()
