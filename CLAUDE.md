# CLAUDE.md — v5.2 (producción)
> Leé este archivo completo al iniciar. Es todo lo que necesitás.
> La memoria y los scripts del proyecto viven en `/claude/`.
> La carpeta `/claude/` está en `.gitignore` — nunca se sube a git.

---

## 📍 INICIO DE SESIÓN — SIEMPRE

### Si `/claude/` NO existe → proyecto virgen
1. Verificar si existe `acciones/` en la raíz → es la señal de proyecto virgen
2. Leer estructura de archivos → detectar stack (tabla abajo)
3. Leer `STACK.md` si existe en la raíz
4. Proponer roadmap `Etapa → Sub-etapa → Paso`
5. Esperar `R:/` o aprobación
6. Crear estructura base y mover `acciones/` a `claude/` (ver sección PROYECTO VIRGEN)

### Si `/claude/` ya existe → proyecto con historial
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

| Indicador | Stack |
|---|---|
| `manage.py` + `frontend/vite.config.*` | Django + DRF + React + Vite |
| `manage.py` solo | Django + DRF |
| `pubspec.yaml` | Flutter |
| `app.json` + `expo` en `package.json` | React Native + Expo |
| `.sln` o `.csproj` o `.vbproj` | WinForms / C# / VB |
| `docker-compose.yml` con servicio `n8n` | n8n incluido |
| `package.json` + `"vite"` sin `manage.py` | React + Vite standalone |

Si no puede determinar → pregunta antes de asumir.

---

## 🧭 CICLO COMPLETO

```
IDEA (+ imagen opcional)
      ↓
Claude analiza → crea disc_[tema].md
      ↓
Chat: "📝 disc_[tema].md — marca 1 cuando hayas leído"
      ↓
┌─────────────────────────────────────┐
│  CICLO DE RETROALIMENTACIÓN         │
│                                     │
│  Arquitecto lee → responde/corrige  │
│        ↓                            │
│  R:/ [texto] → Claude incorpora     │
│        ↓                            │
│  Claude actualiza disc_[tema].md    │
│        ↓                            │
│  Arquitecto marca 1 → re-lee        │
│        ↓                            │
│  ¿Conforme? NO → vuelve arriba      │
└─────────────────────────────────────┘
      ↓ SÍ (arquitecto dice 0)
Discusión marcada: Estado: Aprobado
      ↓
Claude genera plan_XXX.md (checklist)
      ↓
Claude ejecuta solo → tachando tareas
      ↓
Cierre: backup + estado.log + aviso
```

---

## 💬 Modo Discusión (por defecto)
No genera código. Crea y actualiza `.md` en `claude/discusiones/`.
El chat se mantiene en una línea. Todo el contenido va al archivo.

Al iniciar discusión nueva:
1. Si hay imagen → revisar `claude/imagenes/mejoras/` para tomar contexto visual
2. Crear `claude/discusiones/disc_[tema].md` con análisis, propuesta, preguntas y riesgos
3. En el chat decir solo: `📝 disc_[tema].md — marca 1 cuando hayas leído`
4. Ejecutar: `python claude/acciones/avisar.py "disc_[tema].md listo — marca 1" suave`

| Comando | Acción |
|---|---|
| `1` | Re-leer `.md`, actualizar si hay cambios, avisar |
| `revisa` | Incorporar notas del arquitecto, actualizar `.md` |
| `R:/ [texto]` | Parar, incorporar todo en `.md`, confirmar con una línea en el chat |
| `0` | **Aprobado** — marcar `Estado: Aprobado`, generar checklist y arrancar |

> `R:/` tiene prioridad absoluta. Todo lo que venga ahí se lee, se implementa en el `.md` y se confirma antes de seguir.

---

## ⚡ Modo Ejecución — activado automáticamente por `0`

Cuando el arquitecto dice `0`:
1. Marcar `disc_[tema].md` con `Estado: Aprobado`
2. Generar `claude/planes/plan_XXX.md` como checklist basado en la discusión
3. Avisar: `python claude/acciones/avisar.py "plan_XXX.md listo — arrancando" normal`
4. Ejecutar de corrido, marcando `[x]` en cada tarea completada
5. Agregar notas inline si algo surgió durante la ejecución
6. Al terminar todas las tareas → cierre de etapa obligatorio

---

## 📋 PLAN/CHECKLIST — generado automáticamente al `0`

Guardado en `claude/planes/plan_XXX.md`. Claude lo genera y arranca sin esperar aprobación adicional.

```markdown
# Plan #XXX — [Nombre]
**Fecha:** YYYY-MM-DD
**Estado:** En ejecución
**Discusión origen:** disc_[tema].md

## Tareas
- [ ] Tarea 1
  - [ ] Sub-tarea 1.1
  - [ ] Sub-tarea 1.2
- [ ] Tarea 2
- [ ] Tarea 3

## Notas de ejecución
_(Claude agrega notas aquí mientras trabaja — cambios, problemas, decisiones)_
```

Claude actualiza el archivo en tiempo real: `[ ]` → `[x]` al completar cada tarea.
El checklist es la memoria compartida del estado real de la ejecución.

---

## 💾 CIERRE DE ETAPA — obligatorio

Al terminar cada etapa o sub-etapa, en este orden:

```bash
# 1. Verificar git
git status
# Si hay cambios → avisar y esperar "listo, seguimos"

# 2. Backup n8n
python claude/acciones/backup_n8n.py [numero_etapa]

# 3. Avisar
python claude/acciones/avisar.py "Etapa XX terminada — revisá para continuar" normal
```

Luego actualizar:
- `claude/estado.log` — estado granular actual
- `claude/RESUMEN.md` — máximo 5 líneas
- `claude/acciones/README.md` — si cambió algo en el stack

### Formato estado.log
```
[PROJ: nombre]
[STACK: Django|React|PostgreSQL]
[ETAPA: 02-Create]
[SUB-ETAPA: 2.1-Serializer]
[PASO: 2.1.2-Vista POST]
[LAST_FILE: apps/usuarios/views.py]
[LAST_TASK: descripción breve]
[NEXT: próximo paso concreto]
[DB: 0/1]
[DEBT: L/M/H]
```

---

## 🔔 AVISOS — siempre doble (sonido + WhatsApp)

| Tipo | Cuándo | Comando |
|---|---|---|
| `suave` | Discusión actualizada, "marca 1" | `python claude/acciones/avisar.py "mensaje" suave` |
| `normal` | Etapa terminada, plan guardado, paso listo | `python claude/acciones/avisar.py "mensaje" normal` |
| `urgente` | Error inesperado, secreto detectado, git sin push | `python claude/acciones/avisar.py "mensaje" urgente` |

---

## 🔑 CREDENCIALES DE CLAUDE

Guardadas en `claude/acciones/credenciales.md`. Viajan dentro de `acciones/` — al mover la carpeta en proyecto virgen, las credenciales quedan en su lugar automáticamente.

### Lógica de permiso
> **Tener la credencial = tener permiso de usarla.**
> Si está en `claude/credenciales.md` → Claude la usa directamente, sin preguntar.
> Si no está → Claude para y la pide antes de continuar.

### Flujo
- Antes de acceder a cualquier servicio externo (n8n, API, webhook, DB remota) → leer `claude/credenciales.md`
- Si el arquitecto da una credencial en el chat → guardarla en el archivo antes de usarla
- Si una credencial falla → marcarla `expirada` y pedir una nueva

### Formato
```markdown
# Credenciales

## Callmebot
- PHONE: +[tu número con código de país]
- API_KEY: [tu apikey de Callmebot]
- Estado: activa | expirada

## n8n
- URL: http://localhost:5678
- API_KEY: [valor]
- Estado: activa | expirada

## [Servicio]
- API_KEY: [valor]
- Estado: activa | expirada

## Notas
_(tokens temporales, instrucciones especiales)_
```

---

## 🔐 SEGURIDAD + GITIGNORE

Nunca escribir secrets en código. Siempre `.env` + `.env.example`.
Si detecta secreto hardcodeado → parar y señalar antes de continuar.

Crear/actualizar `.gitignore` en proyecto virgen o cuando cambia el stack:

```gitignore
# Carpeta claude — nunca a git (memoria, scripts, backups, credenciales)
claude/

# Entorno
.env
.env.local
.env.*.local
*.log
.DS_Store
Thumbs.db

# Django
__pycache__/
*.pyc
db.sqlite3
media/
staticfiles/

# React + Vite
node_modules/
dist/
.vite/

# Expo
.expo/
android/build/
ios/build/
*.ipa
*.apk

# Flutter
build/
.dart_tool/

# WinForms
bin/
obj/
*.user
*.suo
.vs/
```

---

## 📝 ESTÁNDARES DE CÓDIGO

Bloque al inicio de cada archivo nuevo:
```
# ARCHIVO: nombre
# QUÉ HACE: descripción simple
# CÓMO ENCAJA: conexión con el resto
# PARA EDITAR: qué saber antes de tocarlo
# DEPENDENCIAS: qué necesita
```

---

## 🖥️ TERMINAL — permisos

| Acción | Permiso |
|---|---|
| `npm/pip install`, crear archivos | ✅ Automático |
| `ls`, `cat`, tests | ✅ Automático |
| `git status/diff/log` | ✅ Automático |
| `git pull` | ✅ Automático |
| `.gitignore` crear/actualizar | ✅ Automático |
| `python claude/acciones/avisar.py` | ✅ Automático |
| `python claude/acciones/backup_n8n.py` | ✅ Automático |
| `git merge`, `rm -rf` | ⏸ Aprobación explícita |
| `git commit` | 🚫 Nunca |
| `git push` | 🚫 Nunca |

---

## 🚀 PROYECTO VIRGEN — crear estructura base

Solo tras aprobación del roadmap. Solo una vez. Nunca sobreescribir si ya existe.

```bash
# 1. Crear estructura claude/
mkdir -p claude/planes claude/discusiones claude/backups/n8n claude/backups/sql claude/imagenes/errores claude/imagenes/mejoras

# 2. Mover acciones/ de la raíz a claude/
mv acciones/ claude/acciones/

# 3. Completar scripts que faltan en claude/acciones/
```

Archivos a crear dentro de `claude/acciones/` (los que no existen aún):
- `claude/acciones/iniciar.sh` — según stack detectado
- `claude/acciones/avisar.py` — script de avisos
- `claude/acciones/backup_n8n.py` — script de backup n8n
- `claude/acciones/README.md` — documentación

Archivos a crear en `claude/`:
- `claude/RESUMEN.md` — plantilla vacía
- `claude/estado.log` — en blanco
_(credenciales.md ya viaja dentro de acciones/ — no hace falta crearla aparte)_

Archivo a crear en raíz:
- `.gitignore` — según stack (incluye `claude/`)

> Los sonidos `aviso_*.mp3` que estaban en `acciones/` se mueven junto con la carpeta — quedan en `claude/acciones/`.

---

## 🖼️ CARPETAS DE REFERENCIA VISUAL

Claude tiene dos carpetas de imágenes de referencia que el arquitecto mantiene:

```
claude/imagenes/
├── errores/    ← screenshots de errores, bugs visuales, comportamientos incorrectos
└── mejoras/    ← referencias de UI, flujos, diseños o ideas a implementar
```

### Cuándo las usa Claude

| El arquitecto menciona | Claude hace |
|---|---|
| "error", "bug", "no funciona", "mirá esto" | Busca en `claude/imagenes/errores/` y usa las imágenes como contexto para diagnosticar |
| "mejora", "quiero esto", "implementá algo así", "inspirate" | Busca en `claude/imagenes/mejoras/` y usa las imágenes como referencia visual para implementar |

### Cómo el arquitecto las usa
- Subís la imagen a la carpeta correspondiente
- En el chat mencionás "error" o "mejora" y Claude va a buscarla
- No necesitás decir el nombre del archivo — Claude lista la carpeta y toma la más reciente
- Si hay varias imágenes relevantes → Claude las menciona todas antes de actuar

### Reglas
- Claude nunca borra imágenes de estas carpetas
- Si encuentra una imagen ambigua → pregunta antes de asumir
- Las imágenes de `errores/` se archivan en `claude/backups/` al cerrar la etapa

---

## 🚫 CLAUDE NUNCA

- Escribe código sin checklist generado desde una discusión aprobada
- Genera el checklist sin que el arquitecto haya dicho `0`
- Ejecuta `git commit` o `git push`
- Escribe secretos en código
- Repite en el chat lo que escribió en un `.md`
- Ignora `R:/`, `revisa`, `1` o `0`
- Termina etapa sin backup, estado.log y aviso
- Crea `/claude/` si ya existe
- Borra imágenes de `claude/imagenes/errores/` o `claude/imagenes/mejoras/`
- Asume qué imagen usar sin listar la carpeta primero
- Arranca etapa nueva sin verificar git status
- Sube la carpeta `claude/` a git
- Usa una credencial sin verificar primero en `claude/credenciales.md`
