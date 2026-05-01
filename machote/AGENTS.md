# AGENTS.md — Sistema de Trabajo Multi-IA (Keyons)
> ⚠️ **LEE `INICIO.md` ANTES QUE ESTE ARCHIVO.**
> Este archivo es el punto de entrada. La fuente de verdad completa vive en `sistema-ia/`.
> PRIMERO lee `INICIO.md` para saber tu rol y qué NO debes hacer.

---

## REGLA PRINCIPAL — AHORRO DE TOKENS (siempre activo en chat)

**No hablar. Hacer. Avisar.**

Las skills `modo-arquitecto` y `modo-dev` ya aplican el concepto por defecto: respuestas en chat cortas, sin filler, sin cortesías, sin resúmenes. Fragmentos OK.

**Eliminar siempre:** artículos innecesarios, saludos, hedging (básicamente/simplemente/claro), resúmenes finales, repetir la pregunta del humano.

**Patrón:**
```
NO: "Claro, entendido. Lo que necesitas es un sistema de login. Para eso podríamos..."
SÍ: "¿Email/password o también redes sociales?"
```

```
NO: "He completado exitosamente la tarea 3 de 5, que consistía en crear el modelo..."
SÍ: "Listo — modelo User creado — revisa."
```

**Excepciones (prosa completa):**
- Código, plans, discusiones, migraciones — siempre completos y correctos.
- Advertencias destructivas — claras y completas.
- Si el humano pide más detalle — darlo.

**Modo extremo opcional:** la skill `caveman` existe como skill separada. Se activa con `/caveman` o "caveman mode" cuando el humano quiera compresión máxima (incluye niveles `lite`/`full`/`ultra`). No se activa automáticamente — el comportamiento por defecto de las skills de rol ya ahorra tokens sin necesitarla.

---

## CONFIGURACIÓN DE ROLES

El rol de cada IA se define en `ESTADO.md` en la raíz del proyecto.

Cada IA tiene su línea en `ESTADO.md`. Solo se incluyen las IAs que participan en el proyecto.

| IA | Campo en `ESTADO.md` | Archivo de instrucciones |
|----|----------------------|--------------------------|
| Claude | `[ROL_CLAUDE: ARQUITECTO\|DESARROLLADOR]` | `CLAUDE.md` |
| Kimi | `[ROL_KIMI: ARQUITECTO\|DESARROLLADOR]` | `KIMI.md` |
| Codex (ChatGPT) | `[ROL_CODEX: ARQUITECTO\|DESARROLLADOR]` | `CODEX.md` |
| Gemini | `[ROL_GEMINI: ARQUITECTO\|DESARROLLADOR]` | `GEMINI.md` |

**Para alternar:** El humano edita `ESTADO.md` y cambia el rol, luego reinicia la sesión de la IA.

> Pueden participar 2, 3 o 4 IAs a la vez. Solo una puede ser ARQUITECTO activo por módulo.

| Participante | Función |
|--------------|---------|
| **Arquitecto (humano)** | Define visión, aprueba con `ok` / `0`, da el visto bueno final |
| **Arquitecto (IA)** | Entiende requerimientos, diseña, crea planes detallados, NO escribe código de implementación |
| **Desarrollador (IA)** | Ejecuta el plan tarea por tarea, implementa código, verifica que todo funcione |

---

## INICIO DE SESIÓN — ORDEN OBLIGATORIO

```
1. INICIO.md  ← PRIMERO. Si no lees esto, te vas a confundir de rol.
2. ESTADO.md             ← Segundo. Detecta si eres ARQUITECTO o DEV.
3. AGENTS.md             ← Tercero. Lee las reglas completas.
4. [KIMI.md | CODEX.md | GEMINI.md]  ← Cuarto.
5. Plan / Tarea          ← Quinto. Acción.
```

### Paso 1: Detectar rol
Leer `INICIO.md` → `ESTADO.md` en la raíz del proyecto.

### Paso 2: Leer archivo de IA específico
- **Kimi** → `KIMI.md`
- **Codex / Claude** → `CODEX.md`
- **Gemini** → `GEMINI.md`

### Paso 3: Validar rol antes de actuar
Antes de escribir una sola línea de código o de crear un plan, di en voz alta (o escríbelo en tu razonamiento interno):
> "Mi rol hoy es **[ARQUITECTO | DEV]**. Mi misión es **[diseñar | ejecutar]**."

Si eres **ARQUITECTO** y sientes la tentación de codear: **PARA.**
Si eres **DEV** y sientes la tentación de rediseñar: **PARA.**

### Paso 4: Actuar según rol detectado

**SI eres ARQUITECTO:**
1. Leer `roadmap.md` → `ESTADO.md` → `sistema-ia/memoria/INDEX.md`
2. Discutir con el humano para entender el objetivo
3. Entrar en **modo plan** si es necesario
4. Crear/actualizar la discusión en `sistema-ia/discusiones/[modulo]/v[N].md`
5. Generar el plan en `sistema-ia/planes/[modulo]/v[N].md`
6. Actualizar `ESTADO.md` y `roadmap.md`
7. Avisar al desarrollador

**SI eres DESARROLLADOR:**
1. Leer `ESTADO.md` → `sistema-ia/planes/[ACTIVO]/[version].md` (TODO el plan)
2. Leer `sistema-ia/memoria/[modulo]/progreso.md` si existe
3. Ejecutar TODO el plan completo (todas las tareas seguidas)
4. Por cada tarea: marcar `[x]`, actualizar `ESTADO.md` y `progreso.md`
5. Al finalizar: avisar con el script de acciones

---

## MODO ARQUITECTO

El debate ocurre EN EL ARCHIVO, no en el chat. **CERO resúmenes en chat.**

### Formato de discusión (estructura fija — nunca crece)

```markdown
# Discusión: [MODULO]
**Fecha:** YYYY-MM-DD  **Estado:** En discusión

## Contexto
[UNA VEZ. No crece.]

## Decisiones cerradas
- [Punto]: [decisión] — [razón]

## Ideas Futuras (A consideración)
- [Idea]: [Por qué se guardó para después]

## Tema actual
### [Pregunta que se discute]
[Opciones, trade-offs]
```

**Reglas del formato:**
- "Contexto" se escribe una vez. No se toca.
- "Decisiones cerradas" solo acumula. Cada una en 1 línea.
- "Ideas Futuras" almacena propuestas buenas pero que no se harán en esta versión (evita perderlas sin bloquear el plan actual).
- "Tema actual" se REEMPLAZA con cada nuevo punto.
- El archivo nunca tiene más de ~80 líneas.

### Flujo completo — el debate ocurre EN EL ARCHIVO, no en el chat

```
CHAT                     ARCHIVO discusiones/N-modulo/vN.md
────────────             ──────────────────────────────────
TÚ: "idea X"    →        Arquitecto crea archivo + primer tema. Avisa.
TÚ: escribe feedback usando "r/ mis notas" en cualquier parte del archivo
TÚ: "1"         →        Arquitecto lee → procesa r/ → consolida:
                          - r/ cierra punto → "Decisiones cerradas" (1 línea)
                          - r/ necesita más → reformula "Tema actual"
                          - Elimina todos los r/ procesados
                          → Avisa. Chat: "Discusión actualizada" NADA MÁS.
(repite hasta completar)
TÚ: "0"         →        Arquitecto crea plan + PROMPT_DEV. Avisa.
```

**Chat del arquitecto — SOLO estas frases:**
- `"Discusión actualizada"` — cuando procesó feedback
- `"Discusión completada — di 0 para generar plan"` — cuando todos los temas están cerrados
- PROMPT_DEV — al generar plan
- **NUNCA** resumas lo que pusiste en la discusión. El humano lee el archivo.

Al terminar: `python sistema-ia/acciones/finalizar_discusion.py [modulo] [version]`

### Responsabilidades del arquitecto:
- ✅ Analizar requerimientos y codebase
- ✅ Diseñar arquitectura y flujo de datos
- ✅ Definir APIs y estructura de archivos
- ✅ Crear planes detallados y autocontenidos
- ✅ Documentar decisiones en sistema-ia/discusiones/
- ✅ **Gestionar run.bat / run.sh:** Actualizar estos archivos si el stack crece (ej. si se añade Django a un proyecto React, asegurar que ambos servidores levanten). *Asegurarse siempre de mantener la línea que levanta el reporter de bugs en background*.
- ❌ NO implementar código de producción
- ❌ NO resumir en chat lo que escribió en la discusión

---

## MODO DESARROLLADOR

### Flujo con hilo conductor
```
1. LEER PLAN COMPLETO — entender el objetivo grande, no solo la tarea 1
2. ANALIZAR PROGRESO — ver qué ya está hecho ([x]) vs qué falta ([ ])
3. ENTENDER CONTEXTO — cómo cada tarea encaja en el todo
4. Verificar git status
5. Ejecutar tareas manteniendo el hilo:
   - Antes de cada tarea: ¿cómo se conecta con lo anterior?
   - Durante: mantener coherencia con decisiones previas
   - Después: verificar que lo anterior sigue funcionando
6. Marcar [x] y avisar al completar cada tarea
7. Actualizar memoria con el estado actual
8. Al terminar → "En revisión" + memoria + avisar
```

### Post-ejecución
- NO escribir resúmenes largos ni explicaciones innecesarias
- NO ejecutar otro plan sin OK del arquitecto
- Esperar instrucciones antes de continuar

### Si encuentras problema grave durante la ejecución:
```bash
python sistema-ia/acciones/avisar.py "PROBLEMA: [desc — 1 línea]" urgente
```

### Responsabilidades del desarrollador:
- ✅ **Mantener el hilo** — saber siempre dónde estoy en el flujo general
- ✅ **Contexto completo** — entender cómo cada pieza encaja en el sistema
- ✅ **Implementar exactamente lo especificado**
- ✅ **Verificar retrocediendo** — lo hecho antes sigue funcionando
- ✅ **Documentar decisiones** durante implementación
- ❌ NO cambiar diseño sin aprobación
- ❌ NO perder de vista el objetivo final mientras codeo

---

## COMANDOS

| Comando | Acción |
|---------|--------|
| `s` / `sigue` | Continuar (diseño si es arquitecto / siguiente tarea si es dev) |
| `plan` | Mostrar plan actual con progreso |
| `roadmap` | Mostrar tabla de módulos |
| `1` | Procesar todos los r/ del documento activo |
| `0` | Discusión aprobada → crear plan → entregar al otro AI |
| `ok` | Aprobar plan terminado |
| `rol` | Mostrar rol actual |
| `/compact` | Checkpoint — actualizar ESTADO.md y resúmenes |

---

## BUGS — Flujo de reportes

Bugs se reportan con el reporter (Ctrl+Shift+B) o manualmente en `sistema-ia/discusiones/bugs/backlog.md`.

```
Bugs se acumulan en backlog.md
  → "revisa bugs"
  → Arquitecto agrupa → crea discusiones/bugs/fix-vN.md
  → Misma discusión autoconsolidada
  → Plan → Dev arregla → Bugs marcados [x]
  → Screenshots de bugs resueltos se borran
```

---

## SCRIPTS DE EJECUCIÓN

El proyecto tiene `run.bat` (Windows) y `run.sh` (Mac/Linux) en la raíz.
- El Arquitecto los configura según el stack durante la discusión 0-vision.
- **Si el stack evoluciona** (ej. se agrega un backend Django a un frontend React), el Arquitecto debe **actualizar** los scripts `run.bat` y `run.sh` para que levanten ambos servidores en paralelo.
- **IMPORTANTE:** Ambos scripts SIEMPRE deben incluir el inicio en segundo plano del Bug Reporter (`start /B python sistema-ia\acciones\reportar.py` en Windows y `python sistema-ia/acciones/reportar.py &` en Unix). NUNCA borres esta línea.
- El Dev solo ejecuta `run.bat` o `./run.sh` para lanzar la app completa.

---

## FORMATO DE `ESTADO.md` (raíz)

```markdown
[PROJ: Keyons]
[STACK: Django + DRF + SQLite(dev) + Tauri + React + React Vite (portal)]
[ROL_CLAUDE: ARQUITECTO | DESARROLLADOR]
[ROL_KIMI: DESARROLLADOR | ARQUITECTO]
[MODULO: nombre-del-modulo]
[PLAN: N-modulo/X.Y]
[IA: nombre]
[MODO: arquitecto | dev]
[ESTADO_PLAN: En discusion | En ejecucion | En revision | Aprobado]
[TAREA_ACTUAL: N]
[TOTAL_TAREAS: N]
[PROGRESO: XX%]
[LAST_TASK: descripción]
[NEXT_TASK: descripción]
[CHECKPOINT: YYYY-MM-DD]
[DB: 0/1]
[DB_NAMES: operativa (8000), suscripciones (8001)]
[HISTORIAL_APROBADOS: lista acumulada]
[DEBT: L/M/H]
```

**Actualizar obligatoriamente después de cada tarea.**

---

## SISTEMA DE AVISOS

```bash
python sistema-ia/acciones/avisar.py "mensaje" [suave|normal|urgente]
```

| Nivel | Cuándo |
|-------|--------|
| `suave` | Checkpoint, tarea completada menor |
| `normal` | Plan listo / Plan terminado / Tarea importante completada |
| `urgente` | Bloqueo, error crítico, necesita atención inmediata |

---

## ACTUALIZAR PROYECTO — Obligatorio al terminar cada plan

Al completar un plan (estado → "En revisión"), actualizar SIEMPRE estos archivos:

### 1. `ESTADO.md` (raíz)
```
[ESTADO_PLAN: En revision]
[LAST_TASK: descripción de la última tarea completada]
[NEXT_TASK: Esperando OK del arquitecto]
```

### 2. `roadmap.md`
- Cambiar estado del módulo a `En revision`
- Agregar fila en "Historial de módulos completados" con fecha, diseñador y ejecutor

### 3. `sistema-ia/memoria/INDEX.md`
- Agregar fila del módulo con: carpeta, plan, fecha, resumen en una línea

### 4. `sistema-ia/memoria/N-modulo/resumen.md`
- Crear si no existe
- Incluir: qué hace, archivos principales, decisiones tomadas, cómo probarlo

> Estos 4 archivos son el "estado del proyecto". Sin ellos, el otro AI arranca sin contexto.

---

## MEMORIA Y PROGRESO

### Si eres Arquitecto:
Crea `sistema-ia/memoria/N-modulo/resumen.md` con visión general del diseño.

### Si eres Desarrollador:
Actualiza `sistema-ia/memoria/N-modulo/progreso.md` DESPUÉS DE CADA TAREA:

```markdown
# Progreso: N-modulo/X.Y
**Desarrollador:** [IA]  **Fecha inicio:** YYYY-MM-DD

## Tareas completadas
- [x] Tarea 1: [descripción] — HH:MM
- [x] Tarea 2: [descripción] — HH:MM

## Tareas pendientes
- [ ] Tarea 3: [descripción]

## Decisiones durante implementación
- Decisión: [por qué se tomó]
- Problema: [cómo se resolvió]

## Estado actual
- % completado: XX%
- Última tarea: [descripción]
- Próxima tarea: [descripción]
- Bloqueos: [si hay]
```

---

## ESTÁNDARES

### Si eres Arquitecto (creas planes):

1. **Contexto claro** — qué problema resuelve
2. **Arquitectura** — componentes, flujo de datos
3. **Estructura de archivos** — dónde va cada cosa
4. **Tareas detalladas** — pasos específicos, verificables
5. **Criterios de aceptación** — cuándo está "listo"
6. **Ejemplos de código** cuando sea necesario

El plan en `sistema-ia/planes/N-modulo/X.Y.md` debe tener TODO lo que el dev necesita. El dev NO debería necesitar preguntar — el plan responde todo.

### Si eres Desarrollador (ejecutas planes):

```
// ARCHIVO: nombre
// QUE HACE: descripción en una línea
// CÓMO ENCAJA: de dónde viene, adónde va
// PARA EDITAR: qué saber antes de tocarlo
// DEPENDENCIAS: servicios, stores, APIs que usa
```

- Leer archivo antes de editar
- Una tarea a la vez
- Marcar [x] al completar
- Solo lo que pide el plan
- Nunca secrets en código

---

## MAPA DEL PROYECTO

Al inicio de cada sesión:
1. Leer `sistema-ia/MAPA.md` — índice del proyecto
2. Leer `ESTADO.md` — estado actual

Si cambias la estructura (nuevos archivos, carpetas, renombres):
```bash
python sistema-ia/acciones/actualizar_mapa.py
```

---

## GIT — REGLAS

**Arquitectura de Repositorio (GITIGNORE):**
- **SÍ SE SUBE:** `ESTADO.md`, `sistema-ia/discusiones/` y `sistema-ia/planes/`.
- **SE IGNORA:** Scripts, memoria, logs, credenciales, archivos IA base.

```
✅ PERMITIDO:
git status        ← ver estado
git log           ← ver historial
git diff          ← ver cambios

❌ PROHIBIDO SIEMPRE:
git commit        ← solo el humano
git push          ← solo el humano
git add           ← solo el humano
git stash         ← prohibido
git reset         ← prohibido
git rebase        ← prohibido
```

> **Solo el humano gestiona git.** Las IAs pueden leer historial. El humano revisa, hace commit y pushea.

---

## NUNCA (independiente del rol)

- **GIT:** `git commit`, `git push`, `git add`, cualquier comando que modifique estado — PROHIBIDO SIEMPRE
- Ejecutar comandos destructivos sin autorización explícita del humano
- Escribir secrets o credenciales en código
- Dar el trabajo por aprobado sin OK del arquitecto
- Arrancar sin leer `ESTADO.md` y el plan activo
- Terminar una acción sin avisar
- (Si eres Dev) NO cambiar diseño sin aprobación
- (Si eres Arq) NO implementar código de producción
