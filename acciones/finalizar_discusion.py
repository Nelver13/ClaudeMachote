#!/usr/bin/env python3
"""
finalizar_discusion.py — Cierra discusion modo:arquitecto, genera prompt handoff para dev.
Uso: python .claude/ia/acciones/finalizar_discusion.py [modulo] [version]
Ejemplo: python .claude/ia/acciones/finalizar_discusion.py facturacion v1
"""
import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
PLANES_DIR = ROOT_DIR / "planes"
HANDOFF_DIR = ROOT_DIR / "handoff"


def extraer_tareas(plan_path: Path) -> str:
    if not plan_path.exists():
        return "(No se encontro el plan. Verifica la ruta.)"
    contenido = plan_path.read_text(encoding="utf-8")
    tareas, en_tareas = [], False
    for line in contenido.splitlines():
        if "## Tareas" in line or "## TAREAS" in line:
            en_tareas = True
            continue
        if en_tareas and line.startswith("## ") and "Tareas" not in line:
            break
        if en_tareas:
            tareas.append(line)
    return "\n".join(tareas).strip() if tareas else contenido


def extraer_decisiones(plan_path: Path) -> list:
    if not plan_path.exists():
        return []
    contenido = plan_path.read_text(encoding="utf-8")
    decisiones = []
    for line in contenido.splitlines():
        if re.match(r"^[-*] .{5,80}$", line.strip()):
            decisiones.append(line.strip().lstrip("-* "))
        if len(decisiones) >= 5:
            break
    return decisiones


def extraer_archivos(plan_path: Path) -> str:
    contenido = plan_path.read_text(encoding="utf-8")
    archivos = set()
    for match in re.finditer(r"`([^`]+\.[a-zA-Z0-9]+)`", contenido):
        candidato = match.group(1)
        if "/" in candidato or "\\" in candidato or "." in candidato:
            archivos.add(candidato)
    return "\n".join(sorted(archivos)) if archivos else "(Ver plan completo)"


def main():
    if len(sys.argv) < 3:
        print("Uso: python .claude/ia/acciones/finalizar_discusion.py [modulo] [version]")
        sys.exit(1)

    modulo, version = sys.argv[1], sys.argv[2]
    plan_path = PLANES_DIR / modulo / f"{version}.md"
    (PLANES_DIR / modulo).mkdir(parents=True, exist_ok=True)

    tareas_texto = extraer_tareas(plan_path)
    archivos_texto = extraer_archivos(plan_path)

    prompt = f"""modo:dev

Archivos a cargar:
- INICIO.md, ESTADO.md, AGENTS.md, MAPA.md
- sistema-ia/.claude/ia/AGENTS.md

Plan: sistema-ia/.claude/ia/planes/{modulo}/{version}.md
Memoria: sistema-ia/.claude/ia/memoria/{modulo}/progreso.md

Tareas:
{tareas_texto}

Archivos referenciados:
{archivos_texto}

Reglas:
- Ejecuta TODO seguido. Sin parar entre tareas.
- Marca [x] en cada tarea completada. Actualiza progreso.md y ESTADO.md.
- Problema grave: python sistema-ia/.claude/ia/acciones/avisar.py "PROBLEMA: [desc]" urgente
- Al terminar: python sistema-ia/.claude/ia/acciones/finalizar_plan.py {modulo} {version}
- NO git commit/push. NO secrets en código.
"""

    # Guardar prompt en raíz del proyecto
    proyecto_raiz = ROOT_DIR.parent.parent
    prompt_file = proyecto_raiz / f"PROMPT_DEV_{modulo}_{version}.txt"
    prompt_file.write_text(prompt, encoding="utf-8")

    # Generar JSON handoff (más eficiente que el txt para IAs)
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    decisiones = extraer_decisiones(PLANES_DIR / modulo / f"{version}.md")
    handoff = {
        "modulo": modulo,
        "version": version,
        "plan": f"sistema-ia/.claude/ia/planes/{modulo}/{version}.md",
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "decisiones_clave": decisiones,
        "estado": "listo_para_dev"
    }
    handoff_file = HANDOFF_DIR / f"{modulo}.json"
    handoff_file.write_text(json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8")

    os.system(
        f'python "{SCRIPT_DIR}/avisar.py" "PLAN: {modulo}/{version} listo — ejecuta dev" normal'
    )

    print(f"OK: {modulo}/{version}")
    print(f"Plan:    sistema-ia/.claude/ia/planes/{modulo}/{version}.md")
    print(f"Handoff: sistema-ia/.claude/ia/handoff/{modulo}.json")
    print(f"Prompt:  {prompt_file.name}")


if __name__ == "__main__":
    main()
