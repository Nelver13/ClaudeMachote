#!/usr/bin/env python3
"""
comprimir_discusion.py — Comprime secciones cerradas de una discusión.
Cuando una discusión crece demasiado, comprime las decisiones ya cerradas
en una sola línea y borra el detalle. Solo quedan los temas abiertos.

Marca temas como cerrados en el .md con: <!-- CERRADO -->

Uso: python comprimir_discusion.py sistema-ia/.claude/ia/discusiones/1-login/v1.md
"""
import sys
import re
from pathlib import Path
from datetime import datetime


def comprimir(path: Path):
    contenido = path.read_text(encoding="utf-8")
    secciones = re.split(r"(^#{1,3} .+$)", contenido, flags=re.MULTILINE)

    resultado = []
    comprimidos = []
    i = 0

    while i < len(secciones):
        bloque = secciones[i]
        if "<!-- CERRADO -->" in bloque:
            # Extraer título de la sección anterior
            titulo = secciones[i - 1].strip() if i > 0 else "Sección"
            decision = re.search(r"(?:decision|resultado|resuelto)[:\s]+(.+)", bloque, re.IGNORECASE)
            resumen = decision.group(1).strip() if decision else "cerrado"
            comprimidos.append(f"- {titulo.lstrip('#').strip()}: {resumen}")
        else:
            resultado.append(bloque)
        i += 1

    # Insertar bloque comprimido al inicio si hay temas cerrados
    if comprimidos:
        fecha = datetime.now().strftime("%Y-%m-%d")
        bloque_comprimido = f"\n## Decisiones cerradas [{fecha}]\n" + "\n".join(comprimidos) + "\n\n"
        # Insertar después del primer encabezado
        primer_h1 = next((j for j, s in enumerate(resultado) if s.startswith("# ")), 0)
        resultado.insert(primer_h1 + 1, bloque_comprimido)

    path.write_text("".join(resultado), encoding="utf-8")
    print(f"OK: {len(comprimidos)} temas comprimidos en {path.name}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python comprimir_discusion.py [ruta_discusion.md]")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: No existe {path}")
        sys.exit(1)

    comprimir(path)


if __name__ == "__main__":
    main()
