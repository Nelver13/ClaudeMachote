#!/usr/bin/env python3
"""
cambiar_rol.py — Cambia el rol de cualquier IA en ESTADO.md
Uso:
  python cambiar_rol.py                     → muestra roles actuales
  python cambiar_rol.py claude dev          → ROL_CLAUDE: DESARROLLADOR
  python cambiar_rol.py claude arq          → ROL_CLAUDE: ARQUITECTO
  python cambiar_rol.py kimi arq            → ROL_KIMI: ARQUITECTO
  python cambiar_rol.py codex dev           → ROL_CODEX: DESARROLLADOR
  python cambiar_rol.py gemini arquitecto   → ROL_GEMINI: ARQUITECTO
"""
import sys
import os
import re
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parents[3]  # acciones/→ia/→.claude/→sistema-ia/→raíz
ESTADO_FILE = ROOT / "ESTADO.md"

ALIASES = {
    "dev": "DESARROLLADOR",
    "developer": "DESARROLLADOR",
    "desarrollador": "DESARROLLADOR",
    "arq": "ARQUITECTO",
    "arquitecto": "ARQUITECTO",
    "architect": "ARQUITECTO",
}

ROLES_VALIDOS = {"ARQUITECTO", "DESARROLLADOR"}


def leer_roles_actuales() -> dict[str, str]:
    """Extrae todos los [ROL_XXX: YYY] del ESTADO.md."""
    roles = {}
    if not ESTADO_FILE.exists():
        return roles
    for linea in ESTADO_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\[ROL_([A-Z0-9_]+):\s*([A-Z]+)\]", linea.strip())
        if m:
            roles[m.group(1)] = m.group(2)
    return roles


def imprimir_tabla(roles: dict[str, str]) -> None:
    print("\nRoles actuales:")
    print("-" * 30)
    if not roles:
        print("  (ninguno definido)")
    else:
        for ia, rol in sorted(roles.items()):
            print(f"  {ia:<15} -> {rol}")
    print()


def cambiar_rol(ia: str, rol: str) -> None:
    """Reemplaza o inserta [ROL_{IA}: {ROL}] en ESTADO.md."""
    if not ESTADO_FILE.exists():
        print(f"ERROR: No se encontró ESTADO.md en {ROOT}")
        sys.exit(1)

    clave = f"ROL_{ia}"
    linea_nueva = f"[{clave}: {rol}]"
    contenido = ESTADO_FILE.read_text(encoding="utf-8")
    lineas = contenido.splitlines()
    nueva_lineas = []
    encontrado = False

    for linea in lineas:
        if linea.strip().startswith(f"[{clave}:"):
            nueva_lineas.append(linea_nueva)
            encontrado = True
        elif linea.strip().startswith("[CHECKPOINT:"):
            nueva_lineas.append(f"[CHECKPOINT: {datetime.now().strftime('%Y-%m-%d %H:%M')}]")
        else:
            nueva_lineas.append(linea)

    if not encontrado:
        # Insertar después de la última línea [ROL_*] o al inicio
        insert_idx = 0
        for i, linea in enumerate(nueva_lineas):
            if linea.strip().startswith("[ROL_"):
                insert_idx = i + 1
        nueva_lineas.insert(insert_idx, linea_nueva)

    ESTADO_FILE.write_text("\n".join(nueva_lineas) + "\n", encoding="utf-8")


def main():
    if len(sys.argv) == 1:
        # Solo mostrar tabla
        imprimir_tabla(leer_roles_actuales())
        return

    if len(sys.argv) < 3:
        print("Uso: python cambiar_rol.py [ia] [rol]")
        print("     python cambiar_rol.py claude arq")
        print("     python cambiar_rol.py kimi dev")
        sys.exit(1)

    ia_raw = sys.argv[1].strip().upper()
    rol_raw = sys.argv[2].strip().lower()

    rol = ALIASES.get(rol_raw, rol_raw.upper())
    if rol not in ROLES_VALIDOS:
        print(f"ERROR: Rol inválido '{rol_raw}'. Opciones: arq, dev")
        sys.exit(1)

    cambiar_rol(ia_raw, rol)

    # Avisar
    avisar = SCRIPT_DIR / "avisar.py"
    if avisar.exists():
        os.system(f'python "{avisar}" "ROL_{ia_raw}: {rol}" suave')

    # Mostrar tabla actualizada
    print(f"OK: ROL_{ia_raw} -> {rol}")
    imprimir_tabla(leer_roles_actuales())


if __name__ == "__main__":
    main()
