#!/usr/bin/env python3
"""
finalizar_plan.py
El dev ejecuta esto al completar TODO el plan.
Genera review caveman + limpia screenshots de bugs resueltos.
Uso: python ./acciones/finalizar_plan.py [modulo] [version]

Ejemplo:
  python ./acciones/finalizar_plan.py facturacion v1
"""
import sys
import os
import re
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent


def encontrar_raiz():
    current = SCRIPT_DIR.parent
    for _ in range(6):
        if (current / "ESTADO.md").exists():
            return current
        current = current.parent
    return SCRIPT_DIR.parent.parent


ROOT = encontrar_raiz()
SIA = ROOT / "sistema-ia"


def generar_review(modulo, version):
    """Genera review caveman en memoria/[modulo]/review.md"""
    plan_path = SIA / "planes" / modulo / f"{version}.md"
    memoria_dir = SIA / "memoria" / modulo
    memoria_dir.mkdir(parents=True, exist_ok=True)
    review_path = memoria_dir / "review.md"

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Extraer tareas completadas del plan
    tareas = []
    if plan_path.exists():
        contenido = plan_path.read_text(encoding="utf-8")
        for line in contenido.splitlines():
            if line.strip().startswith("- [x]"):
                tareas.append(line.strip()[6:].strip())

    tareas_texto = "\n".join(f"- [x] {t}" for t in tareas) if tareas else "- (ver plan)"

    review = f"""# Review: {modulo}/{version}
**Fecha:** {fecha}  **Tareas:** {len(tareas)} completadas

## Cambios
{tareas_texto}

## Para verificar
- [ ] App compila/corre sin errores
- [ ] Funcionalidad nueva funciona como se esperaba
- [ ] No hay regresiones en lo anterior
"""

    review_path.write_text(review, encoding="utf-8")
    print(f"OK: Review generado en memoria/{modulo}/review.md")
    return review_path


def limpiar_screenshots_bugs(modulo):
    """Si el plan es de bugs (fix-*), limpia screenshots de bugs marcados [x]."""
    if "bug" not in modulo.lower() and "fix" not in modulo.lower():
        return

    backlog_path = SIA / "discusiones" / "bugs" / "backlog.md"
    if not backlog_path.exists():
        return

    contenido = backlog_path.read_text(encoding="utf-8")
    screenshots_dir = SIA / "discusiones" / "bugs" / "screenshots"

    # Buscar bugs marcados como resueltos
    bugs_resueltos = re.findall(
        r'## Bug #(\d+).*?Estado:\s*(?:resuelto|arreglado|cerrado|fijo)',
        contenido, re.DOTALL | re.IGNORECASE
    )

    eliminados = 0
    for num in bugs_resueltos:
        screenshot = screenshots_dir / f"bug-{int(num):03d}.png"
        if screenshot.exists():
            screenshot.unlink()
            eliminados += 1

    if eliminados:
        print(f"OK: {eliminados} screenshots de bugs resueltos eliminados")


def main():
    if len(sys.argv) < 3:
        print("Uso: python ./acciones/finalizar_plan.py [modulo] [version]")
        sys.exit(1)

    modulo, version = sys.argv[1], sys.argv[2]

    # Generar review caveman
    generar_review(modulo, version)

    # Limpiar screenshots de bugs resueltos
    limpiar_screenshots_bugs(modulo)

    # Avisar
    os.system(f'python "{SCRIPT_DIR}/avisar.py" "PLAN COMPLETO: {modulo}/{version} — review generado — revisa" normal')

    print(f"\n✅ Plan {modulo}/{version} ejecutado completo")
    print(f"📋 Review en: sistema-ia/memoria/{modulo}/review.md")
    print("🆗 Si todo OK: di 'ok' para cerrar\n")


if __name__ == '__main__':
    main()
