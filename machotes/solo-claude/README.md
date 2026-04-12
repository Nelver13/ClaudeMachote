# ClaudeMachote

Sistema de trabajo con Claude Code para proyectos de software.

- **Opus 4.6** = arquitecto (discute, diseña, genera planes)
- **Sonnet 4.6** = desarrollador (lee planes, escribe codigo, marca [x])

Un solo `CLAUDE.md` — Claude detecta el modelo y asume el rol correcto.

---

## Requisitos

- [Claude Code](https://claude.ai/code)
- Python 3.x

---

## Estructura

```
proyecto/
├── CLAUDE.md           <- instrucciones para Claude (ambos roles)
├── roadmap.md          <- vision y estado del proyecto
├── .gitignore
├── .claude/
│   └── settings.json   <- hook check_secrets
└── claude/             <- workspace (no va a git)
    ├── acciones/       <- scripts: avisar.py, credenciales.md, etc.
    ├── discusiones/
    │   ├── creaciones/ <- nuevas features
    │   └── soluciones/ <- bugs y fixes
    ├── planes/         <- plan_*.md
    ├── memoria/        <- memoria por modulo completado
    ├── backups/
    ├── logs/
    ├── RESUMEN.md
    └── estado.log
```

---

## Flujo de trabajo

### 1. Arquitecto (Opus)
```bash
claude  # abrir con modelo Opus
# Claude anuncia: Modo ARQUITECTO
# Discutir idea → 0 → genera plan
```

### 2. Desarrollador (Sonnet)
```bash
claude  # abrir con modelo Sonnet
# Claude anuncia: Modo DESARROLLADOR
s       # ejecutar plan tarea por tarea
```

### 3. Revision
Claude avisa al terminar cada respuesta (popup Windows + Discord).
Vos revisas → `ok` en Opus para aprobar → siguiente modulo.

---

## Setup inicial

```bash
# Copiar proyecto_listo/ a tu proyecto nuevo
# Configurar credenciales Discord:
# Editar: claude/acciones/credenciales.md

# Probar avisos:
python claude/acciones/avisar.py --test
```

---

## Scripts

| Script | Uso |
|---|---|
| `avisar.py "msg" suave\|normal\|urgente` | Notificacion con popup + sonido |
| `actualizar_checklist.py` | Marca [x] en plan |
| `backup_n8n.py [etapa]` | Backup n8n |
| `backup_sql.py [etapa]` | Backup DB |
| `finalizar_etapa.py` | Cierre de etapa |

---

## Reglas de oro

- Opus no escribe codigo. Sonnet no crea planes.
- `git commit/push` solo lo hace el arquitecto (vos).
- `claude/` nunca va a git.
- Credenciales en `claude/acciones/credenciales.md`.
