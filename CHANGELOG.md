# Changelog

## v2.6 — 2026-05-01
### Instalación limpia
- `instalar.py` ahora borra `sistema-ia/.git/` automáticamente — elimina repo anidado que contaminaba `git status`
- Borrar `sistema-ia/.gitignore` del repo clonado (es del machote, no del proyecto)
- Flujo simplificado: `git clone` + `python instalar.py` = listo
- `PROMPT_MIGRAR.md` → renombrado a `PROMPT_ACTUALIZAR.md` (re-clonar parcial en vez de git pull)

### Discusiones autoconsolidadas
- Nuevo formato fijo de discusión: Contexto (1 vez) + Decisiones cerradas (acumula) + Tema actual (se reemplaza)
- El archivo de discusión nunca crece más de ~80 líneas
- Al procesar `r/`: si cierra punto → va a Decisiones cerradas. Si necesita más → reformula Tema actual. Elimina el `r/`
- Chat del arquitecto: CERO resúmenes. Solo "Discusión actualizada" o "Discusión completada"

### Discusión primaria (0-vision)
- Al instalar se crea `discusiones/0-vision/v1.md` automáticamente
- Define roadmap del proyecto: qué es, stack, módulos, orden, roles
- Al completar → genera el plan-roadmap del proyecto

### Bug reporter universal
- Nuevo script `acciones/reportar.py` — hotkey Ctrl+Shift+B
- Captura screenshot de ventana activa (Pillow) + overlay de anotación (tkinter)
- Guarda en `discusiones/bugs/backlog.md` + `screenshots/bug-NNN.png`
- Funciona con CUALQUIER aplicación (OS-level, no depende del framework)
- Se activa automáticamente al iniciar sesión IA (auto_setup.py)
- Ciclo: bugs acumulan → arquitecto agrupa → discusión → plan → dev arregla

### Review post-plan (caveman)
- `finalizar_plan.py` ahora genera `memoria/[modulo]/review.md` automáticamente
- Formato ultra-comprimido: lista de cambios + checklist de verificación
- Limpia screenshots de bugs resueltos al cerrar plan de tipo fix

### Scripts de ejecución
- `run.bat` y `run.sh` creados en raíz del proyecto al instalar
- El arquitecto los configura según stack en discusión 0-vision
- El dev solo ejecuta el script para lanzar la app

### Git
- Permisos actualizados: `git log`, `git diff` ahora permitidos (además de `git status`)
- `git commit/push/add` sigue prohibido para IAs


### Mejorado: gitignore inteligente para trabajo en equipo
- Se actualizó `instalar.py` y `migrar.py` para que autoconfiguren el `.gitignore` del proyecto que recibe el sistema IA. 
- Ahora, `ESTADO.md`, `sistema-ia/discusiones/`, y `sistema-ia/planes/` **sí** se rastrean por defecto en Git para que el equipo pueda mantenerse sincronizado. 
- El resto del sistema (memoria, logs, scripts, agentes) permanecerá oculto y local para evitar ruido en el repositorio.

## v2.4 — 2026-04-18
### Reestructura (Fix B) — git pull ahora actualiza scripts directamente
- Scripts movidos a `acciones/` en la raíz del repo. Al clonar como `sistema-ia/`, quedan en `sistema-ia/acciones/` — directamente en git. `git pull` en `sistema-ia/` los actualiza sin pasos extra.
- Skills movidas a `.claude/skills/` en la raíz del repo (mismo principio).
- `migrar.py` simplificado: ya no copia scripts, solo crea carpetas faltantes y limpia pre-v2.0.
- `instalar.py` reescrito: pone `.claude/settings.json` en raíz del PROYECTO (no en sistema-ia/), no copia scripts (ya están en git).
- `auto_setup.py` y todos los scripts usan búsqueda robusta de raíz (search-upward por ESTADO.md) en lugar de `parents[N]` hardcodeado.
- `detectar_version_desfase()`: mensaje simplificado — solo dice `git pull`, no `migrar.py` (ya no es necesario para scripts).

---

## v2.3 — 2026-04-18
### Corregido (bloqueadores reportados en proyectos reales)
- **Arquitecto saltaba directo a dev sin generar plan ni PROMPT_DEV.** Paso `0` del modo-arquitecto ahora valida en disco que el plan exista y que `finalizar_discusion.py` haya generado `handoff/[modulo].json` antes de cambiar `[ESTADO_PLAN: Listo para dev]`. Si algún paso falla → avisa urgente y PARA.
- **Rutas rotas en skills:** `sistema-ia/.claude/ia/acciones/` reemplazado por `sistema-ia/acciones/` en modo-arquitecto y modo-dev (causaba que los scripts nunca se ejecutaran al ser llamados por la IA).
- **Avisos no disparaban en proyectos clonados:** `avisar.py` usaba `Path` sin importar + `parents[3]` del layout viejo. Fix: `from pathlib import Path` + búsqueda robusta de `ESTADO.md` subiendo hasta 6 niveles.
- **Scripts faltantes en clones viejos:** `migrar.py` ahora **REPLENECE** scripts/skills/assets (mp3s, caveman, credenciales) además de actualizar. Proyectos con clon incompleto se recuperan con `python sistema-ia/acciones/migrar.py`.
- **Ahorro de tokens no se respetaba:** concepto embebido directamente en las skills `modo-arquitecto` y `modo-dev` (sección "Estilo de respuesta en chat"). La skill `caveman` queda disponible pero opcional — ya no se depende de ella para la compresión por defecto.

### Agregado
- **Auto-detección de nueva versión:** `auto_setup.py` (SessionStart hook) compara `sistema-ia/VERSION` local vs `origin/main:VERSION` y avisa en el contexto de la sesión cuando hay actualización disponible, con el comando exacto a ejecutar. Silencioso si no hay red/git.
- `VERSION` en raíz del repo, `machote/VERSION`, `machote/sistema-ia/VERSION` — todos en `2.3`.
- Validación estricta de handoff en modo-arquitecto paso `0`.

---

## v2.2 — 2026-04-16
### Corregido
- Faltaban todos los scripts en `machote/sistema-ia/acciones/` (solo había 2)
- Agregados: avisar.py, cambiar_rol.py, cerrar_sesion.py, comprimir_discusion.py, finalizar_discusion.py, finalizar_plan.py, check_role.py, completar_tarea.py, check_secrets.py + mp3s
- Skill caveman agregado a machote
- Skills modo-dev y modo-arquitecto con flujo explícito de avisos y marcado de tareas [x]
- migrar.py inteligente: detecta versión, actualiza solo scripts/skills, no toca trabajo activo

---

## v2.1 — 2026-04-16
### Agregado
- `auto_setup.py` — SessionStart hook: detecta proyecto nuevo vs existente, carga contexto automático
- `cerrar_sesion.py` — guarda resumen comprimido del día en memoria/sesiones/
- `comprimir_discusion.py` — comprime temas cerrados en discusiones largas
- `migrar.py` — migra proyectos con sistema IA viejo al nuevo
- `PROMPT_INSTALAR.md` — prompt listo para instalar en proyecto nuevo
- `PROMPT_MIGRAR.md` — prompt listo para migrar proyecto viejo
- Skill `caveman` — modo comunicación ultra-comprimido (-75% tokens)

### Mejorado
- `avisar.py` — guarda checkpoint en ESTADO.md antes de notificar
- `finalizar_discusion.py` — genera JSON handoff además del PROMPT_DEV.txt
- `modo-dev/SKILL.md` — flujo explícito: ejecuta → marca [x] → actualiza ESTADO.md → avisa por tarea
- `modo-arquitecto/SKILL.md` — debate en archivo, avisa en cada paso, cierra sesión al aprobar
- `INICIO.md` — reducido a 35 líneas (carga lazy)
- `settings.json` — permisos automáticos + hook SessionStart

### Estructura nueva
- `sistema-ia/handoff/` — JSON de traspaso arquitecto → dev
- `sistema-ia/memoria/sesiones/` — contexto diario comprimido

---

## v2.0 — 2026-04-15
- Primer machote virgen multi-IA (Claude / Kimi / Codex / Gemini)
- Sistema arquitecto/dev con roles intercambiables
- Scripts base: avisar.py, cambiar_rol.py, finalizar_plan.py, finalizar_discusion.py
