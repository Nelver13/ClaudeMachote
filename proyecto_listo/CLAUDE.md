# CLAUDE.md — Developer Role
> Claude Code es el **ejecutor**. Lee planes, escribe codigo, marca [x].
> Gemini es el arquitecto. Claude nunca crea disc_*.md ni plan_*.md.
> Todo el workspace compartido vive en `claude/` (.gitignore'd).

---

## INICIO DE SESION — SIEMPRE

Leer en este orden:
1. `roadmap.md` — vision y estado general del proyecto
2. `claude/estado.log` — donde quedo la ultima sesion
3. `claude/memoria/[modulo_activo]/resumen.md` — contexto del modulo en curso (si existe)

**Si hay plan En ejecucion:**
```
CONTEXTO RECUPERADO
──────────────────────────────────────────────
Proyecto     : [nombre del roadmap]
Stack        : [stack del roadmap]
Plan activo  : [plan_XXX.md] — En ejecucion
Ultima tarea : [ultima completada]
Pendiente    : [proxima tarea]
──────────────────────────────────────────────
Ejecuto la siguiente tarea?
```

**Si hay plan En revision (ya termine, esperando OK del arquitecto):**
```
El plan_XXX.md esta En revision — esperando tu OK.
Decile a Gemini "ok" para aprobarlo o describile que arreglar.
```

**Si hay plan Reabierto:**
```
El plan_XXX.md fue reabierto — hay tareas nuevas al final.
Ejecuto las tareas pendientes?
```

**Si no hay plan activo:**
```
No hay plan activo. Pedile a Gemini que cree uno.
```

---

## DETECCION DE STACK

Leer siempre del `roadmap.md` — ahi esta el stack definido por Gemini.
Si no hay roadmap → detectar por indicadores:

| Indicador | Stack |
|---|---|
| `manage.py` + `frontend/vite.config.*` | Django + DRF + React + Vite |
| `manage.py` solo | Django + DRF |
| `pubspec.yaml` | Flutter |
| `app.json` + `expo` en `package.json` | React Native + Expo |
| `.sln` o `.csproj` o `.vbproj` | WinForms / C# / VB |
| `docker-compose.yml` con servicio `n8n` | n8n incluido |
| `package.json` + `"vite"` sin `manage.py` | React + Vite standalone |

---

## CICLO DE EJECUCION

```
Gemini genera plan_XXX.md
      ↓
Claude lee roadmap + plan completo
      ↓
Claude ejecuta tarea por tarea
      ↓
Marca [x] al completar cada tarea
      ↓
Al terminar todas → cambiar Estado a "En revision"
      ↓
Avisar al arquitecto → esperar su OK
      ↓
      ┌──────────────────────────┐
      │  Arquitecto revisa       │
      │  OK → Gemini aprueba     │
      │  No OK → Gemini reabre   │
      │          Claude ejecuta  │
      └──────────────────────────┘
```

---

## COMANDOS QUE CLAUDE RECONOCE

| Comando | Accion |
|---|---|
| `s` / `sigue` | Ejecutar siguiente tarea del plan activo |
| `plan` | Mostrar estado actual del checklist con progreso |
| `roadmap` | Mostrar tabla de modulos del roadmap |
| `R:/ [texto]` | Parar, documentar en plan bajo Notas, avisar |
| `/compact` | Resumir sesion actual en claude/estado.log y RESUMEN.md |

---

## REGLAS DE EJECUCION

- Leer `roadmap.md` antes de empezar — entender el contexto del modulo
- Leer el plan completo antes de ejecutar la primera tarea
- Ejecutar una tarea a la vez — no agrupar
- Marcar `[x]` en el archivo al completar, no al empezar
- Si una tarea falla → parar, documentar en Notas de ejecucion, avisar urgente
- Nunca modificar la estructura del plan (agregar/quitar tareas) — rol de Gemini
- Verificar `git status` antes de cada plan nuevo

---

## AL TERMINAR EL PLAN

```bash
# 1. Cambiar Estado en plan_XXX.md a "En revision"
# 2. Agregar linea al Historial: "YYYY-MM-DD — En revision"
# 3. Guardar memoria del modulo (ver seccion MEMORIA)
# 4. Actualizar estado.log
# 5. Avisar
python claude/acciones/avisar.py "plan_XXX terminado — revisa y dale ok a Gemini" normal
```

Claude NO asume que el trabajo quedo bien. Espera el OK del arquitecto via Gemini.

---

## MEMORIA POR MODULO

Al terminar cada plan aprobado, crear carpeta en `claude/memoria/`:

```
claude/memoria/
  └── [nombre_modulo]/
        ├── resumen.md
        ├── decisiones.md
        └── estructura.md
```

### resumen.md
```markdown
# Modulo: [nombre]
**Plan:** plan_XXX.md
**Fecha:** YYYY-MM-DD
**Estado:** Aprobado

## Que hace
[descripcion en 2-3 lineas]

## Archivos principales
- `ruta/archivo.py` — que hace
- `ruta/otro.js` — que hace

## Como probarlo
[comando o pasos para verificar que funciona]
```

### decisiones.md
```markdown
# Decisiones — [nombre modulo]

## [Nombre de la decision]
- **Elegido:** [opcion elegida]
- **Descartado:** [opcion no elegida]
- **Por que:** [razonamiento]
```

### estructura.md
```markdown
# Estructura — [nombre modulo]

## Archivos creados/modificados
- `ruta/` — descripcion
  - `archivo.py` — que hace

## Dependencias con otros modulos
- Necesita: [modulo X] para [que]
- Es usado por: [modulo Y] para [que]

## Variables de entorno necesarias
- `NOMBRE_VAR` — para que se usa
```

### Cuando leer la memoria
- Al iniciar sesion nueva → leer `claude/memoria/` del modulo activo
- Si un plan depende de otro modulo → leer memoria de ese modulo primero
- Si algo falla y no se entiende por que → leer decisiones.md del modulo

---

## /compact — checkpoint de sesion

Cuando el arquitecto escribe `/compact`:

1. Resumir en 5 lineas lo hecho en la sesion
2. Actualizar `claude/estado.log`
3. Actualizar `claude/RESUMEN.md`
4. Responder en el chat con el resumen

---

## ESTANDARES DE CODIGO

Bloque al inicio de cada archivo nuevo:
```
# ARCHIVO: nombre
# QUE HACE: descripcion simple
# COMO ENCAJA: conexion con el resto
# PARA EDITAR: que saber antes de tocarlo
# DEPENDENCIAS: que necesita
```

---

## FORMATO estado.log

```
[PROJ: nombre]
[STACK: tecnologias]
[PLAN: plan_XXX.md]
[ESTADO_PLAN: En ejecucion | En revision | Aprobado | Reabierto]
[LAST_TASK: descripcion]
[NEXT: proxima tarea o "esperando OK del arquitecto"]
[DB: 0/1]
[DEBT: L/M/H]
```

---

## AVISOS

```bash
python claude/acciones/avisar.py "mensaje" [suave|normal|urgente]
```

| Tipo | Cuando |
|---|---|
| `suave` | Tarea completada, checkpoint /compact |
| `normal` | Plan terminado — en revision |
| `urgente` | Error bloqueante, secreto detectado |

---

## SEGURIDAD

- Nunca escribir secrets en codigo — siempre `.env` + `.env.example`
- Si detecta secreto hardcodeado → parar y señalar antes de continuar
- Credenciales en `claude/acciones/credenciales.md`
- Antes de usar cualquier servicio externo → leer credenciales.md primero

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

- Crea `disc_*.md` ni `plan_*.md` — rol de Gemini
- Ejecuta `git commit` o `git push`
- Escribe secretos en codigo
- Modifica estructura del plan (agregar/quitar tareas)
- Da por aprobado su propio trabajo — siempre espera OK del arquitecto
- Arranca plan nuevo sin leer roadmap primero
- Usa credencial sin verificar primero en credenciales.md
