# PROMPT DE ACTUALIZACIÓN — Sistema Multi-IA v2.7
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
git clone https://github.com/Nelver13/ClaudeMachote.git sistema-ia-temp

== PASO 2 — Copiar solo scripts y skills ==
Copia SOLO estos directorios del clon nuevo al existente:
- sistema-ia-temp/sistema-ia/acciones/ → sistema-ia/acciones/ (reemplazar TODO el contenido)
- sistema-ia-temp/sistema-ia/.claude/skills/ → sistema-ia/.claude/skills/ (reemplazar todo)
- sistema-ia-temp/sistema-ia/VERSION → sistema-ia/VERSION

IMPORTANTE: En particular, confirma que existan estos archivos nuevos después de copiar:
- sistema-ia/acciones/guia.py
- sistema-ia/acciones/reportar.py

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

== PASO 6b — Crear estructura de bugs si no existe ==
Si NO existe la carpeta `sistema-ia/discusiones/bugs/`, créala AHORA:
- sistema-ia/discusiones/bugs/
- sistema-ia/discusiones/bugs/screenshots/
- Crea sistema-ia/discusiones/bugs/backlog.md con este contenido exacto:
  # Bugs Reportados
  > Usa Alt+R para reportar bugs con screenshot y descripción.

== PASO 7 — Instalar dependencias ==
Abre una terminal y ejecuta EXACTAMENTE este comando:
`pip install Pillow pynput SpeechRecognition pyaudio`
(Usa --user si te da error de permisos).

== PASO 8 — Actualizar run.bat y run.sh ==
Lee el ESTADO.md para ver el stack. Abre run.bat y run.sh (si existen) y actualízalos para levantar TODO el stack del proyecto (ej. React + Django).
IMPORTANTE: Siempre debes agregar o mantener la línea que levanta el reporter en background (`start /B python sistema-ia\acciones\reportar.py`). No lo borres.

== PASO 9 — Avisar ==
python sistema-ia/acciones/avisar.py "Sistema actualizado a vX.Y" normal

== PASO 10 — Mostrar Guía ==
Ejecuta la interfaz de novedades para el usuario:
python sistema-ia/acciones/guia.py

== PASO 11 — Reportar ==
- Versión instalada
- Qué se actualizó
- Plan activo: intacto o no
- Algo raro encontrado

== REGLAS GIT ==
✅ Permitido: git status / git clone (solo para el temporal)
❌ Prohibido: git commit / git push / git add
```
