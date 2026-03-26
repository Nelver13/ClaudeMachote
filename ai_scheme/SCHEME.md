# AI Scheme - shared workflow

Este archivo es la "fuente de verdad" para el esquema de trabajo con IA.
Sirve como base para dos motores:
- Claude Code (lee `CLAUDE.md` y soporta imports con `@path`)
- Cursor (usa reglas bajo `.cursor/rules/`)

## Ciclo de trabajo (discusion -> plan -> ejecucion)

1. El arquitecto propone una idea (o un bug/mejora).
2. La IA crea/actualiza un archivo `disc_[tema].md` dentro de:
   - `claude/discusiones/creaciones/` (ideas/features)
   - `claude/discusiones/soluciones/` (bugs/gaps/mejoras)
3. En el chat el arquitecto dice solo:
   - `📝 disc_[tema].md — marca 1 cuando hayas leido`
4. Luego el arquitecto manda:
   - `1` para releer y avisar cambios
   - `revisa` para incorporar notas del arquitecto
   - `R:/ [texto]` para incorporar todo lo que se escribe y confirmar en 1 linea
   - `0` para aprobar y arrancar

Regla absoluta: `R:/` tiene prioridad. Todo se incorpora en el `.md` y se confirma antes de seguir.

## Modo ejecucion (solo tras `0`)

1. Marcar `disc_[tema].md` como `Estado: Aprobado`
2. Generar `claude/planes/plan_XXX.md` (checklist)
3. Ejecutar `python claude/acciones/avisar.py "... listo — arrancando" normal`
4. Ejecutar tareas bottom-up y tachar `[x]` al completar
5. Al terminar: cierre obligatorio (backup + estado.log + aviso)

## Notificaciones (sonido + canal)

- Los avisos se disparan con `python claude/acciones/avisar.py "mensaje" suave|normal|urgente`.
- Usar siempre un canal que funcione (ej: Windows toast + webhooks/push).
- Si un canal falla, mirar `claude/logs/notificaciones.log` para el motivo exacto.

## Seguridad y git

- Nunca escribir secrets hardcodeados en codigo; usar `.env` + `.env.example`.
- Prohibido `git commit` y `git push`.
- Prohibido subir `claude/` a git.

## "Memoria" para retomar

- `disc_[tema].md` y `plan_XXX.md` son notas vivas (memoria operativa).
- Al cerrar etapas, actualizar `claude/estado.log` y el resumen/memoria correspondiente.
