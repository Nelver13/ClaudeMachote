# NOVEDADES — Instrucciones de actualización para la IA
> auto_setup.py inyecta este archivo cuando detecta version nueva.
> La IA ejecuta las instrucciones de la version instalada.
> REGLA: ejecutar TODO en orden. No saltarse pasos. No tocar lo que dice "NO TOCAR".

---

## REGLAS GENERALES (aplican a todas las versiones)

### NUNCA tocar:
- ESTADO.md — tiene el estado actual del proyecto
- planes/ discusiones/ memoria/ handoff/ — trabajo activo
- El nombre del proyecto, stack, roles configurados
- Codigo de produccion del proyecto

### SIEMPRE antes de editar un .md del proyecto:
1. Leer el archivo completo primero
2. Aplicar SOLO lo que dice la instruccion — nada mas
3. Si el contenido ya existe → saltar ese paso (no duplicar)
4. Si tienes duda → avisar urgente y parar

### Al terminar todas las instrucciones:
```bash
python sistema-ia/acciones/avisar.py "Proyecto actualizado a v[X.Y]" normal
```

---

## v2.5

### Que cambio en esta version
- auto_setup.py hace git pull automatico al detectar version nueva
- NOVEDADES.md da instrucciones automaticas a la IA
- /compact se ejecuta al terminar plan y al empezar modulo nuevo

### Instrucciones para la IA:

**1. Verificar seccion de ahorro en AGENTS.md**
- Lee AGENTS.md del proyecto (raiz)
- Busca la primera seccion despues del titulo
- Si dice `MODO CAVEMAN (siempre activo)` → reemplaza esa seccion entera con el contenido de `sistema-ia/machote/AGENTS.md` seccion `AHORRO DE TOKENS`
- Si ya dice `AHORRO DE TOKENS` → OK, no hacer nada

**2. Verificar INICIO.md**
- Si no existe INICIO.md en la raiz del proyecto → copia `sistema-ia/machote/INICIO.md` → `INICIO.md`
- Si ya existe → compara con `sistema-ia/machote/INICIO.md`
- Si el existente tiene menos de 20 lineas y el machote tiene mas → reemplaza
- Si el existente tiene datos del proyecto → no tocar

**3. Verificar hooks en .claude/settings.json**
- Lee `.claude/settings.json` del proyecto
- Debe tener `SessionStart` con comando `python sistema-ia/acciones/auto_setup.py`
- Debe tener `PreToolUse` con matcher `Edit|Write` y comando `python sistema-ia/acciones/check_role.py`
- Si faltan → agrega. Si ya estan → OK

**4. Avisar**
```bash
python sistema-ia/acciones/avisar.py "Proyecto actualizado a v2.5" normal
```

---

## PLANTILLA para versiones futuras

Cuando hagas una nueva version copia esto y llena:

```markdown
## vX.Y

### Que cambio en esta version
- [descripcion corta]

### Instrucciones para la IA:

**1. [Nombre del paso]**
- Lee [archivo]
- Si [condicion] → [accion exacta]
- Si ya esta → OK, no hacer nada

**2. Avisar**
python sistema-ia/acciones/avisar.py "Proyecto actualizado a vX.Y" normal
```
