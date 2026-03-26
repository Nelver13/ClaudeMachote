# disc_dashboard-comandos — claudecodesupremotemrinal
**Estado:** Aprobado
**Fecha:** 2026-03-24

---

## Qué es

Plantilla mínima para Claude Code — sin dashboard, sin SQLite, sin Flask.
Máxima eficiencia. Lista para recibir el dashboard como capa encima después.

**Ciclo:** Idea → realizar → probar → pulir → siguiente idea → hasta terminar el proyecto

---

## Avisos — solo cuando necesitás tu atención

El arquitecto puede estar haciendo otra cosa. El sonido indica que pasó algo. El WhatsApp indica qué pasó.

| Cuándo | Tipo | Por qué avisás |
|---|---|---|
| Discusión lista para leer | suave | Necesitás leerla y dar feedback |
| Discusión releída (`1`) | suave | Hay cambios para revisar |
| Plan generado — listo para arrancar | normal | Confirmar que arranca |
| Plan terminado | normal | Revisá antes de la siguiente etapa |
| Etapa cerrada | normal | Revisá y decí si seguimos |
| Claude necesita una decisión tuya | normal | Sin tu respuesta no puede continuar |
| Secret detectado | urgente | Parar todo |
| Error inesperado | urgente | Necesita tu intervención |

**No avisa:** tareas individuales marcadas, archivos escritos, pasos internos — eso Claude lo resuelve solo.

---

## Estructura — mínimo funcional

```
claudecodesupremotemrinal/
├── CLAUDE.md
├── STACK.md
├── iniciar.bat            ← doble click → abre Claude Code
├── iniciar.sh             ← en Mac/Linux
├── .gitignore
├── .claude/
│   ├── settings.json      ← 2 hooks: check_secrets + notificar
│   └── skills/            ← 7 skills
└── claude/
    ├── estado.log
    ├── MAPA.md
    ├── discusiones/
    │   ├── creaciones/
    │   └── soluciones/
    ├── planes/
    ├── backups/n8n/
    ├── backups/sql/
    ├── imagenes/errores/
    ├── imagenes/mejoras/
    └── acciones/
        ├── avisar.py          ← sonido + WhatsApp
        ├── notificar.py       ← hook Notification (filtrado)
        ├── check_secrets.py   ← hook PreToolUse
        ├── backup_n8n.py
        ├── backup_sql.py
        ├── credenciales.md
        └── aviso_*.mp3 (x3)
```

**Eliminado vs versiones anteriores:** Flask, SQLite, motor_detect, iniciar_sesion, cerrar_sesion, iniciar_dashboard, init_db, setup.py, log_tarea.py (Claude avisa directo cuando termina algo importante).

---

## Hooks — solo 2

| Hook | Script | Qué hace |
|---|---|---|
| `PreToolUse` (Bash) | `check_secrets.py` | Bloquea secrets — urgente si detecta |
| `Notification` | `notificar.py` | Filtra: solo avisa si Claude pide atención |

`notificar.py` filtra el tipo de notificación — si es un paso interno Claude resuelve solo, si necesita al arquitecto avisa. Claude también llama `avisar.py` directamente al terminar etapas y planes.

---

## Punto de entrada

```
doble click en iniciar.bat
        ↓
abre terminal → corre `claude` en esa carpeta
        ↓
Claude lee estado.log → presenta contexto → empezamos
```

---

## Compatible con dashboard después

Cuando se agregue el dashboard: solo se suma `claude/dashboard/` + `setup.py` encima — sin tocar nada de esta estructura.

---

## Próximo paso
`0` → creo `claudecodesupremotemrinal/` completo.
