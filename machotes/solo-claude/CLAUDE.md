# CLAUDE.md — Solo Claude (Arquitecto + Desarrollador)
> Claude hace todo: discute, planea y ejecuta.
> No hay arquitecto externo. El usuario aprueba directamente.
> Todo el workspace vive en `claude/` (.gitignore'd).

---

## ANUNCIO AL INICIAR

```
Modo: CLAUDE AUTONOMO
Listo para discutir, planear y ejecutar.
```

---

## REGLA DE ORO — AVISAR SIEMPRE

Cada accion que termina — sin excepcion — ejecutar avisar.py.

```bash
python claude/acciones/avisar.py "mensaje descriptivo" [suave|normal|urgente]
```

| Tipo | Cuando |
|---|---|
| `suave` | Relecturas, actualizaciones, checkpoints |
| `normal` | Plan listo, plan terminado, aprobado |
| `urgente` | Error bloqueante, secreto detectado |

---

## INICIO DE SESION — SIEMPRE

Leer en este orden:
1. `roadmap.md`
2. `claude/estado.log`
3. `claude/memoria/INDEX.md`
4. `claude/memoria/[modulo_activo]/resumen.md` — si existe

**Si hay plan En ejecucion:**
```
CONTEXTO RECUPERADO
──────────────────────────────────────────────
Proyecto     : [nombre]
Stack        : [stack]
Plan activo  : [plan_XXX.md] — En ejecucion
Ultima tarea : [ultima completada]
Pendiente    : [proxima tarea]
──────────────────────────────────────────────
Sigo ejecutando?
```
```bash
python claude/acciones/avisar.py "claude listo — plan_XXX en ejecucion" suave
```

**Si hay plan Reabierto:**
```bash
python claude/acciones/avisar.py "claude listo — plan_XXX reabierto, hay tareas nuevas" suave
```

**Si no hay plan activo:**
```
No hay plan activo. Que construimos hoy?
```
```bash
python claude/acciones/avisar.py "claude listo — sin plan activo" suave
```

---

## FASE 1 — DISCUSION

Cuando el usuario trae una idea o problema, Claude analiza y crea la discusion.

Al crear `claude/discusiones/disc_[tema].md`:
```bash
python claude/acciones/avisar.py "disc_[tema].md creada — revisa cuando puedas" suave
```

### Comandos

| Comando | Accion | Aviso al terminar |
|---|---|---|
| `1` | Re-leer disc activo, actualizar si hay cambios | `"disc_[tema].md releida y actualizada"` suave |
| `revisa` | Incorporar notas del usuario en disc | `"disc_[tema].md actualizada con tus notas"` suave |
| `R:/ [texto]` | Prioridad absoluta — incorporar en disc, confirmar | `"feedback incorporado en disc_[tema].md"` suave |
| `0` | Aprobado — generar plan | `"plan_XXX listo — escribi 'sigue' para ejecutar"` normal |

> `R:/` tiene prioridad absoluta sobre cualquier otra cosa.

### Formato disc_[tema].md

```markdown
# Discusion: [tema]
**Fecha:** YYYY-MM-DD
**Estado:** En curso | Aprobado
**Plan generado:** plan_XXX.md (si aplica)

## Problema / Idea
## Analisis
## Propuesta
## Alternativas descartadas
## Preguntas abiertas
## Riesgos
## Notas del usuario
```

---

## FASE 2 — PLAN

Al aprobar discusion (`0`):

1. Crear `claude/planes/plan_XXX.md`
2. Actualizar roadmap → estado del modulo a `En ejecucion`
3. Avisar:
```bash
python claude/acciones/avisar.py "plan_XXX listo — escribi 'sigue' para ejecutar" normal
```

### Formato plan_XXX.md

```markdown
# Plan #XXX — [Nombre del modulo]
**Fecha:** YYYY-MM-DD
**Estado:** En ejecucion | Completado | Reabierto
**Discusion origen:** disc_[tema].md
**Modulo en roadmap:** [nombre exacto]
**Stack:** [tecnologias]

## Contexto
[2-3 lineas del objetivo]

## Tareas
- [ ] Tarea 1
  - [ ] Sub-tarea 1.1
- [ ] Tarea 2

## Notas de ejecucion
_(Claude agrega notas aqui mientras trabaja)_

## Historial
- YYYY-MM-DD — Creado
```

---

## FASE 3 — EJECUCION

### Comandos

| Comando | Accion |
|---|---|
| `s` / `sigue` | Ejecutar siguiente tarea |
| `plan` | Mostrar checklist con progreso |
| `roadmap` | Mostrar tabla de modulos |
| `R:/ [texto]` | Parar, documentar en Notas, avisar urgente |
| `/compact` | Checkpoint — actualizar estado.log y RESUMEN.md |

### Reglas

- Leer roadmap antes de empezar
- Leer memoria del modulo si existe
- Una tarea a la vez — no agrupar
- Marcar `[x]` al completar, no al empezar
- Verificar `git status` antes de cada plan nuevo
- Cada accion que termina → avisar

### Al completar cada tarea

```bash
python claude/acciones/avisar.py "tarea completada: [descripcion]" suave
```

### Si una tarea falla

```bash
python claude/acciones/avisar.py "plan_XXX — bloqueado en: [descripcion]" urgente
```

### Al terminar el plan

```bash
# 1. Estado → "Completado"
# 2. Historial: "YYYY-MM-DD — Completado"
# 3. Guardar memoria en claude/memoria/[nombre]/
# 4. Actualizar claude/memoria/INDEX.md
# 5. Actualizar roadmap → "Completado"
# 6. Actualizar estado.log
# 7. Avisar
python claude/acciones/avisar.py "plan_XXX completado — revisa el resultado" normal
```

### Al guardar memoria

```bash
python claude/acciones/avisar.py "memoria de [modulo] guardada" suave
```

### /compact

1. Resumir en 5 lineas
2. Actualizar `claude/estado.log`
3. Actualizar `claude/RESUMEN.md`
4. Responder con resumen
5. Avisar:
```bash
python claude/acciones/avisar.py "checkpoint guardado" suave
```

---

## PROYECTO NUEVO (no existe roadmap.md)

Hacer estas preguntas de a una:
1. Que es el proyecto y para que sirve?
2. Para quien es?
3. Que stack se va a usar?
4. Cuales son los modulos principales?
5. Restricciones tecnicas o de tiempo?
6. Objetivo del MVP?

Al crear roadmap.md:
```bash
python claude/acciones/avisar.py "roadmap.md creado — revisa la vision" suave
```

---

## MEMORIA POR MODULO

`claude/memoria/[nombre_modulo]/resumen.md`:
```markdown
# Modulo: [nombre]
**Plan:** plan_XXX.md  **Fecha:** YYYY-MM-DD  **Estado:** Completado

## Que hace
## Archivos principales
## Como probarlo
```

`decisiones.md`:
```markdown
# Decisiones — [modulo]
## [Decision]
- Elegido: / Descartado: / Por que:
```

`estructura.md`:
```markdown
# Estructura — [modulo]
## Archivos creados/modificados
## Dependencias con otros modulos
## Variables de entorno necesarias
```

Fila para `claude/memoria/INDEX.md`:
```
| [nombre] | claude/memoria/[nombre]/ | plan_XXX.md | YYYY-MM-DD | [descripcion] |
```

---

## DETECCION DE STACK

| Indicador | Stack |
|---|---|
| `manage.py` + `frontend/vite.config.*` | Django + DRF + React + Vite |
| `manage.py` solo | Django + DRF |
| `pubspec.yaml` | Flutter |
| `app.json` + `expo` en `package.json` | React Native + Expo |
| `.sln` o `.csproj` o `.vbproj` | WinForms / C# / VB |
| `docker-compose.yml` con `n8n` | n8n incluido |
| `package.json` + `"vite"` sin `manage.py` | React + Vite standalone |

---

## FORMATO estado.log

```
[PROJ: nombre]
[STACK: tecnologias]
[PLAN: plan_XXX.md]
[ESTADO_PLAN: En ejecucion | Completado | Reabierto]
[LAST_TASK: descripcion]
[NEXT: proxima tarea o "sin plan activo"]
[DB: 0/1]
[DEBT: L/M/H]
```

---

## ESTANDARES DE CODIGO

```
# ARCHIVO: nombre
# QUE HACE: descripcion simple
# COMO ENCAJA: conexion con el resto
# PARA EDITAR: que saber antes de tocarlo
# DEPENDENCIAS: que necesita
```

---

## SEGURIDAD

- Nunca secrets en codigo — siempre `.env` + `.env.example`
- Si detecta secreto hardcodeado → parar y señalar antes de continuar
- Credenciales en `claude/acciones/credenciales.md`
- Antes de usar servicio externo → leer credenciales.md primero

---

## TERMINAL — permisos

| Accion | Permiso |
|---|---|
| `npm/pip install`, crear/editar archivos | Auto |
| `ls`, tests, `git status/diff/log` | Auto |
| `python claude/acciones/avisar.py` | Auto |
| `git merge`, `rm -rf` | Aprobacion explicita |
| `git commit` | NUNCA |
| `git push` | NUNCA |

---

## CLAUDE NUNCA

- Ejecuta `git commit` o `git push`
- Escribe secrets en codigo
- Arranca plan sin leer roadmap
- Usa credencial sin verificar en credenciales.md
- Termina una accion sin avisar
