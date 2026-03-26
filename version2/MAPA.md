# MAPA — Cómo usar este sistema con Claude Code

---

## ¿Qué es esto?

Un sistema de trabajo para Claude Code que define cómo Claude opera en tus proyectos.
En vez de explicarle todo desde cero cada sesión, Claude lee archivos estructurados
y sabe exactamente qué hacer, cómo hacerlo y qué no puede tocar.

---

## 1. ESTRUCTURA COMPLETA

```
tu-proyecto/
│
├── CLAUDE.md                        ← cerebro del sistema (Claude lee esto primero)
├── STACK.md                         ← tus tecnologías preferidas
├── .gitignore                       ← claude/ nunca sube a git
│
├── .claude/                         ← configuración de Claude Code
│   ├── settings.json                ← permisos + hooks automáticos
│   └── skills/                      ← conocimiento por tecnología
│       ├── django-drf/SKILL.md      ← se activa con proyectos Django
│       ├── react-vite/SKILL.md      ← se activa con proyectos React
│       ├── react-native/SKILL.md    ← se activa con proyectos Expo
│       ├── flutter/SKILL.md         ← se activa con proyectos Flutter
│       ├── n8n-flows/SKILL.md       ← se activa con proyectos n8n
│       └── winforms/SKILL.md        ← se activa con proyectos .sln
│
└── claude/                          ← memoria del proyecto (nunca a git)
    ├── RESUMEN.md                   ← estado en 5 líneas
    ├── estado.log                   ← estado granular actual
    ├── escrituras.log               ← log automático de archivos tocados
    ├── discusiones/
    │   ├── INDEX.md                 ← índice de todas las discusiones
    │   └── disc_[tema].md           ← cada discusión activa o archivada
    ├── planes/
    │   └── plan_001.md              ← checklists de ejecución
    ├── backups/
    │   ├── n8n/                     ← exports de flujos n8n
    │   └── sql/                     ← dumps de PostgreSQL
    ├── imagenes/
    │   ├── errores/                 ← screenshots de bugs
    │   └── mejoras/                 ← referencias de UI/diseño
    └── acciones/
        ├── avisar.py                ← sonido + WhatsApp
        ├── notificar.py             ← hook de notificaciones
        ├── backup_n8n.py            ← backup de flujos n8n
        ├── backup_sql.py            ← dump de PostgreSQL
        ├── check_secrets.py         ← hook: bloquea secrets en Bash
        ├── log_escritura.py         ← hook: registra archivos escritos
        ├── codear.sh                ← shortcut modo ejecución
        ├── discutir.sh              ← shortcut modo discusión
        ├── credenciales.md          ← credenciales de servicios
        └── aviso_*.mp3              ← sonidos de aviso
```

---

## 2. INSTALACIÓN — primera vez

### Paso 1 — Copiar el sistema a tu proyecto

```bash
# Copiar desde version2/ a la raíz de tu proyecto nuevo
cp -r version2/. mi-proyecto/
cd mi-proyecto
```

### Paso 2 — Instalar Claude Code (si no lo tenés)

```bash
npm install -g @anthropic-ai/claude-code
```

### Paso 3 — Abrir Claude Code en el proyecto

```bash
cd mi-proyecto
claude
```

Claude va a leer `CLAUDE.md` automáticamente al iniciar.

### Paso 4 — Verificar el global (ya instalado en esta máquina)

`~/.claude/CLAUDE.md` ya existe con tu stack y preferencias personales.
Aplica a todos tus proyectos automáticamente — no hace falta tocarlo.

---

## 3. PRIMER USO — proyecto virgen

Cuando Claude arranca en un proyecto sin `claude/`, detecta que es virgen
y sigue este flujo automáticamente:

```
Claude lee CLAUDE.md + STACK.md
    ↓
Claude detecta el stack del proyecto
    ↓
Claude propone roadmap (Etapas → Sub-etapas → Pasos)
    ↓
Vos aprobás o ajustás con R:/
    ↓
Claude crea la estructura claude/ y arranca
```

---

## 4. FLUJO DE TRABAJO DIARIO

### Abrir sesión

```bash
claude                                    # modo normal
bash claude/acciones/codear.sh            # shortcut modo ejecución
bash claude/acciones/discutir.sh [tema]   # shortcut modo discusión
```

Claude lee `claude/estado.log` y `claude/RESUMEN.md` y te presenta
el contexto de dónde quedó la última sesión.

### Dos modos de trabajo

#### 💬 Modo Discusión (por defecto)
Claude NO escribe código. Discute, analiza, propone.
Todo el contenido va a `claude/discusiones/disc_[tema].md`.
El chat se mantiene en una sola línea.

```
vos describís una idea o problema
    ↓
Claude crea disc_[tema].md y avisa por WhatsApp
    ↓
Vos leés el archivo y respondés en el chat
```

#### ⚡ Modo Ejecución (activado por `0`)
Claude escribe código, crea archivos, ejecuta comandos.
Sigue el checklist de `claude/planes/plan_XXX.md` y tacha tareas.

---

## 5. COMANDOS DE CONTROL

| Comando | Cuándo usarlo | Qué hace Claude |
|---|---|---|
| `1` | Después de leer un disc_ | Relee el archivo, actualiza si hay cambios, avisa |
| `R:/ [texto]` | En cualquier momento | Para todo, incorpora tu feedback al disc_, confirma |
| `revisa` | Después de agregar notas al disc_ | Incorpora los cambios, actualiza el archivo |
| `0` | Cuando aprobás una discusión | Genera plan_XXX.md y empieza a ejecutar |

> `R:/` tiene prioridad absoluta — Claude para lo que está haciendo y lo incorpora.

---

## 6. CÓMO FUNCIONAN LOS SKILLS

Los skills son archivos `.md` en `.claude/skills/` que Claude carga
automáticamente según el stack que detecta en el proyecto.

| Si el proyecto tiene | Claude carga |
|---|---|
| `manage.py` + `vite.config.*` | django-drf + react-vite |
| `manage.py` solo | django-drf |
| `pubspec.yaml` | flutter |
| `app.json` + expo | react-native |
| `.sln` o `.csproj` | winforms |
| `docker-compose` + n8n | n8n-flows |
| `package.json` + vite | react-vite |

Con el skill cargado, Claude ya sabe las convenciones, estructura de
carpetas, patrones de código y comandos de tu stack — sin que tengas
que explicárselo.

**Para agregar un skill nuevo:**
Crear `.claude/skills/[nombre]/SKILL.md` con este formato:
```markdown
# Skill: Nombre
name: nombre
description: Cuándo se activa (palabras clave que lo disparan)
allowed tools: Read, Grep, Glob, Edit, Write, Bash
---
(convenciones, patrones, comandos)
```

---

## 7. CÓMO FUNCIONAN LOS HOOKS

Los hooks en `.claude/settings.json` se ejecutan automáticamente
sin que Claude lo decida. Son deterministas.

| Hook | Cuándo | Script | Qué hace |
|---|---|---|---|
| PreToolUse Bash | Antes de cada comando | `check_secrets.py` | Bloquea si detecta un secret hardcodeado |
| PostToolUse Write | Después de cada write | `log_escritura.py` | Registra archivo + timestamp en `escrituras.log` |
| Notification | Cuando Claude notifica | `notificar.py` | Reproduce sonido + manda WhatsApp |

---

## 8. SISTEMA DE AVISOS

Tres tipos de aviso — cada uno con sonido diferente y mensaje de WhatsApp:

```bash
python claude/acciones/avisar.py "mensaje" suave    # 💬 discusión lista
python claude/acciones/avisar.py "mensaje" normal   # ✅ etapa terminada
python claude/acciones/avisar.py "mensaje" urgente  # 🚨 error o alerta
```

Las credenciales de WhatsApp (Callmebot) están en `claude/acciones/credenciales.md`.
Si una credencial expira, marcá `Estado: expirada` y Claude te pedirá una nueva.

---

## 9. IMÁGENES DE REFERENCIA

Dos carpetas para dar contexto visual a Claude sin explicar nada:

| Carpeta | Cuándo usarla |
|---|---|
| `claude/imagenes/errores/` | Screenshots de bugs, comportamientos incorrectos |
| `claude/imagenes/mejoras/` | Referencias de UI, diseños, ideas a implementar |

**Uso:** subís la imagen a la carpeta y en el chat mencionás "error" o "mejora".
Claude lista la carpeta, toma la más reciente y la usa como contexto.

---

## 10. CIERRE DE ETAPA

Al terminar cada etapa, Claude ejecuta esto en orden:

```bash
git status                                     # verificar cambios
python claude/acciones/backup_n8n.py [N]       # backup n8n (si el stack lo usa)
python claude/acciones/backup_sql.py [N]       # backup PostgreSQL (si hay DB)
python claude/acciones/avisar.py "Etapa XX terminada" normal
```

Y actualiza:
- `claude/estado.log` — estado granular (etapa, paso, deuda, próximo)
- `claude/RESUMEN.md` — resumen en 5 líneas
- `claude/discusiones/INDEX.md` — marcar disc como completada

---

## 11. PERMISOS — qué puede hacer Claude sin preguntar

| Acción | Permiso |
|---|---|
| Leer cualquier archivo | ✅ Automático |
| `git status/diff/log/pull` | ✅ Automático |
| `npm install/run/test` | ✅ Automático |
| `pip install`, `python manage.py *` | ✅ Automático |
| `flutter *`, `npx expo *`, `dotnet *` | ✅ Automático |
| Escribir `.md .py .js .ts .jsx .tsx .vb .cs .json .html .css .xml` | ✅ Automático |
| `mkdir`, `ls` | ✅ Automático |
| `git merge`, `rm -rf` | ⏸ Pide aprobación |
| `git commit` | 🚫 Nunca |
| `git push` | 🚫 Nunca |
| Escribir `.env` | 🚫 Nunca |
| Leer `.env` | 🚫 Nunca |

---

## 12. RECUPERAR CONTEXTO ENTRE SESIONES

Al abrir Claude en un proyecto existente, presenta automáticamente:

```
📍 CONTEXTO RECUPERADO
──────────────────────────────────────────────
Proyecto     : mi-proyecto
Stack        : Django + React + PostgreSQL
Etapa        : 03-Dashboard
Sub-etapa    : 3.2-Gráficos
Paso actual  : 3.2.1-Componente BarChart
Última acción: serializer de métricas terminado
Pendiente    : conectar datos reales al componente
──────────────────────────────────────────────
Listo. ¿Continuamos o hay algo nuevo?
```

Toda esa información viene de `claude/estado.log`.

---

## 13. REGLAS QUE CLAUDE NUNCA ROMPE

- No escribe código sin checklist generado desde discusión aprobada (`0`)
- No hace `git commit` ni `git push`
- No escribe secrets en código ni en `.env`
- No termina una etapa sin hacer backup, actualizar `estado.log` y avisar
- No arranca una etapa nueva sin verificar `git status`
- No crea `claude/` si ya existe
- No borra imágenes de `claude/imagenes/`
- No usa una credencial sin verificarla en `credenciales.md`

---

## 14. AGREGAR UN PROYECTO NUEVO

1. Copiar `version2/` como base
2. Abrir Claude Code: `claude`
3. Claude detecta el stack y propone el roadmap
4. Aprobar con `0` o ajustar con `R:/`
5. Claude crea la estructura y arranca

---

_Sistema v6.0 — ver `CLAUDE.md` para el protocolo completo_
