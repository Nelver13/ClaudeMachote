# PROMPT DE MIGRACIÓN — Actualizar sistema IA existente
> Pega esto a cualquier IA (Claude, Kimi, Codex, Gemini) cuando el proyecto ya tiene sistema-ia/ instalado.
> Este prompt sirve tanto para actualizar una version vieja como para recuperar un sistema roto.

---

```
Vas a actualizar el sistema IA de este proyecto a la version mas reciente.
Sigue los pasos EN ORDEN. No saltes ninguno. Lee completo antes de empezar.

== REGLAS DE SEGURIDAD — LEE PRIMERO ==
NUNCA tocar:
- ESTADO.md (tiene el estado actual del proyecto)
- planes/ discusiones/ memoria/ handoff/ (trabajo activo)
- Codigo de produccion del proyecto
- El nombre del proyecto, stack, roles ya configurados
Si algo no esta claro → avisa urgente y para. No adivines.

== PASO 1 — Verificar estado actual ==
Ejecuta:
  python sistema-ia/acciones/migrar.py

Si da error "No such file" → el sistema esta roto, ir al PASO 1B.
Si corre bien → continuar al PASO 2.

== PASO 1B — Sistema roto (solo si migrar.py no existe) ==
Ejecuta en PowerShell:
  Rename-Item sistema-ia\acciones sistema-ia\acciones_old
  cd sistema-ia
  git checkout acciones/migrar.py
  cd ..
  python sistema-ia/acciones/migrar.py

== PASO 2 — Actualizar scripts y skills via git ==
Ejecuta:
  cd sistema-ia
  git checkout acciones/migrar.py
  git pull
  cd ..

Si git pull da error de merge en algun archivo:
  git checkout [archivo-con-conflicto]
  git pull

== PASO 3 — Verificar que los scripts llegaron ==
Ejecuta:
  python sistema-ia/acciones/avisar.py "test migracion" suave

Debe sonar + popup en Windows. Si no funciona → avisa urgente con el error exacto.

== PASO 4 — Verificar .claude/settings.json ==
Lee el archivo .claude/settings.json en la raiz del proyecto.
Debe tener:
- SessionStart hook: python sistema-ia/acciones/auto_setup.py
- PreToolUse hook: python sistema-ia/acciones/check_role.py

Si no existe .claude/settings.json → ejecuta:
  python sistema-ia/machote/instalar.py

Si existe pero le faltan los hooks → agrega solo los que falten, no reemplaces el archivo.

== PASO 5 — Aplicar NOVEDADES.md ==
Lee sistema-ia/NOVEDADES.md completo.
Ejecuta las instrucciones de la version mas reciente que aparece en ese archivo.
Sigue las reglas de seguridad de ese archivo (no tocar ESTADO.md, planes, etc.).

== PASO 6 — Verificar archivos raiz del proyecto ==
Compara cada archivo con su template en sistema-ia/machote/:
  CLAUDE.md    → compara con sistema-ia/machote/CLAUDE.md
  AGENTS.md    → compara con sistema-ia/machote/AGENTS.md
  INICIO.md    → compara con sistema-ia/machote/INICIO.md
  KIMI.md      → compara con sistema-ia/machote/KIMI.md (si usa Kimi)
  CODEX.md     → compara con sistema-ia/machote/CODEX.md (si usa Codex)
  GEMINI.md    → compara con sistema-ia/machote/GEMINI.md (si usa Gemini)

Para cada archivo:
- Si el proyecto tiene datos especificos (nombre, stack, roles) → conservarlos
- Si el template tiene secciones nuevas que no existen en el proyecto → agregarlas
- Si el template tiene secciones mejoradas → reemplazar SOLO esa seccion
- No borrar nada que sea especifico del proyecto

== PASO 7 — Confirmar ESTADO.md intacto ==
Lee ESTADO.md y confirma que tiene:
- [PROJ: nombre-del-proyecto] (no NOMBRE_PROYECTO)
- Roles configurados
- Modulo y plan actuales (si habia uno activo)

Si algo esta mal → avisame antes de corregir.

== PASO 8 — Avisar ==
python sistema-ia/acciones/avisar.py "Sistema IA actualizado — revision completa OK" normal

== PASO 9 — Reportar ==
Di en una sola respuesta corta:
- Version instalada
- Que se actualizo
- Si habia plan activo: confirmar que sigue intacto
- Si encontraste algo raro: mencionarlo

Reglas desde ya:
- Sin saludos ni relleno. Respuestas cortas.
- Una pregunta a la vez si necesitas aclarar algo.
- git commit/push/pull/add — NUNCA. Solo el humano toca git.
- Si un paso falla → avisa urgente con el error exacto y para.
```
