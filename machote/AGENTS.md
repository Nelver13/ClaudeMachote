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

El debate ocurre EN EL ARCHIVO, no en el chat. **CERO resúmenes en chat.**

### Formato de discusión (estructura fija — nunca crece)

```markdown
# Discusión: [MODULO]
**Fecha:** YYYY-MM-DD  **Estado:** En discusión

## Contexto
[UNA VEZ. No crece.]

## Decisiones cerradas
- [Punto]: [decisión] — [razón]

## Tema actual
### [Pregunta que se discute]
[Opciones, trade-offs]
```

**Reglas:**
- "Contexto" se escribe una vez. No se toca.
- "Decisiones cerradas" solo acumula. Cada una en 1 línea.
- "Tema actual" se REEMPLAZA con cada nuevo punto.
- El archivo nunca tiene más de ~80 líneas.

### Flujo

```
CHAT                     ARCHIVO discusiones/N-modulo/vN.md
────────────             ──────────────────────────────────
TÚ: "idea X"    →        Arquitecto crea archivo + primer tema. Avisa.
TÚ: escribe feedback usando "r/ mis notas" en cualquier parte del archivo
TÚ: "1"         →        Arquitecto lee → procesa r/ → consolida:
                          - r/ cierra punto → "Decisiones cerradas" (1 línea)
                          - r/ necesita más → reformula "Tema actual"
                          - Elimina todos los r/ procesados
                          → Avisa. Chat: "Discusión actualizada" NADA MÁS.
(repite hasta completar)
TÚ: "0"         →        Arquitecto crea plan + PROMPT_DEV. Avisa.
```

**Chat del arquitecto — SOLO estas frases:**
- `"Discusión actualizada"` — cuando procesó feedback
- `"Discusión completada — di 0 para generar plan"` — cuando todos los temas están cerrados
- PROMPT_DEV — al generar plan

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

## BUGS — Flujo de reportes

Los bugs se reportan con el reporter (Ctrl+Shift+B) o manualmente en `discusiones/bugs/backlog.md`.

```
Bugs se acumulan en backlog.md
  → "revisa bugs"
  → Arquitecto agrupa → crea discusiones/bugs/fix-vN.md
  → Misma discusión autoconsolidada
  → Plan → Dev arregla → Bugs marcados [x]
  → Screenshots de bugs resueltos se borran
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

## SCRIPTS DE EJECUCIÓN

El proyecto tiene `run.bat` (Windows) y `run.sh` (Mac/Linux) en la raíz.
El arquitecto los configura según el stack durante la discusión 0-vision.
El dev solo ejecuta `run.bat` o `./run.sh` para lanzar la app.

---

## GIT — REGLAS

**Arquitectura de Repositorio (GITIGNORE):**
- **SÍ SE SUBE (Público para el equipo):** `ESTADO.md`, `sistema-ia/discusiones/` y `sistema-ia/planes/`.
- **SE IGNORA (Local del Dev):** Scripts, memoria, logs, credenciales, archivos IA base.

```
✅ PERMITIDO:
git status        ← ver estado
git log           ← ver historial
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
