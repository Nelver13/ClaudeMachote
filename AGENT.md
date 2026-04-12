# AGENT.md
> Claude / Kimi / Codex / Gemini — leer esto.
> Carpeta base: ./

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
- Al final: plan cerrado en `./planes/[modulo]/v[N].md`

**La IA guarda la sesión en** `./discs/[modulo]/v[N].md`:
```
ia/ [propuesta o razonamiento]
r/  [tu intervención — esto manda]
ia/ [ajuste]
r/  ok
```

**Al cerrar la discusión:**

Cuando tú dices `ok`, la IA ejecuta:
```bash
python ./acciones/finalizar_discusion.py [modulo] [version]
```

Solo avisa: **"DISC: [modulo]/v[N] lista — revisa y dime ok"**

**Tú:**
1. Revisas el plan en `planes/` o `discs/`
2. Si hay cambios → reabres discusión con feedback
3. Si está OK → dices "modo:dev" o pegas el prompt de inicio

---

## MODO DEV (tarea por tarea)

**Flujo:**
1. Leer `estado.log` → `TAREA_ACTUAL`
2. Ejecutar SOLO esa tarea
3. **Si hay problema/bloqueo:**
   ```bash
   python ./acciones/avisar.py "PROBLEMA: [qué pasa]" urgente
   ```
   → Tú revisas, das instrucciones, continúa

4. **Si tarea completada OK:**
   ```bash
   python ./acciones/completar_tarea.py [N] [total]
   ```
   → Si es última tarea: avisa **"🎉 PLAN COMPLETO"**
   → Si hay más: avisa **"Tarea N/M lista — siguiente: N+1"**

**Nunca:** hacer dos tareas seguidas sin avisar.

---

## MAPA DEL PROYECTO

Antes de cada sesión:
1. Leer `MAPA.md` — índice rápido del proyecto (embedding-optimized)
2. Leer `estado.log` — estado actual

**Si cambias la estructura (nuevos archivos, carpetas, renombres):**
```bash
python ./acciones/actualizar_mapa.py
```

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

## SIEMPRE
- Actualizar `MAPA.md` tras cambios estructurales (nuevos archivos/carpetas)
- Verificar `estado.log` al inicio de cada sesión

## NUNCA
- Parla antes o después del trabajo
- Más de una tarea por sesión en modo:dev
- git commit / git push
- Terminar sin avisar.py
