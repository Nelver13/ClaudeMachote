#!/usr/bin/env python3
"""
migrar.py — Actualiza sistema IA a la versión más reciente.
- Actualiza scripts/skills existentes (sobrescribe con backup).
- REPLENECE scripts/skills faltantes (caso: clon incompleto).
- NUNCA toca: planes/, discusiones/, memoria/, handoff/, ESTADO.md.

Uso: python sistema-ia/acciones/migrar.py
"""
import shutil
from pathlib import Path
from datetime import datetime

ROOT       = Path(__file__).parents[2]   # acciones → sistema-ia → raíz
SIA        = ROOT / "sistema-ia"
BACKUP_DIR = SIA / "_backup_migracion"
VERSION_FILE = SIA / "VERSION"

# Scripts que SE ACTUALIZAN / REPLENECEN
SCRIPTS_ACTUALIZAR = [
    "avisar.py",
    "cambiar_rol.py",
    "cerrar_sesion.py",
    "comprimir_discusion.py",
    "finalizar_discusion.py",
    "finalizar_plan.py",
    "check_role.py",
    "check_secrets.py",
    "completar_tarea.py",
    "auto_setup.py",
    "migrar.py",
]

# Assets auxiliares (mp3 + credenciales)
ASSETS_ACTUALIZAR = [
    "aviso_suave.mp3",
    "aviso_normal.mp3",
    "aviso_urgente.mp3",
    "credenciales.md",
]

# Skills que SE ACTUALIZAN / REPLENECEN
SKILLS_ACTUALIZAR = [
    ".claude/skills/modo-dev/SKILL.md",
    ".claude/skills/modo-arquitecto/SKILL.md",
    ".claude/skills/caveman/SKILL.md",
]

SETTINGS = ".claude/settings.json"

# Archivos viejos pre-v2.0
ARCHIVOS_VIEJOS = ["AGENT.md", "MAPA.md", "estado.log", "ia_roles.json"]
CARPETAS_VIEJAS = ["acciones", "benchmark", "discs", "backups", "machote-ia-hooks"]

# NUNCA tocar
PROTEGIDOS = ["planes", "discusiones", "memoria", "handoff", "ESTADO.md"]


def version_actual() -> str:
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    if (SIA / "acciones").exists():
        return "2.0"
    return "1.x"


def version_nueva() -> str:
    # El machote clonado trae VERSION en su raíz
    src = Path(__file__).parents[1] / "VERSION"  # sistema-ia/VERSION del clon
    if src.exists():
        return src.read_text(encoding="utf-8").strip()
    return "2.3"


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


ESTE_SCRIPT = Path(__file__).resolve()

def sincronizar_archivos(src_dir: Path, dst_dir: Path, nombres: list, tag: str):
    """
    Copia cada nombre de src_dir → dst_dir. Si dst existe, backup + sobrescribe.
    Si dst no existe, lo replenece. Devuelve (actualizados, replenecidos).
    Salta migrar.py si coincide con el script en ejecución (no se puede sobreescribir en Windows).
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    actualizados = []
    replenecidos = []
    for nombre in nombres:
        src = src_dir / nombre
        dst = dst_dir / nombre
        # No sobreescribir el script que está corriendo ahora mismo
        if dst.resolve() == ESTE_SCRIPT:
            print(f"  [skip] {nombre} — en uso, actualízalo manualmente si cambia")
            continue
        if not src.exists():
            continue
        if dst.exists():
            backup([dst], tag)
            shutil.copy2(str(src), str(dst))
            actualizados.append(nombre)
        else:
            shutil.copy2(str(src), str(dst))
            replenecidos.append(nombre)
    return actualizados, replenecidos


def actualizar_scripts_y_assets():
    src = Path(__file__).parent  # acciones/ del machote clonado
    dst = SIA / "acciones"
    act1, rep1 = sincronizar_archivos(src, dst, SCRIPTS_ACTUALIZAR, "scripts")
    act2, rep2 = sincronizar_archivos(src, dst, ASSETS_ACTUALIZAR, "assets")
    return act1 + act2, rep1 + rep2


def actualizar_skills():
    src_base = Path(__file__).parents[1]  # sistema-ia/ del machote clonado
    dst_base = SIA
    actualizados = []
    replenecidos = []

    for skill_path in SKILLS_ACTUALIZAR:
        src = src_base / skill_path
        dst = dst_base / skill_path
        if not src.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            backup([dst], "skills")
            shutil.copy2(str(src), str(dst))
            actualizados.append(skill_path)
        else:
            shutil.copy2(str(src), str(dst))
            replenecidos.append(skill_path)
    return actualizados, replenecidos


def actualizar_version(nueva: str):
    VERSION_FILE.write_text(nueva + "\n", encoding="utf-8")


def configurar_gitignore():
    gitignore_dst = ROOT / ".gitignore"
    gitignore_rules = """
# ── Sistema IA (Generado) ───────────────────────────────
# Ocultar scripts y memoria, pero mantener discusiones y planes para el equipo
sistema-ia/*
!sistema-ia/discusiones/
!sistema-ia/planes/

# Archivos de la IA locales (ESTADO.md sí sube a git)
INICIO.md
AGENTS.md
CLAUDE.md
KIMI.md
CODEX.md
GEMINI.md
RESUMEN.md
instalar.py
"""
    validar_y_reemplazar = False
    
    if not gitignore_dst.exists():
        gitignore_dst.write_text(gitignore_rules, encoding="utf-8")
        print("Reglas del sistema IA agregadas al .gitignore original.")
    else:
        current_gitignore = gitignore_dst.read_text(encoding="utf-8")
        if "sistema-ia" not in current_gitignore or "ESTADO.md" in current_gitignore:
            # Si tiene las reglas viejas (que ignoran ESTADO.md) limpiamos o las anexamos. 
            # De forma sencilla las adjuntamos al final, pero si el usuario usaba la version anterior
            # ESTADO.md estaba ignorado (INICIO.md, AGENTS.md, ESTADO.md). 
            # Para no destruir su archivo vamos a simplemente re-agregar las reglas o quitar "ESTADO.md"
            nuevo_gitignore = current_gitignore.replace("ESTADO.md\n", "")
            if "\n!sistema-ia/discusiones/" not in nuevo_gitignore:
                nuevo_gitignore += "\n" + gitignore_rules

            with open(gitignore_dst, "w", encoding="utf-8") as f:
                f.write(nuevo_gitignore)
            print("Reglas del sistema IA actualizadas en el .gitignore del proyecto.")
        else:
            pass


def main():
    v_actual = version_actual()
    v_nueva  = version_nueva()

    print(f"=== Migración sistema IA {v_actual} → {v_nueva} ===")
    print(f"Proyecto: {ROOT.name}")
    print()

    # 1. Limpiar archivos pre-v2.0
    viejos = limpiar_viejos()
    if viejos:
        print(f"Archivos pre-v2.0 movidos a backup: {', '.join(viejos)}")

    # 2. Scripts + assets (actualiza + replenece)
    act_scripts, rep_scripts = actualizar_scripts_y_assets()
    if act_scripts:
        print(f"Scripts/assets actualizados ({len(act_scripts)}): {', '.join(act_scripts)}")
    if rep_scripts:
        print(f"Scripts/assets REPLENECIDOS ({len(rep_scripts)}): {', '.join(rep_scripts)}")

    # 3. Skills (actualiza + replenece)
    act_skills, rep_skills = actualizar_skills()
    if act_skills:
        print(f"Skills actualizados ({len(act_skills)}): {', '.join(act_skills)}")
    if rep_skills:
        print(f"Skills REPLENECIDOS ({len(rep_skills)}): {', '.join(rep_skills)}")

    # 4. Crear carpetas faltantes
    for carpeta in ["planes", "discusiones", "memoria/sesiones", "handoff", "logs"]:
        p = SIA / carpeta
        p.mkdir(parents=True, exist_ok=True)

    # 5. Actualizar .gitignore
    configurar_gitignore()

    # 5. VERSION
    if v_actual != v_nueva:
        actualizar_version(v_nueva)
        print(f"\nVersión actualizada: {v_actual} → {v_nueva}")
    else:
        # Forzar la escritura si falta (ej. proyecto sin VERSION)
        if not VERSION_FILE.exists():
            actualizar_version(v_nueva)
        print(f"\nVersión local: v{v_nueva}")

    print()
    print("INTACTO (trabajo activo no tocado):")
    for p in PROTEGIDOS:
        estado = "existe" if (SIA / p).exists() or (ROOT / p).exists() else "no existe"
        print(f"  {p}: {estado}")

    print()
    if not (act_scripts or rep_scripts or act_skills or rep_skills) and v_actual == v_nueva:
        print(f"Ya en v{v_nueva} y completo. Nada que hacer.")
    else:
        print(f"Migración completa. Sistema en v{v_nueva}.")
        if BACKUP_DIR.exists():
            print(f"Backups en: {BACKUP_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
