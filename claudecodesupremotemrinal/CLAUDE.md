# CLAUDE.md — claudecodesupremotemrinal
> Leé este archivo al iniciar. Todo lo que necesitás está acá.
> Memoria del proyecto en `claude/` — nunca sube a git.

---

## INICIO DE SESIÓN

Leer `claude/estado.log`:

**Proyecto nuevo** (estado.log vacío):
1. Detectar stack → cargar skill correspondiente
2. Abrir `disc_vision-[proyecto].md` → hacer kit de preguntas de visión → construir `VISION.md`
3. Arquitecto aprueba visión con `0` → generar roadmap `Etapa → Sub-etapa → Paso`
4. Esperar aprobación del roadmap antes de arrancar

**Proyecto con historial:**
```
Proyecto : [PROJ]
Etapa    : [ETAPA] — [PASO]
Último   : [LAST_TASK]
Próximo  : [NEXT]
¿Continuamos?
```
Leer también `VISION.md` si existe — tenerlo presente durante toda la sesión.

---

## DETECCIÓN DE STACK

| Indicador | Stack | Skill |
|---|---|---|
| `manage.py` + `vite.config.*` | Django + React | django-drf + react-vite |
| `manage.py` solo | Django + DRF | django-drf |
| `pubspec.yaml` | Flutter | mobile |
| `app.json` + expo | React Native | mobile |
| `package.json` + electron | Electron | mobile |
| `docker-compose` + n8n | n8n | n8n-flows |
| `package.json` + vite | React standalone | react-vite |

`git-security` se activa siempre.

---

## CICLO DE TRABAJO

```
Idea nueva / problema
      ↓
disc_[tema].md  →  creaciones/ (idea nueva)
                   soluciones/ (bug, mejora, gap)
      ↓
"📝 disc_[tema].md — marca 1 cuando hayas leído"
python claude/acciones/avisar.py "disc_[tema].md listo — marca 1" suave
      ↓
[ 1 | R:/ | 0 ]
      ↓ 0
plan_XXX.md generado
python claude/acciones/avisar.py "plan_XXX.md listo — arrancando" normal
      ↓
Ejecutar bottom-up marcando [x]
      ↓
Cierre de etapa
python claude/acciones/avisar.py "Etapa XX terminada — revisá para continuar" normal
```

---

## COMANDOS

| Comando | Acción |
|---|---|
| `1` | Releer disc activa → actualizar si hay cambios → `avisar.py "disc actualizada" suave` |
| `R:/ [texto]` | Parar todo → incorporar en el .md → confirmar en una línea → avisar suave |
| `0` | Aprobado → generar plan → avisar normal → ejecutar |
| `revisa` | Incorporar notas del arquitecto en el .md |

`R:/` tiene prioridad absoluta sobre cualquier otra cosa.

---

## AVISOS — cuándo y cómo

Claude llama `avisar.py` directamente en estos momentos:

```bash
# Discusión lista
python claude/acciones/avisar.py "disc_[tema].md listo — marca 1" suave

# Discusión releída con cambios
python claude/acciones/avisar.py "disc_[tema].md actualizada — releé" suave

# Plan generado
python claude/acciones/avisar.py "plan_XXX listo — arrancando" normal

# Plan terminado
python claude/acciones/avisar.py "plan_XXX completado — revisá" normal

# Etapa cerrada
python claude/acciones/avisar.py "Etapa [N] terminada — revisá para continuar" normal

# Necesito decisión tuya
python claude/acciones/avisar.py "[pregunta concreta]" normal

# Error o secret detectado
python claude/acciones/avisar.py "[descripción del problema]" urgente
```

**No avisa:** tareas individuales, archivos escritos, pasos internos — eso lo resuelve solo.

---

## PLANES — formato

```markdown
# Plan #XXX — [Nombre]
**Fecha:** YYYY-MM-DD | **Estado:** En ejecución
**Origen:** disc_[tema].md

## Tareas
- [ ] 1. Tarea principal
  - [ ] 1.1 Sub-tarea
  - [ ] 1.2 Sub-tarea
- [ ] 2. Tarea principal

## Notas de ejecución
```

Orden obligatorio: datos → servicios → API → UI → integración

---

## CIERRE DE ETAPA

```bash
# 1. Verificar git
git status

# 2. Backup (si aplica)
python claude/acciones/backup_n8n.py [N]
python claude/acciones/backup_sql.py [N]

# 3. Avisar
python claude/acciones/avisar.py "Etapa [N] terminada — revisá para continuar" normal
```

Actualizar `claude/estado.log` y `claude/MAPA.md`.

---

## ESTADO.LOG — formato

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
[DEBT: deuda técnica concreta]
```

---

## SEGURIDAD

- Nunca secrets en código → `.env` + `.env.example`
- Secret detectado → parar, señalar, no continuar
- Credenciales en `claude/acciones/credenciales.md`
- `claude/` nunca a git

---

## IMÁGENES DE REFERENCIA

| Mención | Carpeta |
|---|---|
| "error", "bug", "no funciona" | `claude/imagenes/errores/` |
| "mejora", "quiero esto", "inspirate" | `claude/imagenes/mejoras/` |

Listar la carpeta, usar la más reciente, nunca borrar.

---

## VISIÓN MULTI-SOLUCIÓN

Si `VISION.md` tiene más de una solución (web + mobile + desktop, etc.):

- La API se diseña para todos los consumidores desde el día 1 — RESTful, sin lógica de presentación
- Auth JWT válido para todos los canales desde el inicio
- Al crear un disc de módulo → cruzar con `VISION.md` y señalar impacto en otras soluciones
- En cada plan → agregar sección `## Impacto en visión final`
- Al cerrar una solución → verificar que el contrato de API no rompió las pendientes
- Para modificar la visión → `disc_vision-update-[tema].md`, nunca editar `VISION.md` a mano
- Al cierre de etapa → actualizar columna Estado en `VISION.md`

### Kit de preguntas — proyecto virgen

Claude hace estas 6 preguntas en `disc_vision-[proyecto].md`:

```
1. ¿Qué hace el sistema en una oración?
2. ¿Cuántas soluciones/plataformas prevés? (web, mobile, desktop, API pública, etc.)
3. ¿Qué hace cada una? (una línea por solución)
4. ¿Qué tecnologías tenés en mente o preferís?
5. ¿Hay restricciones? (deadline, presupuesto, equipo, infra existente)
6. ¿Por dónde querés arrancar?
```

Claude puede proponer si el arquitecto no tiene claro algún punto.
El arquitecto orienta — Claude no asume el norte solo.

---

## NUNCA

- `git commit` o `git push`
- Código sin checklist de discusión aprobada
- Checklist sin `0` del arquitecto
- Ignorar `R:/`, `1` o `0`
- Terminar etapa sin backup + estado.log + aviso
- Usar credencial sin verificar en `credenciales.md`
- Subir `claude/` a git
- Editar `VISION.md` a mano — siempre vía disc_vision-update
