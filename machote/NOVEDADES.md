# NOVEDADES — Instrucciones de actualización para la IA
> auto_setup.py inyecta este archivo cuando detecta version nueva.
> NOTA: machote/ se borra automaticamente despues del pull — las instrucciones
> deben tener el contenido exacto inline, sin referenciar sistema-ia/machote/.

---

## REGLAS GENERALES (aplican a todas las versiones)

### NUNCA tocar:
- ESTADO.md
- planes/ discusiones/ memoria/ handoff/
- Nombre del proyecto, stack, roles configurados
- Codigo de produccion del proyecto

### SIEMPRE antes de editar un .md del proyecto:
1. Leer el archivo completo primero
2. Aplicar SOLO lo que dice la instruccion
3. Si el contenido ya existe → saltar (no duplicar)
4. Si tienes duda → avisar urgente y parar

### Al terminar todas las instrucciones:
```bash
python sistema-ia/acciones/avisar.py "Proyecto actualizado a v[X.Y]" normal
```

---

## v2.6

### Qué cambió
- Instalación limpia: `instalar.py` borra automáticamente `.git/` de `sistema-ia/` (adiós repos anidados).
- Discusiones fijas: el Arquitecto ahora consolida y reescribe `r/` en discusiones de tamaño fijo (max ~80 líneas). CERO resúmenes en chat.
- Bug Reporter: script `reportar.py` activable con `Alt+R`. Se inicia solo en background en los scripts `run.bat` / `run.sh` que se generan.
- Dictado por voz (Push-to-Talk): El Bug Reporter ahora permite dictar bugs con voz usando la librería `SpeechRecognition`.
- Guía interactiva: Al finalizar `instalar.py`, se despliega una interfaz gráfica de bienvenida.
- Review Caveman: al completar un plan, se genera `memoria/[modulo]/review.md` ultracompacto y se limpian screenshots de bugs.

### Instrucciones para la IA (si actualizas un proyecto):

**1. Verificar AGENTS.md**
Lee la sección del Arquitecto en `AGENTS.md` y `SKILL.md` (modo-arquitecto). El comportamiento del Arquitecto ahora es de **Cero Resúmenes** y reemplazo total de la sección "Tema actual" en las discusiones al procesar feedbacks `r/`.
Asegúrate de que la IA conozca la regla de no aumentar indefinidamente el archivo de discusión.
Además, verifica que la plantilla de discusión en `AGENTS.md` contenga la sección `## Ideas Futuras (A consideración)`. Si no la tiene, agrégala justo debajo de `## Decisiones cerradas`. Esta sección sirve para almacenar propuestas a futuro sin bloquear el trabajo actual.

**2. Verificar dependencias del Bug Reporter**
Abre una terminal y ejecuta: `pip install Pillow pynput SpeechRecognition pyaudio --quiet` (si falla o tarda, usa el flag `--user`).

**3. Verificar scripts de ejecución en la raíz**
Si el proyecto no tiene `run.bat` o `run.sh` en su raíz, créalos. Asegúrate de incluir la línea para lanzar el reporter:
- Windows (`run.bat`): `start /B python sistema-ia\acciones\reportar.py`
- Linux/Mac (`run.sh`): `python sistema-ia/acciones/reportar.py &`

**4. Avisar**
```bash
python sistema-ia/acciones/avisar.py "Proyecto actualizado a v2.6" normal
```

---

## v2.5

### Que cambio
- auto_setup.py hace git pull automatico y lee este archivo
- machote/ se borra automaticamente despues de instalar/actualizar
- /compact al terminar plan y al empezar modulo nuevo
- git log/pull/diff permitidos — solo commit/push/add prohibidos

### Instrucciones para la IA:

**1. Verificar seccion GIT en AGENTS.md**
Lee AGENTS.md. Busca la seccion GIT.
Si dice solo `git status → unico permitido` → reemplaza esa seccion con esto:

```
## GIT — REGLAS

✅ PERMITIDO:
git status / git log / git pull / git diff

❌ PROHIBIDO SIEMPRE:
git commit / git push / git add / git stash / git reset / git rebase

El humano hace commit, add y push. La IA puede leer historial y actualizar sistema-ia/.
```

Si ya tiene esa estructura → OK, no tocar.

**2. Verificar INICIO.md**
Si no existe INICIO.md en la raiz → copia el contenido de abajo como INICIO.md:

```
# INICIO — Lee esto primero

Lee ESTADO.md → detecta tu rol → actua.

## Si eres ARQUITECTO
- Debate en archivo discusiones/N-modulo/v1.md — NO en el chat
- Chat solo: idea / 1 (feedback) / 0 (aprobar)
- Al terminar: python sistema-ia/acciones/finalizar_discusion.py [modulo] [version]
- NO escribas codigo. NO toques archivos fuera de discusiones/planes/ESTADO.md.

## Si eres DEV
- Lee el plan COMPLETO antes de empezar
- Ejecuta TODAS las tareas seguidas, sin pedir permiso
- Marca [x] por tarea, actualiza ESTADO.md
- Al terminar: python sistema-ia/acciones/finalizar_plan.py [modulo] [version]

## Avisos (obligatorio)
python sistema-ia/acciones/avisar.py "mensaje" suave|normal|urgente

## Prohibido siempre
- git commit / push / add
- Secrets en codigo
- Continuar sin avisar al terminar
```

Si ya existe INICIO.md → OK, no tocar.

**3. Avisar**
```bash
python sistema-ia/acciones/avisar.py "Proyecto actualizado a v2.5" normal
```

---

## PLANTILLA para versiones futuras

```markdown
## vX.Y

### Que cambio
- [descripcion corta]

### Instrucciones para la IA:

**1. [Paso]**
- Lee [archivo]
- Si [condicion] → [accion con contenido INLINE, no referenciar machote/]
- Si ya esta → OK

**2. Avisar**
python sistema-ia/acciones/avisar.py "Proyecto actualizado a vX.Y" normal
```
