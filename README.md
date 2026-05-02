
# ClaudeMachote — Sistema Multi-IA para Gestión de Proyectos

Bienvenido al sistema **ClaudeMachote**, una arquitectura basada en roles (Arquitecto y Desarrollador) diseñada para trabajar colaborativamente con IAs como Claude, Kimi, Codex, y Gemini en cualquier proyecto de software.

Este sistema genera un entorno estandarizado que mantiene un historial claro de diseño (planes y discusiones) y previene pérdida de contexto entre sesiones.

---

## 🚀 Instalar en un proyecto nuevo

Copia este prompt y pégalo a la IA en un proyecto vacío:

```text
Instala el sistema multi-IA en este proyecto.

PASO 1 — Clona y ejecuta:
git clone https://github.com/Nelver13/ClaudeMachote.git sistema-ia
python sistema-ia/instalar.py

Eso hace TODO automáticamente:
- Archivos raíz, carpetas, hooks, run scripts
- Discusión 0-vision, backlog bugs
- Dependencias instaladas
- Guía de inicio mostrada

PASO 2 — Configúrame el proyecto. Pregúntame UNA por UNA:
1. ¿Nombre del proyecto?
2. ¿Stack? (backend / frontend / fullstack / mobile / desktop)
3. ¿IAs que van a trabajar? (Claude / Kimi / Codex / Gemini)
4. ¿Rol de cada IA? (ARQUITECTO o DESARROLLADOR)

Con esas respuestas actualiza ESTADO.md y los archivos de IA.

PASO 3 — Listo. Arranca la discusión de visión (0-vision).

Reglas:
- Sin saludos ni relleno. Respuestas cortas.
- Una pregunta a la vez.
- git commit/push/add — NUNCA.
```

---

## 🔄 Actualizar un proyecto existente a la última versión

Copia este prompt y pégalo a la IA en tu proyecto actual:

```text
Actualiza el sistema IA de este proyecto.

PASO 1 — Clona y ejecuta:
git clone https://github.com/Nelver13/ClaudeMachote.git sistema-ia-temp
python sistema-ia-temp/acciones/actualizar.py

El script detecta tu proyecto automáticamente y hace TODO:
- Sincroniza scripts, skills, docs y VERSION
- Crea backup completo antes de tocar nada
- Crea carpetas/archivos que falten
- Instala/verifica dependencias
- Actualiza .gitignore
- Muestra guía de novedades

PASO 2 — Borra el clon temporal:
rm -rf sistema-ia-temp

Listo.

Reglas:
- NO tocar: ESTADO.md, discusiones/, planes/, memoria/, código de producción
- git commit/push/add — NUNCA.
```

---

## 📁 Estructura

```
sistema-ia/
├── acciones/          # Scripts automatizados (avisar, reportar, actualizar...)
├── discusiones/       # Debates de diseño por módulo
│   └── bugs/          # Backlog de bugs + screenshots
├── planes/            # Planes maestros por módulo
├── memoria/           # Progreso y resúmenes
├── handoff/           # Contexto entre sesiones
├── logs/              # Registros de actividad
├── complemento/       # Investigaciones, guías, ideas
├── PROMPT_MAESTRO.md  # Reglas de trabajo del sistema
├── ROADMAP.md         # Mapa de módulos
├── VERSION            # Versión actual del sistema
└── CHANGELOG.md       # Historial de cambios

Raíz del proyecto:
├── ESTADO.md          # Estado actual (módulo, plan, progreso)
├── INICIO.md          # Descripción del proyecto
├── AGENTS.md          # Reglas universales
├── CLAUDE.md          # Instrucciones para Claude
├── KIMI.md            # Instrucciones para Kimi
├── CODEX.md           # Instrucciones para Codex
├── GEMINI.md          # Instrucciones para Gemini
├── run.bat / run.sh   # Levanta el proyecto + bug reporter
└── .claude/
    ├── settings.json  # Hooks de sesión (auto_setup.py)
    └── skills/        # Skills modo-arquitecto / modo-dev
```

---

## 🛠️ Scripts principales

| Script | Uso |
|--------|-----|
| `instalar.py` | Instala el sistema en un proyecto nuevo |
| `acciones/actualizar.py` | Actualiza sistema-ia desde el machote base |
| `acciones/avisar.py` | Avisos con sonido (suave/normal/urgente) |
| `acciones/reportar.py` | Bug reporter con hotkey Alt+R |
| `acciones/auto_setup.py` | Hook de inicio de sesión IA |
| `acciones/guia.py` | Interfaz gráfica de novedades |

---

## 📄 Documentación adicional

- `PROMPT_INSTALAR.md` — Prompt copiar-pegar para instalar
- `PROMPT_ACTUALIZAR.md` — Prompt copiar-pegar para actualizar
- `NOVEDADES.md` — Cambios de la última versión
- `CHANGELOG.md` — Historial completo

---

*Versión actual: ver `VERSION`*
