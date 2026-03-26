# CLAUDE.md — v6.0 (mejorado)
> Leé este archivo al iniciar. Skills y permisos en `.claude/`.
> Memoria del proyecto en `claude/` — nunca sube a git.
> Stack del arquitecto: @STACK.md

---

## 📍 INICIO DE SESIÓN — SIEMPRE

Leer `claude/estado.log` y determinar el caso:

### Caso A — `claude/` no existe → proyecto virgen (caso legacy)
1. Detectar stack según @STACK.md y estructura de archivos
2. Cargar skill correspondiente (ver tabla DETECCIÓN DE STACK)
3. Proponer roadmap `Etapa → Sub-etapa → Paso`
4. Esperar `R:/` o aprobación
5. Crear estructura base: `mkdir -p claude/planes claude/discusiones claude/backups/n8n claude/backups/sql claude/imagenes/errores claude/imagenes/mejoras`
6. Mover `acciones/` a `claude/acciones/` si existe en la raíz

### Caso B — `claude/` existe pero `estado.log` tiene PROJ y STACK vacíos → template copiado, proyecto nuevo
1. Detectar stack según @STACK.md y estructura de archivos
2. Cargar skill correspondiente (ver tabla DETECCIÓN DE STACK)
3. Proponer roadmap `Etapa → Sub-etapa → Paso`
4. Esperar `R:/` o aprobación
_(La estructura ya está creada en `claude/`. No crear carpetas ni mover archivos.)_

### Caso C — `claude/` existe y `estado.log` tiene datos → proyecto con historial
Leer `claude/estado.log` y `claude/RESUMEN.md`. Presentar:
```
📍 CONTEXTO RECUPERADO
──────────────────────────────────────────────
Proyecto     : [nombre]
Stack        : [tecnologías]
Etapa        : [etapa actual]
Sub-etapa    : [sub-etapa]
Paso actual  : [paso]
Última acción: [qué se hizo]
Pendiente    : [próximo paso]
──────────────────────────────────────────────
Listo. ¿Continuamos o hay algo nuevo?
```

---

## 🔍 DETECCIÓN DE STACK

| Indicador | Stack | Skill a cargar |
|---|---|---|
| `manage.py` + `vite.config.*` | Django + React | @django-drf + @react-vite |
| `manage.py` solo | Django + DRF | @django-drf |
| `pubspec.yaml` | Flutter | @flutter |
| `app.json` + expo | React Native + Expo | @react-native |
| `.sln` o `.csproj` | WinForms / C# | @winforms |
| `docker-compose` + n8n | n8n incluido | @n8n-flows |
| `package.json` + vite | React standalone | @react-vite |

Si no puede determinar → pregunta antes de asumir.

---

## 🧭 CICLO COMPLETO

```
IDEA → Claude analiza → disc_[tema].md
  ↓
"📝 disc_[tema].md — marca 1 cuando hayas leído"
  ↓
[ 1=releer | R:/=incorporar | 0=aprobar ]
  ↓
Estado: Aprobado → plan_XXX.md → ejecución
  ↓
Cierre: backup + estado.log + aviso
```

---

## 💬 Modo Discusión (por defecto)
No genera código. Crea/actualiza `.md` en `claude/discusiones/`.

Al iniciar discusión nueva:
1. Si hay imagen → revisar `claude/imagenes/mejoras/`
2. Crear `claude/discusiones/disc_[tema].md`
3. Chat: `📝 disc_[tema].md — marca 1 cuando hayas leído`
4. `python claude/acciones/avisar.py "disc_[tema].md listo" suave`
5. Registrar en `claude/discusiones/INDEX.md`

| Comando | Acción |
|---|---|
| `1` | Re-leer el `.md`. Si hubo cambios: actualizar el archivo + `avisar.py "disc_[tema].md actualizado" suave`. Si no hubo cambios: decir "sin cambios" en el chat, sin avisar. |
| `revisa` | Incorporar notas del arquitecto en el `.md` + `avisar.py "disc_[tema].md revisado" suave` |
| `R:/ [texto]` | Parar, incorporar todo en el `.md`, confirmar con una línea en el chat + `avisar.py "disc_[tema].md actualizado" suave` |
| `0` | **Aprobado** → generar checklist y arrancar |

> `R:/` tiene prioridad absoluta.

---

## ⚡ Modo Ejecución — activado por `0`

1. Marcar `disc_[tema].md` → `Estado: Aprobado`
2. Actualizar `claude/discusiones/INDEX.md`
3. Generar `claude/planes/plan_XXX.md` como checklist
4. `python claude/acciones/avisar.py "plan_XXX.md listo — arrancando" normal`
5. Ejecutar marcando `[x]` en cada tarea
6. Al terminar → cierre de etapa obligatorio

Formato del plan:
```markdown
# Plan #XXX — [Nombre]
Fecha: YYYY-MM-DD | Estado: En ejecución
Origen: disc_[tema].md | Depende de: plan_YYY.md (si aplica)

## Tareas
- [ ] Tarea 1
  - [ ] Sub-tarea 1.1
- [ ] Tarea 2

## Notas de ejecución
_(cambios, problemas, decisiones durante la ejecución)_
```

---

## 💾 CIERRE DE ETAPA

```bash
git status                                          # verificar cambios
python claude/acciones/backup_n8n.py [N]            # backup n8n (si aplica)
python claude/acciones/backup_sql.py [N]            # backup PostgreSQL (si aplica)
python claude/acciones/avisar.py "Etapa XX terminada" normal
```

Actualizar:
- `claude/estado.log` — estado granular
- `claude/RESUMEN.md` — máximo 5 líneas
- `claude/discusiones/INDEX.md` — marcar disc como completada

Formato `estado.log`:
```
[PROJ: nombre]
[STACK: tecnologías]
[ETAPA: XX-Nombre]
[SUB-ETAPA: X.X-Nombre]
[PASO: X.X.X-descripción]
[LAST_FILE: path/archivo]
[LAST_TASK: descripción breve]
[NEXT: próximo paso concreto]
[DB: 0/1]
[DEBT: descripción concreta de deuda — archivo y qué falta]
[PLAN_DEPS: plan_XXX depende de plan_YYY]
```

---

## 🔔 AVISOS

| Tipo | Cuándo |
|---|---|
| `suave` | Discusión actualizada |
| `normal` | Etapa terminada, plan listo |
| `urgente` | Error inesperado, secreto detectado |

Comando: `python claude/acciones/avisar.py "mensaje" [tipo]`

---

## 🔑 CREDENCIALES

En `claude/acciones/credenciales.md`. Tener la credencial = tener permiso de usarla.
- Antes de servicio externo → leer `credenciales.md`
- Si el arquitecto da credencial en chat → guardar antes de usar
- Si falla → marcar `expirada` y pedir nueva

---

## 🔐 SEGURIDAD

- Nunca secrets en código → siempre `.env` + `.env.example`
- Si detecta secreto hardcodeado → parar y señalar antes de continuar
- Permisos de terminal → ver `.claude/settings.json`

---

## 🚀 PROYECTO VIRGEN

```bash
mkdir -p claude/planes claude/discusiones claude/backups/n8n claude/backups/sql claude/imagenes/errores claude/imagenes/mejoras
mv acciones/ claude/acciones/
```

Crear en `claude/`: `RESUMEN.md`, `estado.log`, `discusiones/INDEX.md`
Crear en raíz: `.gitignore` según stack

---

## 🖼️ IMÁGENES DE REFERENCIA

| Mención | Carpeta |
|---|---|
| "error", "bug", "no funciona" | `claude/imagenes/errores/` |
| "mejora", "quiero esto", "inspirate" | `claude/imagenes/mejoras/` |

Claude lista la carpeta y toma la más reciente. Nunca borra imágenes.

---

## 🚫 CLAUDE NUNCA

- Escribe código sin checklist desde discusión aprobada
- Genera checklist sin `0` del arquitecto
- Ejecuta `git commit` o `git push`
- Escribe secretos en código
- Repite en chat lo que escribió en `.md`
- Ignora `R:/`, `revisa`, `1` o `0`
- Termina etapa sin backup, estado.log y aviso
- Crea `claude/` si ya existe
- Borra imágenes de referencia
- Arranca etapa sin verificar git status
- Usa credencial sin verificar en `credenciales.md`
