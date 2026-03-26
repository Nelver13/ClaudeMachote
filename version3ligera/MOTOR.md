# MOTOR v3 Ligera
> Sistema agnóstico de IA. Funciona con Copilot, Claude, Cursor, Google Antigravity.
> Flujo: discusión → aprobación → ejecución | Dashboard de progreso | Credenciales centralizadas

---

## 🎯 Qué es

Un **meta-sistema** que detecta qué IDE/motor de IA estás usando y adapta el flujo automáticamente.

- **Copilot en VS Code** → usa chat integrado + instrucciones
- **Claude en VS Code** → usa Claude, instrucciones + avisos
- **Cursor IDE** → auto-detecta, ajusta prompts
- **Google Antigravity** → adaptación de API

---

## 📁 Estructura

```
version3ligera/
├── .motor/
│   ├── motor.json          ← Detecta qué motor activo
│   ├── copilot.schema      ← Config para Copilot
│   ├── claude.schema       ← Config para Claude
│   ├── cursor.schema       ← Config para Cursor
│   └── antigravity.schema  ← Config para Google
├── claude/
│   ├── acciones/           ← Scripts Python/bash
│   ├── discusiones/        ← disc_[tema].md
│   ├── planes/             ← plan_XXX.md (checklist)
│   ├── dashboard/          ← App visualización
│   ├── imagenes/           ← errores/ + mejoras/
│   └── RESUMEN.md
├── .gitignore
├── MOTOR.md                ← Este archivo
├── FLUJO.md                ← Workflow (discusión → 0 → ejecución)
└── credenciales.md         ← API keys centralizadas
```

---

## 🔄 Flujo — es igual para todos los motores

```
IDEA
  ↓
Motor IA crea disc_[tema].md
  ↓
Arquitecto: "marca 1 cuando hayas leído"
  ↓
[FEEDBACK loop: revisa / R:/ / 1 / final ]
  ↓ cuando dice "0" (aprobado)
Motor genera plan_XXX.md
  ↓
Motor EJECUTA → checklist [x]
  ↓
Cierre: backup + estado
```

| Comando | Motor hace |
|---------|-----------|
| `1` | Re-lee disc_[tema].md, actualiza si hay cambios |
| `R:/ [nota]` | Incorpora nota en disc_[tema].md, confirma |
| `revisa` | Lee feedback, actualiza doc |
| `0` | Marca aprobado → genera plan_XXX.md → ARRANCA |

---

## 🔌 Motor Activo

Guardado en `.motor/motor.json`:

```json
{
  "active": "copilot",
  "available": ["copilot", "claude", "cursor", "antigravity"],
  "timestamp": "2026-03-23T10:30:00Z",
  "settings": {
    "max_tokens": 4000,
    "temperature": 0.7,
    "timeout": 300,
    "language": "es"
  },
  "integrations": {
    "notifications": true,
    "dashboard": true,
    "git_integration": false
  }
}
```

---

## 🔑 Credenciales

Archivo: `credenciales.md` (raíz)

```markdown
# Credenciales

## Motor API Keys
- COPILOT_KEY: [si usas API]
- CLAUDE_KEY: [si usas API]
- ANTIGRAVITY_KEY: [clave]

## Notificaciones
- CALLMEBOT_PHONE: +[número]
- CALLMEBOT_APIKEY: [key]

## Integraciones
- N8N_URL: http://localhost:5678
- N8N_KEY: [key]

## Estado
- Última actualización: [fecha]
- Keys activas: [list]
- Keys expiradas: [list]
```

**Regla**: Si está en `credenciales.md` → Motor la usa sin preguntar.

---

## 📊 Dashboard

App web simple (Flask) que muestra:
- Motor actual
- Discusiones activas
- Planes en progreso
- % completado
- Última acción

URL: `http://localhost:5000`

---

## 🚀 Comandos Rápidos

```bash
# Ver motor activo
python claude/acciones/motor_status.py

# Cambiar motor (ej: de Copilot a Claude)
python claude/acciones/motor_switch.py claude

# Listar motors disponibles
python claude/acciones/motor_list.py

# Iniciar dashboard
python claude/dashboard/app.py
```

---

## ✅ Primeros Pasos

1. **Abrí version3ligera en tu IDE**
2. **Corre `python claude/acciones/motor_detect.py`** — detecta motor activo
3. **Lee `FLUJO.md`** — entiende el workflow
4. **Crea `credenciales.md`** con tus keys (si necesitás APIs)
5. **Empezá**: Describe una idea, deja que el motor cree `disc_[tema].md`, marca `1`

---

## 🔐 Seguridad

- `claude/` en `.gitignore` — nunca sube a git
- `credenciales.md` también en `.gitignore`
- Motor detecta hardcoded secrets automáticamente
- Avisos van por WhatsApp + sonido (via `avisar.py`)

---

## 🛠️ Para Agregar Otro Motor

1. Crear `[motor].schema` en `.motor/`
2. Crear `detectar_[motor].py` en `claude/acciones/`
3. Actualizar `motor.json`
4. Incluir lógica de traducción de prompts en `motor_adapt.py`
