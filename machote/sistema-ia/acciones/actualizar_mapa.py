#!/usr/bin/env python3
"""
actualizar_mapa.py
Actualiza MAPA.md automáticamente con el estado actual del proyecto.
Uso: python ./acciones/actualizar_mapa.py
"""
import os
import re
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
MAPA_FILE = ROOT_DIR / "MAPA.md"
ESTADO_FILE = ROOT_DIR.parent / "ESTADO.md"

def parse_estado():
    """Lee ESTADO.md (raiz) y devuelve dict con valores."""
    data = {}
    if ESTADO_FILE.exists():
        content = ESTADO_FILE.read_text(encoding='utf-8')
        for line in content.strip().split('\n'):
            if '[' in line and ']' in line:
                key = line.split('[')[1].split(']')[0]
                val = line.split(': ', 1)[1] if ': ' in line else ''
                data[key] = val.strip()
    return data

def count_files():
    """Cuenta archivos por tipo."""
    total = 0
    py_files = 0
    md_files = 0
    audio_files = 0
    
    for path in ROOT_DIR.rglob('*'):
        if path.is_file() and '.git' not in str(path):
            total += 1
            if path.suffix == '.py':
                py_files += 1
            elif path.suffix == '.md':
                md_files += 1
            elif path.suffix in ['.mp3', '.wav', '.ogg']:
                audio_files += 1
    
    return {'total': total, 'py': py_files, 'md': md_files, 'audio': audio_files}

def list_dirs():
    """Lista directorios principales."""
    dirs = []
    for item in sorted(ROOT_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith('.') and item.name != '__pycache__':
            file_count = len([f for f in item.rglob('*') if f.is_file()])
            dirs.append((item.name, file_count))
    return dirs

def generate_mapa():
    """Genera el contenido del MAPA.md."""
    estado = parse_estado()
    counts = count_files()
    dirs = list_dirs()
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    proyecto = estado.get('PROJ', estado.get('PROYECTO', 'mi-proyecto'))
    modulo = estado.get('MODULO', '(vacío)')
    plan = estado.get('PLAN', 'v1')
    ia = estado.get('IA', 'ninguna')
    tarea = estado.get('TAREA_ACTUAL', '1')
    progreso = estado.get('PROGRESO', '0%')
    next_task = estado.get('NEXT_TASK', 'definir plan')
    
    dirs_table = '\n'.join([f"| `./{d}/` | {c} archivos |" for d, c in dirs])
    
    content = f"""# 🗺️ MAPA DEL PROYECTO — Multi-IA System
> Formato: embedding-optimized | Auto-generado: {now}

```
[PROYECTO] {proyecto}
[RAIZ] ./
[ESTADO] {progreso} — {next_task}
[ESTRUCTURA] {len(dirs)} dirs | {counts['md']} MD | {counts['py']} PY | {counts['audio']} audio
```

---

## 📁 DIRECTORIOS ({len(dirs)})

| Path | Contenido |
|------|-----------|
{dirs_table}

---

## 📄 ARCHIVOS CORE (leer al inicio)

| Archivo | Propósito | Tokens est. |
|---------|-----------|-------------|
| `AGENTS.md` | Reglas universales TODAS las IAs | ~300 |
| `MAPA.md` | Este archivo — índice del proyecto | ~600 |
| `ESTADO.md` | Estado actual | ~50 |

---

## 🤖 CONFIG POR IA (leer según quién soy)

| Archivo | Para | Tokens |
|---------|------|--------|
| `CLAUDE.md` | Claude | ~200 |
| `KIMI.md` | Kimi | ~150 |
| `CODEX.md` | Codex | ~150 |
| `GEMINI.md` | Gemini | ~200 |

---

## ⚡ SCRIPTS (`./acciones/`)

| Script | Función | Args |
|--------|---------|------|
| `avisar.py` | Notificar | `"msg" tipo` |
| `actualizar_checklist.py` | Marcar tarea | `<plan> <N>` |
| `finalizar_etapa.py` | Cerrar etapa | `[nombre]` |
| `backup_n8n.py` | Backup n8n | `[N]` |
| `backup_sql.py` | Backup DB | `[N]` |
| `check_secrets.py` | Detectar secretos | — |
| `actualizar_mapa.py` | Actualizar este archivo | — |

---

## 🎯 FLUJO RÁPIDO

```
1. Leer AGENTS.md + MAPA.md + ESTADO.md
2. modo:arquitecto → discs/[modulo]/v[N].md
3. modo:dev → ESTADO.md → tarea → avisar.py → [x]
4. finalizar_etapa.py → backup → avisar.py
```

---

## 📊 ESTADO ACTUAL

```
PROYECTO: {proyecto}
MODULO: {modulo}
PLAN: {plan}
IA: {ia}
TAREA_ACTUAL: {tarea}
PROGRESO: {progreso}
NEXT_TASK: {next_task}
```

---

## 🔔 COMANDOS

```bash
# Notificar (suave|normal|urgente)
python ./acciones/avisar.py "Tarea N: X" normal

# Actualizar este mapa
python ./acciones/actualizar_mapa.py

# Test
python ./acciones/avisar.py --test
```

---

## ⚠️ REGLAS

1. No hablar. Hacer. Avisar.
2. Una tarea por sesión (modo:dev)
3. NUNCA git commit/push
4. Siempre avisar.py al terminar
5. **Actualizar MAPA.md tras cambios estructurales**

---

```
[AUTO] Regenerado: {now} | Archivos: {counts['total']} | Dirs: {len(dirs)}
[ACCION] Si cambiaste estructura: python ./acciones/actualizar_mapa.py
```
"""
    return content

def main():
    new_content = generate_mapa()
    MAPA_FILE.write_text(new_content, encoding='utf-8')
    print(f"[MAPA] Actualizado: {MAPA_FILE}")
    print(f"[INFO] {len(list(ROOT_DIR.rglob('*.md')))} archivos MD encontrados")

if __name__ == '__main__':
    main()
