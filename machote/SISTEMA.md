# SISTEMA.md — Guía completa del sistema Multi-IA
> Este archivo describe la estructura, versiones y reglas de evolución del sistema.
> La IA lo lee para entender qué hay, qué cambió y cómo versionar correctamente.

---

## Estructura completa

```
proyecto/
├── CLAUDE.md              ← Claude lee esto al abrir (instrucciones + rol)
├── KIMI.md                ← Kimi lee esto al abrir
├── CODEX.md               ← Codex/ChatGPT lee esto al abrir
├── GEMINI.md              ← Gemini lee esto al abrir
├── INICIO.md              ← Briefing de rol (todas las IAs)
├── AGENTS.md              ← Reglas completas del sistema
├── ESTADO.md              ← Estado actual + roles + checkpoint
│
└── sistema-ia/
    ├── VERSION                    ← versión actual del sistema
    ├── SISTEMA.md                 ← este archivo
    ├── CHANGELOG.md               ← historial de cambios
    │
    ├── .claude/
    │   ├── settings.json          ← permisos automáticos + hooks
    │   └── skills/
    │       ├── modo-arquitecto/SKILL.md  ← comportamiento arquitecto
    │       ├── modo-dev/SKILL.md         ← comportamiento dev
    │       └── caveman/SKILL.md          ← modo ahorro de tokens
    │
    ├── acciones/                  ← scripts que ejecutan las IAs
    │   ├── avisar.py              ← notifica + guarda checkpoint
    │   ├── cambiar_rol.py         ← cambia rol en ESTADO.md
    │   ├── cerrar_sesion.py       ← guarda resumen del día
    │   ├── comprimir_discusion.py ← comprime temas cerrados
    │   ├── finalizar_discusion.py ← cierra debate → genera plan + JSON handoff
    │   ├── finalizar_plan.py      ← cierra plan ejecutado
    │   ├── check_role.py          ← hook PreToolUse: valida rol antes de escribir
    │   ├── check_secrets.py       ← detecta secrets en código
    │   ├── completar_tarea.py     ← marca tarea [x] y actualiza ESTADO.md
    │   ├── auto_setup.py          ← SessionStart hook: configura o carga contexto
    │   ├── migrar.py              ← actualiza sistema sin tocar trabajo activo
    │   ├── credenciales.md        ← webhook/ntfy para notificaciones
    │   ├── aviso_suave.mp3        ← sonido tarea menor
    │   ├── aviso_normal.mp3       ← sonido plan listo/completo
    │   └── aviso_urgente.mp3      ← sonido error/bloqueo
    │
    ├── planes/                    ← planes del arquitecto para el dev
    ├── discusiones/               ← debate arquitecto + humano
    ├── memoria/
    │   ├── sesiones/              ← resúmenes diarios comprimidos
    │   └── [modulo]/              ← resumen + progreso por módulo
    ├── handoff/                   ← JSON de traspaso arquitecto → dev
    └── logs/                      ← log de notificaciones

```

---

## Versiones

| Versión | Fecha | Qué cambió |
|---------|-------|-----------|
| v1.x | anterior | Sistema básico Keyons (AGENT.md, estado.log, acciones/ en raíz) |
| v2.0 | 2026-04-15 | Primer machote multi-IA. Claude/Kimi/Codex/Gemini. Scripts base. |
| v2.1 | 2026-04-16 | auto_setup, cerrar_sesion, comprimir_discusion, caveman skill, checkpoints en avisar |
| v2.2 | 2026-04-16 | Acciones completas en machote, skills con flujo explícito de avisos y [x] |
| v2.3 | 2026-04-18 | Fix arquitecto→dev handoff validado, avisar.py paths robustos, migrar.py replenece scripts faltantes, auto-detección de versión nueva, ahorro embebido en skills de rol |

---

## Reglas de versionado

| Cambio | Versión |
|--------|---------|
| Fix de bug / script faltante | patch (2.1 → 2.2) |
| Nueva funcionalidad / nuevo script | minor (2.2 → 2.3) |
| Cambio de estructura / flujo completo | major (2.x → 3.0) |

---

## Checklist para nuevo commit/versión

Cuando se mejora el sistema, la IA hace esto EN ORDEN:

**1. Implementar el cambio**
- Editar scripts en `machote/sistema-ia/acciones/`
- Editar skills en `machote/sistema-ia/.claude/skills/`
- Editar estructura si aplica

**2. Sincronizar al proyecto activo**
- Copiar scripts modificados también a `sistema-ia/acciones/` (proyecto actual)
- Copiar skills modificados también a `sistema-ia/.claude/skills/`

**3. Actualizar VERSION**
```
machote/sistema-ia/VERSION  ← nueva versión
VERSION                      ← nueva versión (raíz)
```

**4. Actualizar CHANGELOG.md**
```markdown
## vX.Y — YYYY-MM-DD
### Agregado / Corregido / Mejorado
- descripción exacta del cambio
```

**5. Actualizar SISTEMA.md**
- Agregar nueva versión a la tabla
- Actualizar estructura si cambió algún archivo

**6. Avisar**
```bash
python sistema-ia/acciones/avisar.py "vX.Y lista para commit" normal
```

**7. Decir al humano:**
```
Listo — vX.Y — ejecuta:
git add machote/ VERSION CHANGELOG.md SISTEMA.md
git commit -m "vX.Y — [descripción corta]"
git push
```

---

## Flujo del sistema (resumen)

```
TÚ: idea
  ↓
Arquitecto: crea discusiones/N-modulo/v1.md + pregunta 1 → avisa
TÚ: escribe feedback en el archivo → "1"
Arquitecto: procesa feedback → actualiza → avisa
(repite hasta cerrar todos los temas)
TÚ: "0"
Arquitecto: crea plan + PROMPT_DEV → avisa
  ↓
TÚ: pega PROMPT_DEV
Dev: cambia rol solo → ejecuta tarea → marca [x] → actualiza ESTADO.md → avisa
(repite por cada tarea)
Dev: finalizar_plan.py → cerrar_sesion.py → avisa
  ↓
TÚ: "ok"
```

---

## Comandos del humano

| Comando | Qué hace |
|---------|----------|
| `1` | Arquitecto procesa feedback del archivo de discusión |
| `0` | Arquitecto aprueba → genera plan → entrega al dev |
| `ok` | Aprueba plan ejecutado |
| `rol` | Muestra rol actual de la IA |

---

## Para instalar en proyecto nuevo

```bash
git clone git@github.com:Nelver13/ClaudeMachote.git sistema-ia
python sistema-ia/instalar.py
```

## Para actualizar desde versión anterior

```bash
cd sistema-ia && git pull && cd ..
python sistema-ia/acciones/migrar.py
```

---

## Auto-actualización (desde v2.3)

Flujo automático cuando el machote remoto tiene cambios:

```
1. Dev pushea v2.X al repo ClaudeMachote
2. En cualquier proyecto que ya clonó sistema-ia/:
   SessionStart hook (auto_setup.py) corre al abrir Claude
   → git fetch silencioso en sistema-ia/
   → compara VERSION local vs origin/main:VERSION
   → si difiere, inyecta aviso en el contexto de la sesión:
     "⚠ ACTUALIZACIÓN DISPONIBLE — machote vX.Y (local vZ.W).
      Ejecuta: cd sistema-ia && git pull && cd .. && python sistema-ia/acciones/migrar.py"
3. Humano ejecuta el comando
4. migrar.py:
   - Actualiza scripts/skills/assets existentes (con backup).
   - REPLENECE los que falten (recupera clones incompletos).
   - Actualiza sistema-ia/VERSION a la nueva.
   - NUNCA toca planes/, discusiones/, memoria/, handoff/, ESTADO.md.
```

Silencioso si no hay red o si `sistema-ia/` no es un clon git. No rompe nada.
