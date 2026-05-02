#!/usr/bin/env python3
"""
actualizar.py — Actualiza sistema-ia en un proyecto existente desde el machote base.

Mantiene intactos: planes, discusiones, memoria, handoff, logs, complemento,
ESTADO.md e instrucciones por IA en la raíz.

Actualiza: scripts, skills, docs del sistema, VERSION.

Uso:
  # Desde el machote base
  python acciones/actualizar.py /ruta/al/proyecto

  # Desde dentro del proyecto (si sistema-ia/ es clone del machote)
  cd mi-proyecto
  python sistema-ia/acciones/actualizar.py

  # Ver qué haría sin ejecutar
  python acciones/actualizar.py /ruta/al/proyecto --dry-run
"""
import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# ── CONFIGURACIÓN ────────────────────────────────────────────────────────────

# Archivos y carpetas del sistema que se sincronizan desde el machote
SINCRONIZAR = [
    # (origen_relativo, destino_relativo, tipo)
    ("acciones", "sistema-ia/acciones", "dir"),
    ("acciones/app", "sistema-ia/app", "dir"),
    (".claude/skills", ".claude/skills", "dir"),
    ("sistema-ia/PROMPT_MAESTRO.md", "sistema-ia/PROMPT_MAESTRO.md", "file"),
    ("sistema-ia/ROADMAP.md", "sistema-ia/ROADMAP.md", "file"),
    ("sistema-ia/README.md", "sistema-ia/README.md", "file"),
    ("sistema-ia/PLANTILLA_OTROS_PROYECTOS.md", "sistema-ia/PLANTILLA_OTROS_PROYECTOS.md", "file"),
    ("VERSION", "sistema-ia/VERSION", "file"),
    ("CHANGELOG.md", "sistema-ia/CHANGELOG.md", "file"),
    ("instalar.py", "sistema-ia/instalar.py", "file"),
]

# Proyectados en el destino: NUNCA se tocan, ni siquiera en backup de reemplazo
PROTEGIDOS_DESTINO = {
    "sistema-ia/planes",
    "sistema-ia/discusiones",
    "sistema-ia/memoria",
    "sistema-ia/handoff",
    "sistema-ia/logs",
    "sistema-ia/complemento",
    "sistema-ia/_backup",
    "ESTADO.md",
    "INICIO.md",
    "AGENTS.md",
    "CLAUDE.md",
    "KIMI.md",
    "CODEX.md",
    "GEMINI.md",
    "RESUMEN.md",
}

# Carpetas vacías que deben existir
CARPETAS_OBLIGATORIAS = [
    "sistema-ia/planes",
    "sistema-ia/discusiones",
    "sistema-ia/discusiones/bugs",
    "sistema-ia/discusiones/bugs/screenshots",
    "sistema-ia/memoria",
    "sistema-ia/handoff",
    "sistema-ia/logs",
    "sistema-ia/complemento",
    "sistema-ia/complemento/investigaciones",
    "sistema-ia/complemento/guias",
    "sistema-ia/complemento/ideas",
    "sistema-ia/complemento/referencias",
    "sistema-ia/app",
]

# Archivos/carpetas obsoletas conocidas (pre-v2.0 y residuos de instalación)
OBSOLETOS = [
    "sistema-ia/AGENT.md",
    "sistema-ia/MAPA.md",
    "sistema-ia/estado.log",
    "sistema-ia/ia_roles.json",
    "sistema-ia/benchmark",
    "sistema-ia/discs",
    "sistema-ia/backups",
    "sistema-ia/machote-ia-hooks",
    "sistema-ia/.gitignore",
]

# Líneas mínimas para .gitignore del proyecto
GITIGNORE_LINEAS = [
    "# ── Sistema IA local — nunca sube (solo raíz) ────────────",
    "/sistema-ia/",
    "/ESTADO.md",
    "/INICIO.md",
    "/AGENTS.md",
    "/KIMI.md",
    "/CODEX.md",
    "/GEMINI.md",
    "/RESUMEN.md",
    "/CLAUDE.md",
    "/instalar.py",
]


# ── UTILIDADES ───────────────────────────────────────────────────────────────

def es_protegido(rel_path: str) -> bool:
    """Verifica si una ruta relativa está en la lista de protegidos."""
    rel_norm = rel_path.replace("\\", "/").rstrip("/")
    for prot in PROTEGIDOS_DESTINO:
        if rel_norm == prot or rel_norm.startswith(prot + "/"):
            return True
    return False


def version_de(path: Path) -> str:
    """Lee VERSION de un path, o 'desconocida'."""
    vf = path / "VERSION"
    if not vf.exists():
        vf = path / "sistema-ia" / "VERSION"
    if vf.exists():
        return vf.read_text(encoding="utf-8").strip()
    return "desconocida"


def detectar_origen_destino() -> tuple[Path, Path]:
    """
    Detecta origen (machote) y destino (proyecto) automáticamente.
    Estrategias:
      1. Si estamos en proyecto/sistema-ia/acciones/ → origen=../..  NO, origen=proyecto/sistema-ia/
      2. Si estamos en machote/acciones/ → origen=machote, destino=arg
    """
    script_dir = Path(__file__).parent.resolve()

    # Estrategia A: estamos dentro de un proyecto, en sistema-ia/acciones/
    # script_dir = .../proyecto/sistema-ia/acciones
    posible_sia = script_dir.parent          # .../proyecto/sistema-ia
    posible_destino = posible_sia.parent     # .../proyecto

    if (
        (posible_sia / "VERSION").exists()
        and (posible_destino / "ESTADO.md").exists()
        and (posible_destino / "sistema-ia").exists()
    ):
        return posible_sia, posible_destino

    # Estrategia B: estamos en machote/acciones/ o sistema-ia-temp/acciones/
    posible_origen = script_dir.parent       # .../machote
    if (
        (posible_origen / "VERSION").exists()
        and (posible_origen / "instalar.py").exists()
    ):
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
            destino = Path(sys.argv[1]).resolve()
            return posible_origen, destino
        # Auto-detectar proyecto subiendo directorios buscando ESTADO.md
        destino = _buscar_proyecto_cercano(script_dir)
        if destino:
            return posible_origen, destino
        print("ERROR: Ejecutando desde el machote base. No se detectó proyecto cercano.")
        print(f"  Pasa la ruta explícita: python {sys.argv[0]} /ruta/al/proyecto")
        sys.exit(1)

    # Estrategia C: estamos en machote/sistema-ia/acciones/ (modo meta-recursivo)
    posible_destino_meta = script_dir.parents[2]   # .../machote
    posible_origen_meta = script_dir.parents[1]    # .../machote/sistema-ia
    if (
        (posible_destino_meta / "VERSION").exists()
        and (posible_origen_meta / "PROMPT_MAESTRO.md").exists()
    ):
        return posible_origen_meta, posible_destino_meta

    return None, None


def _buscar_proyecto_cercano(desde: Path) -> Path | None:
    """Sube hasta 4 niveles buscando ESTADO.md."""
    actual = desde
    for _ in range(4):
        actual = actual.parent
        if (actual / "ESTADO.md").exists():
            return actual
    return None


def validar_origen(origen: Path) -> bool:
    """Valida que el origen parezca ser el machote base."""
    checks = [
        (origen / "VERSION").exists(),
        (origen / "instalar.py").exists()
        or (origen / "PROMPT_MAESTRO.md").exists()
        or (origen / "sistema-ia" / "PROMPT_MAESTRO.md").exists(),
    ]
    if not all(checks):
        print(f"ERROR: El origen no parece ser el machote base: {origen}")
        print("  Debe contener VERSION y (instalar.py o sistema-ia/PROMPT_MAESTRO.md)")
        return False
    return True


def validar_destino(destino: Path) -> bool:
    """Valida que el destino sea un proyecto con sistema-ia instalado."""
    sia = destino / "sistema-ia"
    if not sia.exists():
        print(f"ERROR: No existe sistema-ia/ en el destino: {destino}")
        print("  Ejecuta primero: python instalar.py")
        return False

    # Al menos debe tener ESTADO.md o alguna carpeta de trabajo
    tiene_trabajo = (
        (destino / "ESTADO.md").exists()
        or (sia / "planes").exists()
        or (sia / "discusiones").exists()
        or (sia / "memoria").exists()
    )
    if not tiene_trabajo:
        print(f"AVISO: El destino no tiene ESTADO.md ni trabajo previo detectado.")
        resp = input("¿Continuar de todos modos? [s/N]: ").strip().lower()
        if resp != "s":
            return False
    return True


def crear_backup(destino: Path) -> Path:
    """Crea backup de sistema-ia/ completo antes de tocar nada."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bk = destino / "sistema-ia" / f"_backup_actualizacion_{stamp}"
    sia = destino / "sistema-ia"
    bk.mkdir(parents=True, exist_ok=True)

    # Copiar TODO excepto backups anteriores
    for item in sia.iterdir():
        if item.name.startswith("_backup"):
            continue
        dest = bk / item.name
        if item.is_dir():
            shutil.copytree(item, dest, ignore=shutil.ignore_patterns("_backup*"))
        else:
            shutil.copy2(item, dest)

    return bk


def _resolver_src(origen: Path, src_rel: str) -> Path | None:
    """Busca el archivo origen probando rutas alternativas."""
    candidatos = [origen / src_rel]
    if src_rel.startswith("sistema-ia/"):
        candidatos.append(origen / src_rel[len("sistema-ia/"):])
    else:
        candidatos.append(origen / "sistema-ia" / src_rel)
    for c in candidatos:
        if c.exists():
            return c
    return None


def sincronizar(origen: Path, destino: Path, dry_run: bool) -> dict:
    """Sincroniza archivos del sistema desde origen a destino."""
    reporte = {"copiados": [], "omitidos": [], "creados": [], "obsoletos": [], "advertencias": []}

    for src_rel, dst_rel, tipo in SINCRONIZAR:
        src = _resolver_src(origen, src_rel)
        dst = destino / dst_rel

        if src is None:
            reporte["omitidos"].append(f"{src_rel} (no existe en origen)")
            continue

        # Evitar copiar sobre si mismo
        if src.resolve() == dst.resolve():
            continue

        # Verificar que no vayamos a escribir en algo protegido
        if es_protegido(dst_rel):
            reporte["omitidos"].append(f"{dst_rel} (protegido)")
            continue

        if dry_run:
            reporte["copiados"].append(f"{src_rel} -> {dst_rel}")
            continue

        # Backup del destino si existe
        if dst.exists():
            backup_dir = destino / "sistema-ia" / "_backup_reemplazados"
            backup_dir.mkdir(exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            suffix = f"_{stamp}"
            if dst.is_dir():
                shutil.copytree(dst, backup_dir / (dst.name + suffix), dirs_exist_ok=True)
            else:
                shutil.copy2(dst, backup_dir / (dst.name + suffix))

        # Copiar
        if tipo == "dir":
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            reporte["copiados"].append(f"{src_rel}/ -> {dst_rel}/")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            reporte["copiados"].append(f"{src_rel} -> {dst_rel}")

    # Crear carpetas obligatorias faltantes
    for carpeta in CARPETAS_OBLIGATORIAS:
        c = destino / carpeta
        if not c.exists():
            if not dry_run:
                c.mkdir(parents=True, exist_ok=True)
                gitkeep = c / ".gitkeep"
                if not gitkeep.exists():
                    gitkeep.touch()
            reporte["creados"].append(carpeta)

    # Detectar obsoletos
    for obs in OBSOLETOS:
        p = destino / obs
        if p.exists():
            reporte["obsoletos"].append(obs)
            if not dry_run:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()

    # Detectar instalación recursiva (sistema-ia/sistema-ia/)
    recursivo = destino / "sistema-ia" / "sistema-ia"
    if recursivo.exists():
        reporte["advertencias"].append(
            f"INSTALACIÓN RECURSIVA DETECTADA: {recursivo}\n"
            "  Esto ocurre cuando se clona el machote completo sin limpiar.\n"
            "  Revisa si contiene trabajo del proyecto antes de borrarlo manualmente."
        )

    # Detectar .git anidado y borrarlo
    git_anidado = destino / "sistema-ia" / ".git"
    if git_anidado.exists():
        try:
            shutil.rmtree(git_anidado)
            reporte["creados"].append("sistema-ia/.git/ eliminado (repo anidado)")
        except Exception as e:
            reporte["advertencias"].append(
                f"No se pudo borrar {git_anidado}: {e}\n"
                "  Eliminálo manualmente para evitar problemas con git status."
            )

    # Borrar machote/ residuo si existe
    machote_residuo = destino / "sistema-ia" / "machote"
    if machote_residuo.exists():
        try:
            shutil.rmtree(machote_residuo)
            reporte["creados"].append("sistema-ia/machote/ eliminado (residuo)")
        except Exception as e:
            reporte["advertencias"].append(f"No se pudo borrar {machote_residuo}: {e}")

    return reporte


def actualizar_gitignore(destino: Path, dry_run: bool):
    """Asegura que .gitignore tenga las líneas mínimas del sistema IA."""
    gi = destino / ".gitignore"
    existente = gi.read_text(encoding="utf-8") if gi.exists() else ""
    faltantes = [l for l in GITIGNORE_LINEAS if l not in existente]

    if not faltantes:
        return False

    if dry_run:
        return True

    with gi.open("a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(faltantes) + "\n")
    return True


def mostrar_reporte(reporte: dict, bk: Path | None, destino: Path, v_origen: str, v_destino: str, dry_run: bool):
    """Muestra el resumen de la operación."""
    modo = "[DRY-RUN] " if dry_run else ""
    print(f"\n{'='*60}")
    print(f"{modo}ACTUALIZACIÓN SISTEMA-IA COMPLETADA")
    print(f"{'='*60}")
    print(f"Origen (machote):  v{v_origen}")
    print(f"Destino (proyecto): v{v_destino}")
    print(f"Proyecto: {destino.name}")
    if bk:
        print(f"Backup completo: {bk}")
    print()

    if reporte["copiados"]:
        print(f"Archivos sincronizados ({len(reporte['copiados'])}):")
        for c in reporte["copiados"]:
            print(f"  [OK] {c}")
    if reporte["creados"]:
        print(f"Carpetas creadas ({len(reporte['creados'])}):")
        for c in reporte["creados"]:
            print(f"  [+] {c}")
    if reporte["omitidos"]:
        print(f"Omitidos ({len(reporte['omitidos'])}):")
        for o in reporte["omitidos"]:
            print(f"  [SKIP] {o}")
    if reporte["obsoletos"]:
        print(f"Obsoletos eliminados ({len(reporte['obsoletos'])}):")
        for o in reporte["obsoletos"]:
            print(f"  [DEL] {o}")
    if reporte["advertencias"]:
        print(f"\n[WARN] ADVERTENCIAS ({len(reporte['advertencias'])}):")
        for a in reporte["advertencias"]:
            print(f"  [!] {a}")

    print(f"\n{'='*60}")
    if dry_run:
        print("Esto fue un simulacro. Ejecuta sin --dry-run para aplicar.")
    else:
        print("Listo. Revisa los cambios y prueba el sistema.")
    print(f"{'='*60}")


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Actualiza sistema-ia desde el machote base manteniendo trabajo del proyecto."
    )
    parser.add_argument(
        "destino",
        nargs="?",
        default=None,
        help="Ruta al proyecto destino (default: auto-detectar)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra qué haría sin modificar nada",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Omite el backup completo de sistema-ia/",
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Fuerza actualización incluso si las versiones son iguales",
    )
    parser.add_argument(
        "--origen",
        default=None,
        help="Ruta al machote base (default: auto-detectar)",
    )
    args = parser.parse_args()

    # Detectar paths
    if args.origen:
        origen = Path(args.origen).resolve()
        destino = Path(args.destino).resolve() if args.destino else Path.cwd().resolve()
    else:
        auto_origen, auto_destino = detectar_origen_destino()
        if auto_origen is None:
            print("ERROR: No se pudo detectar origen ni destino automáticamente.")
            print("Uso explícito:")
            print(f"  python {sys.argv[0]} /ruta/proyecto")
            print(f"  python {sys.argv[0]} /ruta/proyecto --origen /ruta/machote")
            sys.exit(1)
        origen = auto_origen
        destino = auto_destino if args.destino is None else Path(args.destino).resolve()

    print(f"Origen:  {origen}")
    print(f"Destino: {destino}")

    if not validar_origen(origen):
        sys.exit(1)
    if not validar_destino(destino):
        sys.exit(1)

    v_origen = version_de(origen)
    v_destino = version_de(destino)

    print(f"\nVersión machote:  {v_origen}")
    print(f"Versión proyecto: {v_destino}")

    if v_origen == v_destino and not args.dry_run and not args.force:
        try:
            resp = input("Ambas versiones son iguales. ¿Forzar actualizacion? [s/N]: ").strip().lower()
        except EOFError:
            print("Modo no interactivo detectado. Usa --force para forzar la actualizacion.")
            sys.exit(0)
        if resp != "s":
            print("Cancelado.")
            sys.exit(0)

    # Backup
    bk = None
    if not args.no_backup and not args.dry_run:
        print("\nCreando backup...")
        bk = crear_backup(destino)
        print(f"Backup: {bk}")

    # Sincronizar
    print("\nSincronizando archivos del sistema...")
    reporte = sincronizar(origen, destino, args.dry_run)

    # Gitignore
    gitignore_ok = actualizar_gitignore(destino, args.dry_run)
    if gitignore_ok:
        reporte["creados"].append(".gitignore (líneas de sistema-ia agregadas)")

    # Verificar estructura completa post-actualización
    if not args.dry_run:
        verificar_estructura_bugs(destino)
        verificar_archivos_raiz(destino)
        instalar_dependencias()
        mostrar_guia(destino)

    # Reporte final
    mostrar_reporte(reporte, bk, destino, v_origen, v_destino, args.dry_run)


# ── POST-ACTUALIZACIÓN AUTOMÁTICA ────────────────────────────────────────────

def verificar_estructura_bugs(destino: Path):
    bugs_dir = destino / "sistema-ia" / "discusiones" / "bugs"
    bugs_dir.mkdir(parents=True, exist_ok=True)
    backlog = bugs_dir / "backlog.md"
    if not backlog.exists():
        backlog.write_text("""# Bugs Reportados

> Usa Alt+R para reportar bugs con screenshot y descripción.
> Los bugs se agregan automáticamente aquí.

""", encoding="utf-8")
        print("  OK: bugs/backlog.md creado")
    (bugs_dir / "screenshots").mkdir(parents=True, exist_ok=True)


def verificar_archivos_raiz(destino: Path):
    templates = {
        "INICIO.md": "# {proyecto}\n\n[Descripción, stack, arquitectura]\n\n## Cómo empezar\nLee: AGENTS.md → ESTADO.md → sistema-ia/PROMPT_MAESTRO.md\n",
        "AGENTS.md": "# Reglas para todas las IAs\n\n[Reglas universales del proyecto]\n\nLee: sistema-ia/PROMPT_MAESTRO.md para la estructura de trabajo.\n",
        "ESTADO.md": "[PROJ: {proyecto}]\n[STACK: ]\n[DESC: ]\n\n[ROL_CLAUDE: ARQUITECTO]\n[ROL_KIMI: DESARROLLADOR]\n[ROL_CODEX: DESARROLLADOR]\n[ROL_GEMINI: DESARROLLADOR]\n\n[MODULO: ]\n[PLAN: ]\n[ESTADO_PLAN: ]\n[TAREA_ACTUAL: ]\n[TOTAL_TAREAS: ]\n[PROGRESO: 0%]\n[LAST_TASK: ]\n[NEXT_TASK: ]\n[CHECKPOINT: ]\n[LAST_AVISO: ]\n\n[HISTORIAL_PLANES:]\n",
        "CLAUDE.md": "# Claude — Instrucciones\n\n[Comportamiento esperado de Claude en este proyecto]\n\nLee primero: INICIO.md → AGENTS.md → sistema-ia/PROMPT_MAESTRO.md\n",
        "KIMI.md": "# Kimi — Instrucciones\n\n[Comportamiento esperado de Kimi en este proyecto]\n\nLee primero: INICIO.md → AGENTS.md → sistema-ia/PROMPT_MAESTRO.md\n",
        "CODEX.md": "# Codex — Instrucciones\n\n[Comportamiento esperado de Codex en este proyecto]\n\nLee primero: INICIO.md → AGENTS.md → sistema-ia/PROMPT_MAESTRO.md\n",
        "GEMINI.md": "# Gemini — Instrucciones\n\n[Comportamiento esperado de Gemini en este proyecto]\n\nLee primero: INICIO.md → AGENTS.md → sistema-ia/PROMPT_MAESTRO.md\n",
    }
    nombre = destino.name
    for archivo, contenido in templates.items():
        p = destino / archivo
        if not p.exists():
            p.write_text(contenido.replace("{proyecto}", nombre), encoding="utf-8")
            print(f"  OK: {archivo} creado (template)")


def instalar_dependencias():
    print("\nVerificando dependencias del bug reporter...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "Pillow", "pynput",
             "SpeechRecognition", "pyaudio", "--quiet"],
            check=True, timeout=120
        )
        print("  OK: Dependencias instaladas/verificadas")
    except Exception as e:
        print(f"  WARN: No se pudieron instalar dependencias: {e}")


def mostrar_guia(destino: Path):
    guia = destino / "sistema-ia" / "acciones" / "guia.py"
    if guia.exists():
        try:
            subprocess.run([sys.executable, str(guia)], check=False)
        except Exception:
            pass


if __name__ == "__main__":
    main()
