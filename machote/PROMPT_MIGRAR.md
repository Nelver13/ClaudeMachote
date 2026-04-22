# PROMPT DE MIGRACIÓN / ACTUALIZACIÓN — Sistema IA
> Pega esto a cualquier IA (Claude, Kimi, Codex, Gemini, Antigraviton, etc.)
> Sirve para: actualizar version vieja, recuperar sistema roto, o sincronizar cambios nuevos.

---

```
Vas a actualizar el sistema IA de este proyecto. git@github.com:Nelver13/ClaudeMachote.git
Lee TODO antes de empezar. Sigue el orden exacto.

== REGLAS — NUNCA TOCAR ==
- ESTADO.md
- planes/ discusiones/ memoria/ handoff/
- Codigo de produccion del proyecto
- Nombre del proyecto, stack, roles configurados
Si tienes duda → para y avisa. No adivines.

== PASO 1 — git pull en sistema-ia/ ==
Ejecuta:
  cd sistema-ia
  git pull
  cd ..
  python sistema-ia/acciones/migrar.py

Esto actualiza automaticamente:
  sistema-ia/acciones/     ← todos los scripts (incluyendo el .gitignore automático)
  sistema-ia/.claude/skills/ ← skills modo-arquitecto, modo-dev, caveman

Si git pull da error de merge:
  cd sistema-ia
  git checkout [archivo-con-conflicto]
  git pull
  cd ..

Si acciones/ no existe o esta vacio (sistema roto):
  cd sistema-ia
  git checkout acciones/migrar.py
  cd ..
  python sistema-ia/acciones/migrar.py
  → luego volver al PASO 1

== PASO 2 — Verificar que los scripts funcionan ==
Ejecuta:
  python sistema-ia/acciones/avisar.py "test actualizacion" suave

Debe sonar + popup. Si falla → avisa con el error exacto y para.

== PASO 3 — Verificar .claude/settings.json en raiz del PROYECTO ==
Lee .claude/settings.json (en la raiz del proyecto, NO en sistema-ia/).

Debe contener exactamente esto:
{
  "permissions": { "defaultMode": "acceptEdits", "allow": ["Bash(python*)", "Read(**)", "Glob(**)", "Grep(**)", ...] },
  "hooks": {
    "SessionStart": [{"hooks": [{"type": "command", "command": "python sistema-ia/acciones/auto_setup.py"}]}],
    "PreToolUse": [{"matcher": "Edit|Write", "hooks": [{"type": "command", "command": "python sistema-ia/acciones/check_role.py"}]}]
  }
}

Si no existe .claude/settings.json en la raiz → crealo con ese contenido.
Si existe pero le faltan los hooks → agrega solo los que falten.

== PASO 4 — Leer y aplicar NOVEDADES.md ==
Lee sistema-ia/NOVEDADES.md completo.
Aplica las instrucciones de la version mas reciente.
El archivo dice exactamente que tocar y que no.

== PASO 5 — Verificar archivos raiz del proyecto ==
Verifica que existen estos archivos en la raiz del proyecto:
  INICIO.md / AGENTS.md / ESTADO.md / CLAUDE.md (o el .md de la IA que uses)

Para cada uno que exista:
- Lee el archivo del proyecto
- Lee la VERSION de git: git -C sistema-ia show HEAD:machote/[archivo]
- Si el template tiene secciones que NO estan en el proyecto → agregarlas
- Si el proyecto tiene datos especificos (nombre, stack, roles, historial) → conservarlos
- NO borrar nada especifico del proyecto
- Si el archivo no existe en el proyecto → crearlo con el contenido del template

== PASO 6 — Confirmar ESTADO.md intacto ==
Lee ESTADO.md. Verifica:
- [PROJ: nombre] (no dice NOMBRE_PROYECTO)
- Roles configurados
- Plan activo intacto (si habia uno)
Si algo esta mal → avisame antes de corregir.

== PASO 7 — Avisar ==
python sistema-ia/acciones/avisar.py "Sistema IA actualizado OK" normal

== PASO 8 — Reportar en una sola respuesta ==
- Version instalada
- Que se actualizo (scripts, skills, archivos .md)
- Plan activo: intacto o no
- Algo raro que encontraste

== REGLAS GIT ==
✅ Permitido: git status / git log / git pull / git diff
❌ Prohibido: git commit / git push / git add / git stash / git reset
El humano hace commit y push. Tu solo jalas.

== SI ALGO FALLA ==
python sistema-ia/acciones/avisar.py "ERROR: [descripcion exacta]" urgente
Para. No continues hasta que el humano responda.
```
