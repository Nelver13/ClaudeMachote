# FLUJO — Discusión → Aprobación → Ejecución

> Igual para todos los motores (Copilot, Claude, Cursor, Google Antigravity).
> Simple. Lineal. Agnóstico.

---

## 1️⃣ DISCUSIÓN

### Vos decís
```
Necesito una API REST en Django que...
```

**El motor (Claude/Copilot/Cursor/etc):**
1. Crea `claude/discusiones/disc_[tema].md`
2. Escribe análisis completo + propuesta + riesgos
3. En el chat pone una línea:
   ```
   📝 disc_[tema].md — marca 1 cuando hayas leído
   ```

### Vos leés y respondés

| Comando | Motor hace |
|---------|-----------|
| `1` | Re-lee el `.md`, actualiza si falta algo, confirma |
| `R:/ [nota]` | Incorpora tu nota, actualiza `.md`, confirma |
| `revisa` | Actualiza basado en tu feedback |
| `0` | ✅ **APROBADO** → Genera checklist |

---

## 2️⃣ APROBACIÓN

Cuando decís `0`:
- Motor marca `Estado: Aprobado` en `disc_[tema].md`
- Motor genera `claude/planes/plan_XXX.md` con checklist
- Motor chequea `credenciales.md` — si falta algo → avisa
- **Avisar**: `python claude/acciones/avisar.py "plan_XXX.md listo"`
- ✅ Listo → fase ejecutar

---

## 3️⃣ EJECUCIÓN

Motor corre todo de corrido:

```markdown
# Plan #123 — API REST Django

## Tareas
- [x] Crear serializer
- [x] Crear viewset
- [ ] Tests unitarios    ← EN PROGRESO
  - [ ] test_create
  - [ ] test_list
- [ ] Documentación

## Notas
- [2026-03-23 11:30] Motor: Serializer listo, validaciones OK
- [2026-03-23 11:35] Motor: ViewSet POST/GET/PUT/DELETE funcionan
- [2026-03-23 11:40] Motor: Tests ejecutándose...
```

Motor:
1. Completa cada tarea
2. Marca `[x]` al terminar
3. Agrega notas sobre lo que pasó (cambios, decisiones, errores)
4. Si hay error → pausa y avisa (urgente)

---

## 4️⃣ CIERRE

Al terminar todas las tareas:

```bash
# 1. Git status
git status

# 2. Avisar
python claude/acciones/avisar.py "plan_XXX terminado" normal

# 3. Actualizar estado
# (Claude actualiza claude/RESUMEN.md automáticamente)
```

---

## 🔄 Loop Discusión

```
┌─ Vos: "Necesito..."             (IDEA)
│
├─ Motor: "disc_[tema].md listo"  (ANÁLISIS)
│
├─ Vos: lee + responde
│  ├─ Si "1" → Motor re-lee
│  ├─ Si "R:/ [cosa]" → Motor incorpora
│  └─ Si "revisa" → Motor actualiza
│
└─ Vos: "0"                        (APROBADO)
   │
   ├─ Motor: "plan_XXX listo"
   │
   └─ Motor: ejecuta todo
```

---

## 📋 Estructura disc_[tema].md

```markdown
# Discusión: [tema]
**Fecha**: YYYY-MM-DD
**Motor**: [copilot/claude/cursor/antigravity]
**Estado**: Pendiente | En revisión | **Aprobado**

## 📌 Resumen
Lo que el arquitecto pidió.

## 💡 Propuesta
Cómo el motor lo resuelve.

## ⚠️ Riesgos
Qué puede fallar.

## ❓ Preguntas
Qué el motor necesita confirmar.

## Feedback (del arquitecto)
- R:/ nota 1
- R:/ nota 2
```

---

## 📋 Estructura plan_XXX.md

```markdown
# Plan #XXX — [Nombre]
**Fecha**: YYYY-MM-DD
**Origen**: disc_[tema].md
**Motor**: [activo]
**Estado**: En ejecución

## Tareas
- [ ] Tarea 1
  - [ ] Sub 1.1
  - [ ] Sub 1.2
- [ ] Tarea 2

## Notas de ejecución
- [HH:MM] Motor: Acción realizada, resultado
```

---

## 🔑 Reglas Clave

1. **Un `0` = arrancar ejecución** — No preguntes, arranca
2. **Discusión primero** — Nunca código sin `disc_[tema].md`
3. **Feedback antes de aprobación** — Editá la propuesta antes de `0`
4. **Credenciales centralizadas** — El motor las busca en `credenciales.md`
5. **Avisos siempre** — Motor notifica en cada etapa

---

## 🚫 Nunca

- Ejecutar sin `disc_[tema].md` aprobado
- Saltar fases (discusión → aprobación → ejecución)
- Escribir secretos en el código
- `git commit` (el arquitecto administra git)
