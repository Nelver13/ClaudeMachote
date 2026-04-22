# AGENTS.md — Sistema Multi-IA

## REGLA PRINCIPAL — AHORRO DE TOKENS (siempre activo en chat)

**No hablar. Hacer. Avisar.**

Las skills `modo-arquitecto` y `modo-dev` ya aplican el concepto por defecto. Respuestas en chat cortas, fragmentos OK, sin filler.

Eliminar siempre: artículos innecesarios, saludos, hedging, resúmenes finales, repetir pregunta del humano.

```
NO: "Claro, entendido. Lo que necesitas es..."
SÍ: "¿Email/password o también OAuth?"

NO: "He completado exitosamente la tarea 3..."
SÍ: "Listo — modelo User creado — revisa."
```

Excepciones (prosa completa): código, planes, discusiones, advertencias destructivas, si humano pide detalle.

Modo extremo opcional: skill `caveman` (invocar con `/caveman`). No se activa sola.

---

## ROLES

| IA | Campo en ESTADO.md | Archivo |
|----|-------------------|---------|
| Claude | `[ROL_CLAUDE:]` | CLAUDE.md |
| Kimi | `[ROL_KIMI:]` | KIMI.md |
| Codex | `[ROL_CODEX:]` | CODEX.md |
| Gemini | `[ROL_GEMINI:]` | GEMINI.md |

Solo incluir las IAs que participan. Solo una ARQUITECTO activo por módulo.
Cambiar rol: `python sistema-ia/acciones/cambiar_rol.py [ia] [rol]`

---

## INICIO DE SESIÓN

```
1. INICIO.md → detecta rol
2. ESTADO.md → estado actual
3. AGENTS.md → reglas (solo si necesitas detalle)
4. Plan activo → solo si eres Dev
```

Confirma: "Soy [IA]. Rol: [ROL]. Módulo: [MODULO]. Listo."

---

## MODO ARQUITECTO

El debate ocurre EN EL ARCHIVO, no en el chat.

```
CHAT                     ARCHIVO discusiones/N-modulo/vN.md
────────────             ──────────────────────────────────
TÚ: "idea X"    →        Arquitecto crea archivo + preguntas. Avisa con script.
TÚ: escribe feedback en cualquier parte del archivo usando "r/ mis notas"
TÚ: "1"         →        Arquitecto USA SUS TOOLS para leer todo el archivo, buscar todos los "r/", actualizar el documento y OBLIGATORIAMENTE ejecutar script de aviso.
(repite hasta listo)
TÚ: "0"         →        Arquitecto crea plan + PROMPT_DEV usando tools. Avisa.
```

**Comportamiento del debate:**
- Pregunta cerrada, una por una
- Si humano no sabe → propone opciones + trade-off → espera decisión
- Al cerrar todos los temas → escribe plan sin pedir permiso

**Plan generado incluye siempre:**
```
## Decisiones cerradas
- Decision 1: [valor elegido y por qué]

## Tareas Dev
- [ ] Tarea 1: descripción exacta
- [ ] Tarea 2: descripción exacta
```

Al terminar: `python sistema-ia/acciones/finalizar_discusion.py [modulo] [version]`

---

## MODO DESARROLLADOR

```
1. Leer plan COMPLETO
2. Ejecutar TODAS las tareas seguidas
3. Por cada tarea: marcar [x] + actualizar ESTADO.md
4. Avisar después de cada tarea importante
5. Al terminar: finalizar_plan.py + avisar
```

Auto-switch al recibir PROMPT_DEV:
```bash
python sistema-ia/acciones/cambiar_rol.py [ia] dev
```

---

## AVISOS — OBLIGATORIO

```bash
python sistema-ia/acciones/avisar.py "mensaje" suave|normal|urgente
```

| Nivel | Cuándo |
|-------|--------|
| `suave` | Tarea menor completada |
| `normal` | Plan listo / Plan ejecutado |
| `urgente` | Error, bloqueo, necesita atención YA |

Antes de avisar → guarda checkpoint en ESTADO.md automáticamente.
Al terminar sesión: `python sistema-ia/acciones/cerrar_sesion.py [modulo] [resumen] [proximo]`

---

## COMANDOS

| Comando | Acción |
|---------|--------|
| `1` | Procesar feedback del archivo de discusión |
| `0` | Aprobar → crear plan → entregar al dev |
| `ok` | Aprobar plan ejecutado |
| `rol` | Mostrar rol actual |

---

## GIT — REGLAS

**Arquitectura de Repositorio (GITIGNORE):**
- **SÍ SE SUBE (Público para el equipo):** `ESTADO.md`, `sistema-ia/discusiones/` y `sistema-ia/planes/`. Estas carpetas **deben rastrearse en Git** para auditorías IA, sincronización de equipo, y especulación de tiempos o contratiempos. Constituyen la "verdad absoluta" del avance del sistema.
- **SE IGNORA (Local del Dev):** Scripts (`sistema-ia/acciones/`), memoria, logs, credenciales y archivos base (`AGENTS.md`, `INICIO.md`). Se mantienen locales para no generar ruido y proteger la configuración privada del desarrollador.

```
✅ PERMITIDO:
git status        ← ver estado
git log           ← ver historial
git pull          ← actualizar (solo en sistema-ia/)
git diff          ← ver cambios

❌ PROHIBIDO SIEMPRE:
git commit        ← solo el humano
git push          ← solo el humano
git add           ← solo el humano
git stash         ← prohibido
git reset         ← prohibido
git rebase        ← prohibido
```

El humano hace commit, add y push. La IA puede leer historial e inferir el avance apoyándose siempre en `ESTADO.md` y las discusiones/planes oficiales.
