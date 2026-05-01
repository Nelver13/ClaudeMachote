# PROMPT DE ACTUALIZACIÓN — Sistema Multi-IA v2.6
> Pega esto a cualquier IA para actualizar el sistema a la última versión.
> Ya no usa git pull — se re-clona y copia solo lo necesario.

---

```
Actualiza el sistema IA de este proyecto.

== REGLAS — NUNCA TOCAR ==
- ESTADO.md
- discusiones/ planes/ memoria/ handoff/
- Código de producción del proyecto
- Nombre del proyecto, stack, roles configurados
Si tienes duda → para y avisa. No adivines.

== PASO 1 — Re-clonar en temporal ==
git clone git@github.com:Nelver13/ClaudeMachote.git sistema-ia-temp

== PASO 2 — Copiar solo scripts y skills ==
Copia SOLO estos directorios del clon nuevo al existente:
- sistema-ia-temp/acciones/ → sistema-ia/acciones/ (reemplazar todo)
- sistema-ia-temp/.claude/skills/ → sistema-ia/.claude/skills/ (reemplazar todo)
- sistema-ia-temp/VERSION → sistema-ia/VERSION

NO tocar: discusiones/ planes/ memoria/ handoff/ ESTADO.md

== PASO 3 — Borrar el clon temporal ==
Elimina sistema-ia-temp/ completamente.

== PASO 4 — Verificar ==
python sistema-ia/acciones/avisar.py "test actualizacion" suave
Debe sonar + popup. Si falla → avisa con error exacto.

== PASO 5 — Leer NOVEDADES.md ==
Lee sistema-ia/NOVEDADES.md y aplica las instrucciones de la versión nueva.

== PASO 6 — Verificar archivos raíz ==
Verifica que existen: INICIO.md, AGENTS.md, ESTADO.md
Si faltan → copiar de sistema-ia-temp/machote/ (antes de borrarlo)
NO sobrescribir los que ya existen con datos del proyecto.

== PASO 7 — Avisar ==
python sistema-ia/acciones/avisar.py "Sistema actualizado a vX.Y" normal

== PASO 8 — Reportar ==
- Versión instalada
- Qué se actualizó
- Plan activo: intacto o no
- Algo raro encontrado

== REGLAS GIT ==
✅ Permitido: git status / git clone (solo para el temporal)
❌ Prohibido: git commit / git push / git add
```
