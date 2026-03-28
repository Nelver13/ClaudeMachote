# ClaudeMachote — Dual AI System

Sistema de colaboracion entre dos IAs:
- **Gemini** = Arquitecto (discute, diseña, genera planes)
- **Claude** = Desarrollador (lee planes, escribe codigo, marca [x])

---

## Requisitos

- [Claude Code](https://claude.ai/code) — ejecutor
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) — arquitecto
- Python 3.x — para scripts de avisos

---

## Estructura

```
ClaudeMachote/
├── CLAUDE.md           <- instrucciones para Claude (developer)
├── GEMINI.md           <- instrucciones para Gemini (architect)
├── README.md           <- este archivo
├── .gitignore
└── claude/             <- workspace compartido (no va a git)
    ├── acciones/       <- scripts: avisar.py, credenciales.md, etc.
    ├── discusiones/    <- disc_*.md generados por Gemini
    │   ├── creaciones/ <- nuevas features
    │   └── soluciones/ <- bugs y fixes
    ├── planes/         <- plan_*.md generados por Gemini, ejecutados por Claude
    ├── backups/        <- backups de DB y n8n
    ├── logs/           <- logs de ejecucion
    ├── RESUMEN.md      <- estado del proyecto (max 5 lineas)
    └── estado.log      <- estado granular actual
```

---

## Flujo de trabajo

### 1. Arquitecto habla con Gemini
```bash
gemini "quiero implementar autenticacion JWT"
```
Gemini crea `claude/discusiones/disc_auth.md` con analisis y propuesta.

### 2. Arquitecto revisa y aprueba
```
1        <- re-leer el .md
R:/ ...  <- agregar feedback
0        <- aprobar y generar plan
```
Gemini genera `claude/planes/plan_001.md` y avisa.

### 3. Arquitecto abre Claude Code
```bash
claude
# Claude lee el plan y pregunta si ejecuta
s        <- ejecutar siguiente tarea
```
Claude ejecuta tarea por tarea, marcando [x] en el plan.

### 4. Revision y cierre
Claude avisa al terminar. Arquitecto revisa, hace git commit si conforme.

---

## Setup inicial

```bash
# Clonar o iniciar repo
git clone <repo> && cd ClaudeMachote

# Instalar dependencias de scripts (si aplica)
pip install requests

# Configurar credenciales (Discord, Callmebot, etc.)
# Editar: claude/acciones/credenciales.md
```

---

## Scripts disponibles

| Script | Uso |
|---|---|
| `avisar.py "msg" suave\|normal\|urgente` | Notificacion con sonido |
| `backup_n8n.py [etapa]` | Backup de flujos n8n |
| `backup_sql.py [etapa]` | Backup de base de datos |
| `finalizar_etapa.py` | Cierre de etapa automatizado |

---

## Reglas de oro

- Gemini no escribe codigo. Claude no crea planes.
- git commit/push solo lo hace el arquitecto (humano).
- `claude/` nunca va a git.
- Credenciales siempre en `claude/acciones/credenciales.md`.
