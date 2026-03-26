# disc_modoia — ClaudeMachote "modo ia" — versión 100% funcional
**Estado:** Aprobado
**Fecha:** 2026-03-24

---

## Qué pediste
Analizar todo lo que existe y construir una versión nueva llamada **modo ia** que una lo mejor de version3 y version3ligera, 100% funcional.

---

## Decisiones incorporadas (R:/)

| Tema | Decisión |
|---|---|
| Nombre | `modo_ia/` — carpeta nueva en la raíz |
| Motor | DOS variantes: una multi-motor + una solo Claude Code |
| Dashboard | Nuevo desde cero, funcional, que controle agentes desde la UI |
| MAPA.md | Redefinido como mapa vectorizado para IA (ver abajo) |
| RESUMEN.md | Eliminado — el MAPA cubre esa función |
| discusiones/ | Subcarpetas: `creaciones/` y `soluciones/` |
| SQLite | Persistencia total: guardar estado y continuar entre sesiones |
| winforms skill | ELIMINADO |
| Skills nuevas | `git-security` + `docker-prod` + `docker-test` |
| flutter skill | Renombrado a `mobile/` — cubre Electron + React Native |
| n8n skill | Incluye regla: agentes de IA siempre en JSON |
| Motores | Claude, Cursor, VS Code+Copilot, Google Antigravity |
| Carpetas viejas | No tocar — el arquitecto reorganiza después |

---

## El problema central (diagnóstico)

version3 y version3ligera nunca se unieron. Cada una tiene lo que le falta a la otra:

| | version3 | version3ligera |
|---|---|---|
| Hooks reales | ✅ | ❌ |
| Tokens reales | ✅ | ❌ (estimados) |
| Tracking sesión | ✅ | ❌ |
| Multi-motor | ❌ | ✅ |
| Dashboard rico | ❌ | ✅ (roto) |
| Motor detect | ❌ | ✅ |
| credenciales seguras | ✅ | ❌ (expuestas en raíz) |

---

## Arquitectura de modo ia

### Dos variantes en un solo repo

```
modo_ia/
├── claude_code/     ← variante solo Claude Code (hooks, tracking real, skills)
└── multi_motor/     ← variante multi-motor (+ Cursor, Copilot, Antigravity)
```

Cuando el arquitecto copia a un proyecto nuevo, elige una variante.
Ambas comparten el mismo dashboard y la misma estructura `claude/`.

---

### MAPA.md — redefinido (mapa vectorizado para IA)

Ya no es una guía de usuario. Es un mapa estructurado que la IA lee al inicio para entender rápidamente:
- Qué carpetas existen y para qué sirve cada una
- Qué archivo hace qué cosa
- Cómo están conectados entre sí
- Qué NO tocar sin leer primero

Se actualiza automáticamente al cerrar etapa (`finalizar_etapa.py` lo regenera).
Reemplaza al `RESUMEN.md` — RESUMEN.md se elimina.

Ejemplo de estructura:
```markdown
# MAPA — [nombre proyecto]
## Árbol funcional
claude/acciones/       → scripts que Claude ejecuta
claude/discusiones/
  creaciones/          → ideas nuevas, features nuevas
  soluciones/          → mejoras a algo que ya existe, bugs, gaps
claude/planes/         → checklists de ejecución aprobados
claude/dashboard/      → interfaz web de control
claude/logs/           → tokens, sesiones, eventos
.claude/skills/        → instrucciones de stack por tecnología
motores/               → instrucciones específicas por motor de IA
## Archivos clave
CLAUDE.md              → protocolo que sigue la IA
MAPA.md                → este archivo (actualizar al cerrar etapa)
estado.log             → estado granular actual
```

---

### Skills — lista actualizada

| Skill | Estado | Notas |
|---|---|---|
| `django-drf` | Conservar | Sin cambios |
| `react-vite` | Ampliar | + verificación .gitignore + seguridad |
| `mobile` | Nuevo | Unifica Flutter + React Native + Electron |
| `n8n-flows` | Ampliar | + regla: agentes de IA siempre en JSON |
| `git-security` | NUEVO | Revisa .gitignore antes de cada commit, bloquea secrets |
| `docker-prod` | NUEVO | Build y deploy de producción vía Docker |
| `docker-test` | NUEVO | Deploy rápido a servidor de prueba para ver resultado |
| `winforms` | ELIMINADO | — |

**git-security** se activa automáticamente en cualquier stack — no es opcional. Es parte del hook `check_secrets.py` ya existente pero con un skill dedicado que guía a Claude en cómo armar el `.gitignore` correcto para cada tecnología.

**docker-prod** se activa cuando el arquitecto dice "está listo para producción".
**docker-test** se activa cuando el arquitecto dice "quiero mostrar algo" o "subí a un servidor de prueba".

---

### discusiones/ — estructura nueva

```
claude/discusiones/
├── creaciones/      ← ideas nuevas, features, mejoras de fondo
│   └── disc_[nombre].md
└── soluciones/      ← bugs, gaps, algo que falla o falta
    └── disc_[nombre].md
```

Claude elige la subcarpeta según el tipo de pedido.
El dashboard muestra ambas carpetas en tabs separados.

---

### Dashboard — nuevo desde cero

**Objetivo principal:** controlar agentes de IA (Claude Code, Cursor, Copilot, Antigravity) desde una sola interfaz, con el máximo de automatización posible.

**Tabs:**
1. **Inicio** — estado actual del proyecto, motor activo, sesión en curso
2. **Discusiones** — ver/crear discusiones (creaciones y soluciones)
3. **Planes** — ver checklists activos, marcar tareas `[ ]→[x]` (handler funcional)
4. **Tokens** — consumo real por sesión, por etapa, costo estimado
5. **Motores** — ver qué motor está activo, cambiar, ver estado de cada agente
6. **Reportes** — historial de etapas cerradas, backups, resumen de sesiones

**SQLite** — base de datos persistente que guarda:
- Sesiones (inicio/cierre, tokens, motor usado)
- Eventos de etapas
- Estado de discusiones y planes
- Stats por motor

La idea: el arquitecto abre el dashboard y ve TODO. No tiene que buscar en archivos.

---

### Estructura final de modo ia

```
modo_ia/
├── CLAUDE.md                    ← protocolo para la IA (50 líneas max)
├── MAPA.md                      ← mapa vectorizado (se actualiza solo)
├── STACK.md                     ← stack del arquitecto
├── .gitignore
│
├── .claude/
│   ├── settings.json            ← 4 hooks reales (check_secrets, log_escritura, notificar, iniciar_dashboard)
│   └── skills/
│       ├── django-drf/SKILL.md
│       ├── react-vite/SKILL.md  ← + git security
│       ├── mobile/SKILL.md      ← Flutter + React Native + Electron
│       ├── n8n-flows/SKILL.md   ← + agentes en JSON
│       ├── git-security/SKILL.md  ← NUEVO
│       ├── docker-prod/SKILL.md   ← NUEVO
│       └── docker-test/SKILL.md   ← NUEVO
│
├── motores/
│   ├── claude/.instructions.md
│   ├── cursor/.instructions.md
│   ├── copilot/.instructions.md     ← VS Code + Copilot
│   └── antigravity/.instructions.md ← Google
│
└── claude/
    ├── estado.log
    ├── MAPA.md                  ← copia viva (regenerada por finalizar_etapa)
    ├── discusiones/
    │   ├── creaciones/
    │   └── soluciones/
    ├── planes/
    ├── backups/n8n/
    ├── backups/sql/
    ├── imagenes/errores/
    ├── imagenes/mejoras/
    ├── logs/
    │   ├── tokens.json
    │   └── sesiones.json
    ├── dashboard/
    │   ├── app.py               ← Flask nuevo, 6 tabs, SQLite, token tracking real
    │   ├── requirements.txt
    │   └── templates/index.html ← control de agentes, automatización max
    └── acciones/
        ├── credenciales.md      ← siempre aquí
        ├── avisar.py
        ├── notificar.py
        ├── backup_n8n.py
        ├── backup_sql.py
        ├── check_secrets.py
        ├── log_escritura.py
        ├── cerrar_sesion.py
        ├── iniciar_sesion.py
        ├── iniciar_dashboard.py
        ├── finalizar_etapa.py   ← también regenera MAPA.md
        ├── motor_detect.py
        ├── README.md
        └── aviso_*.mp3 (x3)
```

---

## Orden de construcción (bottom-up)

1. Estructura de carpetas + `.gitignore`
2. Scripts de acciones (base funcional)
3. SQLite schema + `init_db.py`
4. Dashboard Flask nuevo (tabs, handlers funcionales)
5. Token tracking real desde `~/.claude/projects/`
6. `.claude/settings.json` con 4 hooks
7. Skills actualizados (7 skills)
8. Archivos `.instructions.md` por motor (4 motores)
9. `CLAUDE.md` v7.0 compacto
10. `MAPA.md` vectorizado
11. Prueba en `pruebaversion3/` como sandbox

---

## Riesgos

- Token tracking real solo funciona para Claude Code — Cursor/Copilot no exponen el mismo path. Para multi-motor, tokens serán estimados hasta que haya API oficial.
- Dashboard nuevo desde cero = más tiempo de construcción, pero sin deuda técnica
- MAPA.md regenerado automáticamente puede quedar desactualizado si `finalizar_etapa.py` falla

---

## Próximo paso
Decí `0` para aprobar — genero `plan_001.md` y arrancamos.
