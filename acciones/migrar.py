#!/usr/bin/env python3
"""
migrar.py — Desde v2.4 los scripts están en git (acciones/ en la raíz del repo).
git pull en sistema-ia/ los actualiza directamente — no se copian.

Este script solo: crea carpetas faltantes, limpia pre-v2.0, confirma estado.

Uso: python sistema-ia/acciones/migrar.py
"""
import shutil
from pathlib import Path
from datetime import datetime


def _encontrar_raiz() -> Path:
    actual = Path(__file__).parent.resolve()
    for _ in range(6):
        if (actual / 'ESTADO.md').exists():
            return actual
        if actual.parent == actual:
            break
        actual = actual.parent
    return Path(__file__).parents[2]


ROOT = _encontrar_raiz()
SIA  = ROOT / "sistema-ia"
BACKUP_DIR   = SIA / "_backup_migracion"
VERSION_FILE = SIA / "VERSION"

ARCHIVOS_VIEJOS = ["AGENT.md", "MAPA.md", "estado.log", "ia_roles.json"]
CARPETAS_VIEJAS = ["benchmark", "discs", "backups", "machote-ia-hooks"]
PROTEGIDOS = ["planes", "discusiones", "memoria", "handoff", "ESTADO.md"]


def version_actual() -> str:
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    return "desconocida"


def limpiar_viejos():
    movidos = []
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    bk = BACKUP_DIR / f"{stamp}_pre2"
    for nombre in ARCHIVOS_VIEJOS + CARPETAS_VIEJAS:
        p = ROOT / nombre
        if p.exists():
            bk.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(bk / nombre))
            movidos.append(nombre)
    return movidos


def main():
    v = version_actual()
    print(f"=== Sistema IA v{v} — verificación ===")
    print(f"Proyecto: {ROOT.name}")
    print()

    viejos = limpiar_viejos()
    if viejos:
        print(f"Pre-v2.0 movidos a backup: {', '.join(viejos)}")

    creadas = []
    for carpeta in ["planes", "discusiones", "memoria/sesiones", "handoff", "logs"]:
        p = SIA / carpeta
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            creadas.append(carpeta)
    if creadas:
        print(f"Carpetas creadas: {', '.join(creadas)}")
    else:
        print("Carpetas: OK")

    print("Scripts: en git — actualizados vía 'cd sistema-ia && git pull' ✓")
    print("Skills:  en git — actualizadas vía 'cd sistema-ia && git pull' ✓")

    print()
    print("INTACTO:")
    for p in PROTEGIDOS:
        existe = (SIA / p).exists() or (ROOT / p).exists()
        print(f"  {p}: {'existe' if existe else 'no existe'}")

    print()
    print("Listo.")


if __name__ == "__main__":
    main()
