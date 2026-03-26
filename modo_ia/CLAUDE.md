# CLAUDE.md — modo ia v1.0
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
Leer `claude/estado.log` y `MAPA.md`. Presentar:
```
Proyecto : [PROJ]  |  Stack : [STACK]
Etapa    : [ETAPA] |  Motor : [motor detectado]
Último   : [LAST_TASK]
Próximo  : [NEXT]
Listo. ¿Continuamos?
```

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

## CICLO DE TRABAJO

```
IDEA → disc_[tema].md en creaciones/ o soluciones/
 (la discusión funciona como nota viva de memoria)
  → "📝 disc_[tema].md — marca 1 cuando hayas leído"
  → [ 1=releer | R:/=incorporar | 0=aprobar ]
  → Estado: Aprobado → plan_XXX.md → ejecución bottom-up
  → Cierre: finalizar_etapa + backup + avisar
```

**Discusiones:**
- Idea nueva / feature → `claude/discusiones/creaciones/`
- Bug / mejora / gap → `claude/discusiones/soluciones/`
- Base sugerida: `claude/discusiones/TEMPLATE_DISCUSION.md`

**Planes — orden obligatorio:**
1. Datos (modelos, DB, migraciones)
2. Servicios (lógica de negocio, serializers)
3. API (vistas, rutas, auth)
4. UI (componentes, páginas)
5. Integración y tests

**Memoria de continuidad:**
- Archivo vivo: `claude/memoria/MEMORIA.md`
- Se actualiza en cierre de etapa y sirve para retomar exactamente dónde quedó

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
[DEBT: descripción concreta]
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
