# CLAUDE.md — modo ia v2.0 (fullstack optimizado)
> Protocolo de trabajo. La IA lee esto al iniciar cada sesión.
> Skills, motores y memoria del proyecto en sus carpetas correspondientes.

@../ai_scheme/SCHEME.md

---

## INICIO DE SESIÓN

Leer `claude/estado.log` y determinar el caso:

**Caso A — `claude/` sin datos → proyecto nuevo**
1. Ejecutar `python claude/acciones/init_db.py`
2. Detectar stack (ver tabla abajo) → cargar skill correspondiente
3. Proponer roadmap `Etapa → Sub-etapa → Paso`
4. Esperar aprobación

**Caso B — `claude/` con datos → proyecto con historial**
Leer `claude/estado.log`, `MAPA.md` y `VISION.md`. Presentar:
```
Proyecto : [PROJ]  |  Stack : [STACK]  |  Visión: [multi-solución?]
Etapa    : [ETAPA] |  Motor : [motor detectado]
Último   : [LAST_TASK]
Próximo  : [NEXT]
Listo. ¿Continuamos?
```

**Importante:** Si NO existe `VISION.md`, forzar definición de visión antes de cualquier desarrollo.

---

## DETECCIÓN DE STACK

| Indicador | Stack | Skill |
|---|---|---|
| `manage.py` + `vite.config.*` | Django + React | django-drf + react-vite |
| `manage.py` solo | Django + DRF | django-drf |
| `pubspec.yaml` | Flutter | mobile |
| `app.json` + expo | React Native | mobile |
| `package.json` + electron | Electron | mobile |
| `docker-compose.yml` + n8n | n8n incluido | n8n-flows |
| `package.json` + vite | React standalone | react-vite |

`git-security` se activa siempre, en cualquier stack.

---

## CICLO DE TRABAJO v2.0 — Visión First

### 🚀 FASE 1: Definición de Visión (OBLIGATORIA)

```
Arquitecto: "Definir visión del proyecto"
      ↓
Claude: python crear_discusion.py definir-vision-proyecto definicion_vision
      ↓
✓ Detecta que NO existe VISION.md → fuerza definición
✓ Crea disc_definir-vision-proyecto.md con template especial
✓ Arquitecto define soluciones (S1-S4) y módulos
      ↓
Arquitecto: 0 (aprobar)
      ↓
Claude: python procesar_aprobacion.py disc_definir-vision-proyecto.md
      ↓
✓ Detecta tipo "definicion_vision"
✓ Ejecuta generar_vision.py → crea VISION.md automáticamente
✓ Proyecto queda definido con soluciones y módulos
```

### 🔧 FASE 2: Desarrollo por Módulos

```
Arquitecto: "Crear módulo [nombre]"
      ↓
Claude: python crear_discusion.py [modulo] desarrollo
      ↓
✓ Lee VISION.md → detecta solución apropiada (S1/S2/S3/S4)
✓ Crea disc_[modulo].md con template adaptado para esa solución
✓ Arquitecto lee y modifica plan específico para el stack
      ↓
Arquitecto: 0 (aprobar)
      ↓
Claude: python procesar_aprobacion.py disc_[modulo].md
      ↓
✓ Detecta tipo "desarrollo_modulo"
✓ Ejecuta crear_plan.py → extrae plan → plan_XXX.md checklist
✓ Checklist se actualiza automáticamente durante ejecución
      ↓
Cada tarea completada → actualizar_checklist.py
      ↓
Cierre: finalizar_etapa + backup + avisar final
```

**Avisos automáticos en cada paso:**
- Al crear discusión: `avisar.py "disc_[tema].md listo — marca 1" suave`
- Al procesar aprobación visión: `avisar.py "VISION.md generada — proyecto definido" normal`
- Al generar plan: `avisar.py "plan_XXX.md listo — empezando [Solución]" normal`
- Al terminar tarea: `avisar.py "Tarea X completada" suave`
- Al cerrar etapa: `avisar.py "Módulo terminado — listo para siguiente" normal`

**Planes automáticos para ahorro de tokens:**
- Al crear discusión, Claude detecta automáticamente el módulo apropiado (django-drf, react-vite, etc.)
- Genera plan preliminar optimizado para el stack y enfoque backend-first
- Incluye estimación de complejidad, tiempo y archivos afectados
- Arquitecto puede modificar el plan antes de aprobar con `0`

**Discusiones:**
- Idea nueva / feature → `claude/discusiones/creaciones/`
- Bug / mejora / gap → `claude/discusiones/soluciones/`
- Base sugerida: `claude/discusiones/TEMPLATE_DISCUSION.md`

**Planes — orden para fullstack:**
1. **Datos** (modelos Django, migraciones PostgreSQL)
2. **API** (serializers DRF, vistas, rutas, JWT auth)
3. **Frontend** (componentes React, páginas Vite)
4. **Integración** (conexión API-Frontend, tests)
5. **Despliegue** (Docker, configuración prod)

**Memoria de continuidad:**
- Archivo vivo: `claude/memoria/MEMORIA.md`
- Se actualiza en cierre de etapa y resume:
  - Estado actual
  - Última discusión
  - Último plan
  - Impacto en VISION.md

---

## COMANDOS

| Comando | Acción |
|---|---|
| `1` | Re-leer el `.md`. Si hay cambios: actualizar + `avisar.py "actualizado" suave` |
| `R:/ [texto]` | Parar, incorporar todo en el `.md`, confirmar en una línea |
| `0` | Aprobado → generar plan → ejecutar |
| `revisa` | Incorporar notas del arquitecto en el `.md` |

---

## CIERRE DE ETAPA

```bash
python claude/acciones/finalizar_etapa.py "[nombre etapa]"
python claude/acciones/backup_n8n.py [N]     # si hay n8n
python claude/acciones/backup_sql.py [N]     # si hay DB
python claude/acciones/avisar.py "Etapa XX terminada" normal
```

Luego actualizar `claude/estado.log` y verificar `claude/memoria/MEMORIA.md`.

---

## VISION.md — Multi-solución desde el día 1

**Obligatorio en proyectos fullstack.** Se construye en conversación inicial:

```markdown
# VISION.md — [Proyecto]
**Generado:** YYYY-MM-DD

## Qué hace el sistema
[1-3 líneas — qué problema resuelve]

## Soluciones previstas
| ID | Solución | Plataforma | Stack | Estado |
|---|---|---|---|---|
| S1 | API Backend | Django + DRF | Python | En desarrollo |
| S2 | Web Frontend | React + Vite | JS/TS | Pendiente |
| S3 | Mobile App | React Native | JS | Pendiente |

## API compartida
- Base: `/api/v1/`
- Auth: JWT
- DB: PostgreSQL

## Reglas derivadas
- Endpoints pensados para múltiples clientes
- Serializers reutilizables
- Auth válido en todas las plataformas
```

**Cuándo actualizar:** Nueva solución, cambio de rumbo, feedback post-etapa.

---

```
[PROJ: nombre]
[STACK: Django+React+PostgreSQL]
[ETAPA: XX-Nombre]
[SUB-ETAPA: X.X-Nombre]
[PASO: X.X.X-descripción]
[LAST_FILE: apps/usuarios/models.py]
[LAST_TASK: Crear modelo User con JWT]
[NEXT: Serializar modelo para API]
[DB: 1]
[DEBT: Ninguna]
[VISION: S1-API en desarrollo, S2-Web pendiente]
```

---

## SEGURIDAD

- Nunca secrets en código → siempre `.env` + `.env.example`
- Secret detectado → parar y señalar antes de continuar
- Credenciales → `claude/acciones/credenciales.md`
- `claude/` nunca a git

---

## NUNCA

- `git commit` o `git push`
- Código sin checklist desde discusión aprobada
- Checklist sin `0` del arquitecto
- Ignorar `R:/`, `1` o `0`
- Terminar etapa sin `finalizar_etapa.py` + backup + aviso
- Usar credencial sin verificar en `credenciales.md`
- Subir `claude/` a git
