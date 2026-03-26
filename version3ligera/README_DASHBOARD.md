# 🚀 Version3Ligera — Dashboard Control Center

## ¿Qué es?
Dashboard central para gestionar proyectos con **múltiples motores AI** (Claude, Cursor, Copilot, Google Antigravity).

## Características Principales

✅ **Auto-Detección de Motor**
- Detecta automáticamente qué IDE/motor está activo
- Cambia contexto sin intervención manual

✅ **6 Tabs de Control**
1. **📊 Home** — Overview en vivo
2. **📄 Discusiones** — Borradores vs Finales
3. **📋 Planes** — Checklist con progreso %
4. **💰 Tokens** — Costos por etapa/motor
5. **⚙️ Comandos** — Botones para ejecutar agentes
6. **📊 Reportes** — Analytics por etapa

✅ **SQLite Backend**
- Persistencia de tokens/costos
- Queries por etapa/motor
- Reportes generados automáticamente

## Cómo Iniciar

### Opción 1: Script Python (recomendado)
```bash
cd version3ligera/claude
python iniciar_dashboard.py
```

### Opción 2: Script Batch (Windows)
```cmd
cd version3ligera\claude
iniciar_dashboard.bat
```

### Opción 3: Manual
```bash
cd version3ligera/claude/dashboard
python app.py
```

## URL
```
http://localhost:5000
```

El dashboard se abre automáticamente. Si no, ingresa manualmente en tu navegador.

## Carpetas Clave

```
claude/
├── dashboard/              ← Flask app (app.py + templates)
├── discusiones/
│   ├── borrador/          ← Discusiones en edición (disc_*.md)
│   └── final/             ← Discusiones aprobadas
├── planes/                ← Plans con progreso (plan_*.md)
├── reports/               ← SQLite database (reports.db)
├── logs/                  ← Token events (tokens.json)
└── acciones/
    ├── init_db.py         ← Crea schema SQLite
    ├── sync_tokens.py     ← JSON→DB sync
    └── log_tokens.py      ← Registra eventos
```

## Endpoints API

| Endpoint | Método | Función |
|---|---|---|
| `/api/status` | GET | Dashboard data completo |
| `/api/motors` | GET | Motores disponibles |
| `/api/switch-motor/<motor>` | POST | Cambiar motor activo |
| `/api/tokens/etapas` | GET | Tokens agrupados por etapa |
| `/api/tokens/motores` | GET | Stats por motor |
| `/api/comandos/ejecutar` | POST | Ejecuta agente (gen_discusión, ejecutar_plan, etc) |
| `/api/reportes/etapas` | GET | Últimas 20 etapas |

## Comandos Disponibles (Tab Comandos)

```
🔌 Motor: Claude        ← Cambiar a Claude
🔌 Motor: Cursor        ← Cambiar a Cursor
📝 Gen Discusión        ← Crear nueva discusión
▶️ Ejecutar Plan         ← Correr plan_*.md
📊 Gen Reporte          ← Generar reporte etapa
⬇️ Sync Tokens          ← JSON→SQLite sync
```

## Configuración

### Variables de entorno
Crear `.env` en `version3ligera/claude/`:
```
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

### motor.json
Localizado en `version3ligera/.motor/motor.json`:
```json
{
  "active_motor": "claude|cursor|copilot|antigravity",
  "detected_motor": "auto-detected value",
  "version": "3.ligera"
}
```

## Workflow Recomendado

1. **Abrir Dashboard**
   ```bash
   python iniciar_dashboard.py
   ```

2. **Crear Discusión** (Tab Comandos)
   - Click "📝 Gen Discusión"
   - Se crea `discusiones/borrador/disc_*.md`

3. **Revisar Discusión**
   - Tab "📄 Discusiones"
   - Lee en el IDE
   - Aprueba o edita

4. **Mover a Final**
   - Cuando esté OK, mueve a `discusiones/final/`

5. **Crear Plan** (desde borrador aprobado)
   - Click "▶️ Ejecutar Plan"
   - Tab "📋 Planes" para ver progreso

6. **Ver Tokens**
   - Tab "💰 Tokens"
   - Breakdown por etapa/motor
   - Costos acumulados

7. **Generar Reporte**
   - Click "📊 Gen Reporte"
   - Tab "📊 Reportes" para descargar

## Troubleshooting

**Dashboard no abre en navegador**
```bash
# Manual: ingresa en tu navegador
http://localhost:5000
```

**Error: ModuleNotFoundError (Flask)**
```bash
pip install Flask==2.3.0
```

**Error: SQLite database locked**
- Solo una instancia de dashboard debe correr
- Cierra otras pestañas/terminales

**Motor no detecta**
- Verifica `.motor/motor.json` existe
- Ejecuta `python claude/acciones/motor_detect.py`

## Archivos Importantes

| Archivo | Propósito |
|---|---|
| `dashboard/app.py` | Flask app + routes |
| `dashboard/templates/index.html` | UI con 5 tabs |
| `dashboard/static/` | CSS/JS (incluido en HTML) |
| `acciones/init_db.py` | Crea SQLite schema |
| `reports/reports.db` | Base de datos SQLite |
| `logs/tokens.json` | Eventos de tokens (JSON) |

## Notas Importantes

⚠️ **No subir a Git:**
- `reports/reports.db` (datos)
- `logs/tokens.json` (datos)
- Un `.gitignore` ya tiene excluido `claude/`

✅ **Sí subir a Git:**
- `dashboard/app.py`
- `dashboard/templates/index.html`
- `acciones/init_db.py`, `sync_tokens.py`
- Este README

---

**Última actualización:** 2025-01-21  
**Versión:** 3.ligera (v1.0)
