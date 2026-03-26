# Skill: Git Security
name: git-security
description: Seguridad en git — .gitignore correcto por stack, bloqueo de secrets, verificación antes de commit. Se activa en TODOS los proyectos automáticamente.
allowed tools: Read, Grep, Glob, Edit, Write, Bash

---

## Regla principal

**Antes de cualquier operación git → verificar `.gitignore` está completo para el stack activo.**

Este skill se activa siempre, independientemente del stack.

---

## .gitignore base (siempre)

```gitignore
# Claude — nunca a git
claude/
.motor/motor.json

# Entorno
.env
.env.local
.env.*.local
*.log
.DS_Store
Thumbs.db

# Secrets
*.pem
*.key
*.p12
*.pfx
secrets/
credentials/
```

## Adiciones por stack

| Stack | Agregar al .gitignore |
|---|---|
| Django | `__pycache__/`, `*.pyc`, `db.sqlite3`, `media/`, `staticfiles/` |
| React/Vite | `node_modules/`, `dist/`, `.vite/` |
| Flutter | `build/`, `.dart_tool/`, `.flutter-plugins` |
| Expo/RN | `.expo/`, `android/build/`, `ios/build/`, `*.ipa`, `*.apk` |
| Electron | `out/`, `release/` |
| Docker | `.docker/` (si contiene credenciales) |
| Python general | `.venv/`, `venv/`, `*.egg-info/`, `__pycache__/` |

---

## Verificación antes de commit (checklist)

Claude verifica automáticamente:
1. `.gitignore` existe y cubre el stack activo
2. No hay archivos `.env` en el staging
3. No hay credenciales hardcodeadas en archivos nuevos
4. `claude/` está en `.gitignore`

Si algo falla → **parar y señalar antes de continuar**.

---

## Secretos detectados = stop inmediato

Si se detecta cualquiera de estos patrones en código nuevo:
- `password = "..."`
- `API_KEY = "..."`
- `SECRET_KEY = "..."`
- Token JWT hardcodeado (`eyJ...`)

Acción: parar, no continuar, señalar el archivo y línea, sugerir mover a `.env`.

---

## Docker y git

Si el proyecto usa Docker para deploy:
- Verificar que `Dockerfile` y `docker-compose.yml` no copian `.env` al contenedor
- Verificar que `docker-compose.yml` lee variables desde `.env` (no las hardcodea)
- El `.env` siempre debe estar en `.gitignore`
