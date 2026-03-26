# Cursor Scheme - shared workflow

Objetivo: que el agente de Cursor trabaje con el mismo esquema que Claude Code en `ai_scheme/SCHEME.md`.

## Flujo obligatorio

1. Si la tarea es una IDEA / feature:
   - Crear `modo_ia/claude/discusiones/creaciones/disc_[tema].md`
2. Si la tarea es un BUG / gap / mejora:
   - Crear `modo_ia/claude/discusiones/soluciones/disc_[tema].md`
3. Pedir confirmacion al usuario (marcas):
   - `1` para releer `.md`
   - `revisa` para incorporar notas
   - `R:/ [texto]` para incorporar todo lo escrito y confirmar en 1 linea
   - `0` para aprobar
4. Solo si el usuario aprueba con `0`:
   - Marcar `Estado: Aprobado` en la discusion
   - Generar `modo_ia/claude/planes/plan_XXX.md` como checklist
   - Ejecutar tareas siguiendo el checklist bottom-up
   - Al terminar: cierre obligatorio (backup + `claude/estado.log` + aviso)

## Notas

- `R:/` tiene prioridad absoluta y requiere incorporar todo en el `.md` antes de seguir.
- Nunca ejecutar `git commit` ni `git push`.
- Nunca escribir secrets hardcodeados en codigo.
- Discusiones y planes son notas vivas: funcionan como memoria para retomar.
