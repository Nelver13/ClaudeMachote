# AGENT.md
> Claude / Kimi / Codex / Gemini — leer esto.
> Carpeta base: ./claude/

## REGLA PRINCIPAL
No hablar. Hacer. Avisar.

---

## MODOS

| Comando | Qué pasa |
|---------|----------|
| `modo:arquitecto` | Esta conversación ES el plan. Se guarda en discs/ al cerrar. |
| `modo:dev` | Ejecuta el plan de discs/ tarea por tarea. |

---

## MODO ARQUITECTO

Esta sesión es la discusión y el plan al mismo tiempo.

**Durante la sesión:**
- La IA propone, razona, estructura
- Tú intervienes con `r/` — eso redirige todo
- La IA ajusta y sigue
- Al final: plan cerrado en `./claude/planes/[modulo]/v[N].md`

**La IA guarda la sesión en** `./claude/discs/[modulo]/v[N].md`:
```
ia/ [propuesta o razonamiento]
r/  [tu intervención — esto manda]
ia/ [ajuste]
r/  ok
```

**Al cerrar el plan:**
```bash
python ./claude/acciones/avisar.py "Plan [modulo]/v[N] listo — [N] tareas — revisa" normal
```

Tú lees el plan. Dices `ok` o reabres la discusión. El respaldo en discs/ queda para referencia futura.

---

## MODO DEV

1. Leer `./claude/estado.log` → `TAREA_ACTUAL`
2. Ejecutar solo esa tarea
3. Marcar `[x]`, actualizar `estado.log`
4. Avisar:

```bash
# Tarea lista:
python ./claude/acciones/avisar.py "Tarea N/Total: [nombre]" normal

# Necesitas revisar algo antes de continuar:
python ./claude/acciones/avisar.py "REVISAR: [qué — 1 línea]" urgente
```

Tú ves. Dices `ok`. Siguiente tarea.

---

## ESTADO.LOG
```
[IA: nombre]
[TAREA_ACTUAL: N]
[PROGRESO: XX%]
[LAST_TASK: descripción]
[CHECKPOINT: YYYY-MM-DD HH:MM]
```

---

## NUNCA
- Parla antes o después del trabajo
- Más de una tarea por sesión en modo:dev
- git commit / git push
- Terminar sin avisar.py
