#!/usr/bin/env python3
"""
cerrar_sesion.py — Guarda resumen comprimido de la sesión del día.
La IA ejecuta esto al terminar el trabajo del día o al hacer /compact.

Uso: python cerrar_sesion.py "modulo" "resumen_una_linea" "proximo_paso"
     python cerrar_sesion.py "1-login" "modelo User + JWT creados" "falta endpoint refresh"
"""
import sys
import os
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
IA_DIR = SCRIPT_DIR.parent
SESIONES_DIR = IA_DIR / "memoria" / "sesiones"


def main():
    if len(sys.argv) < 4:
        print("Uso: python cerrar_sesion.py [modulo] [resumen] [proximo_paso]")
        sys.exit(1)

    modulo = sys.argv[1]
    resumen = sys.argv[2]
    proximo = sys.argv[3]
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M")

    SESIONES_DIR.mkdir(parents=True, exist_ok=True)
    sesion_file = SESIONES_DIR / f"{fecha}.md"

    # Si ya existe el archivo del día, agrega una entrada más
    if sesion_file.exists():
        contenido = sesion_file.read_text(encoding="utf-8")
    else:
        contenido = f"# Sesión {fecha}\n\n"

    entrada = f"""## {hora} — {modulo}
- Hecho: {resumen}
- Próximo: {proximo}

"""
    sesion_file.write_text(contenido + entrada, encoding="utf-8")

    os.system(f'python "{SCRIPT_DIR}/avisar.py" "Sesión guardada — {modulo}" suave')
    print(f"OK: sesión guardada en memoria/sesiones/{fecha}.md")


if __name__ == "__main__":
    main()
