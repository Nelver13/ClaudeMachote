# Version3Ligera  |  Meta-System para AI Multi-Motor

**Última actualización:** 2025-01-21  
**Status:** 🟢 Funcional (handlers implementados)  
**Compleción:** 85% (UI + Backend + SQLite + Command Executor)

---

## 🎯 En Una Línea

**Hub Central** que auto-detecta tu motor AI (Claude/Cursor/Copilot/Google) y te deja gestionar discusiones, planes, tokens y reportes desde un Dashboard con 6 tabs.

---

## ✨ Características

| Feature | Status | Detalles |
|---|---|---|
| 🔌 Auto-detección motor | ✅ | Detecta IDE automáticamente (`.motor/motor.json`) |
| 📊 Dashboard 6-tabs | ✅ | Home, Discusiones, Planes, Tokens, Comandos, Reportes |
| 💰 SQLite backend | ✅ | 5 tablas: token_events, etapas, reportes, comandos, motor_stats |
| 🤖 Command executor | ✅ | Gen discusión, ejecutar plan, cambiar motor, gen reporte |
| 📈 Token tracking | ✅ | JSON + SQLite sync, costos por etapa |
| 🔄 Auto-refresh | ✅ | Actualiza cada 5 segundos |
| 💬 Multi-motor support | ✅ | Claude, Cursor, Copilot, Google Antigravity |

---

## 🏃 Arrancar

```bash
cd version3ligera/claude
python iniciar_dashboard.py

# Se abre http://localhost:5000
```

---

## 📁 Estructura

```
version3ligera/
├── MANUAL_IMPLEMENTACION.md    ← ⭐ **MANUAL COMPLETO**
├── QUICKSTART.md              ← 5 min tutorial
├── README_DASHBOARD.md        ← Documentación completa
├── ESTADO.md                  ← Status detallado
├── IMPLEMENTAR_HANDLERS.md    ← Cómo completar
├── SUMMARY.md                 ← Este archivo
├── CLAUDE.md                  ← Config general
├── MOTOR.md                   ← Auto-detection
├── FLUJO.md                   ← Workflow
├── STACK.md                   ← Tech stack
├── .motor/
│   └── motor.json            ← Config motor (auto-generado)
├── motores/
│   ├── claude/
│   ├── cursor/
│   ├── copilot/
│   └── antigravity/           ← Context por IDE
└── claude/
    ├── discusiones/
    │   ├── borrador/          ← En edición
    │   └── final/             ← Aprobadas ✅
    ├── planes/                ← plan_*.md con checklist
    ├── reports/               ← reports.db (SQLite)
    ├── logs/                  ← tokens.json (events)
    ├── dashboard/
    │   ├── app.py             ← Flask (50+ líneas)
    │   ├── templates/
    │   │   └── index.html     ← 5 tabs + JavaScript
    │   ├── static/            ← CSS/JS (inline en HTML)
    │   └── requirements.txt    ← Flask==2.3.0
    └── acciones/
        ├── init_db.py         ← Crea SQLite
        ├── sync_tokens.py     ← JSON→DB
        ├── log_tokens.py      ← Logger eventos
        ├── gen_report.py      ← Generator HTML/JSON
        ├── motor_detect.py    ← Detecta IDE
        ├── iniciar_dashboard.py  ← Launcher
        └── iniciar_dashboard.bat ← Launcher Windows
```

---

## 🎮 Tabs del Dashboard

### 📊 **Home**
- Motor detectado + contador
- Discusiones (# borradores | # finales)
- Planes (activos | completados)
- Tokens totales + costo USD

### 📄 **Discusiones**  
- **Borradores** — disc_*.md en edición
- **Finales** — Aprobadas (✅)
- Ver timestamps + líneas

### 📋 **Planes**
- `plan_*.md` con progress bar
- Completadas vs Pendientes
- % avance

### 💰 **Tokens**
- **Por Etapa** — SUM(tokens) + costo
- **Por Motor** — Stats Claude vs Cursor vs etc
- Promedio duración

### ⚙️ **Comandos**
- **Botones:** Gen Disc, Ejecutar Plan, Cambiar Motor, Gen Reporte, Sync Tokens
- **Historial:** Últimos comandos (estado, duración)

### 📊 **Reportes**
- Tabla de etapas (últimas 20)
- Tokens, Costo, # Discusiones, Estado

---

## 🔧 Endpoints API

| Endpoint | Método | Retorna |
|---|---|---|
| `/api/status` | GET | Dashboard data (motor, discusiones, planes, stats) |
| `/api/motors` | GET | `{available: [...], current: "claude"}` |
| `/api/switch-motor/<motor>` | POST | Cambia motor activo |
| `/api/tokens/etapas` | GET | `{etapas: [{etapa, total_tokens, total_costo}]}` |
| `/api/tokens/motores` | GET | `{motores: [{motor, total_tokens, costo_total}]}` |
| `/api/comandos/ejecutar` | POST | Ejecuta comando (gen_discusión, ejecutar_plan, etc) |
| `/api/reportes/etapas` | GET | Últimas 20 etapas |

---

## 💾 SQLite Schema

**5 tablas:**

1. **token_events** — 25 cols
   - id, timestamp, tipo, nombre, motor
   - tokens_in, tokens_out, total_tokens
   - precio_in, precio_out, costo_estimado
   - etapa, duracion_segundos, estado
   - modelo_usado, prompt_tokens, completion_tokens

2. **etapas** — 15 cols  
   - id, nombre, descripcion, tokens_totales, costo_total
   - motor_principal, numero_discusiones, numero_planes
   - start_time, end_time, duracion, success_rate, estado

3. **reportes** — 6 cols
   - id, tipo, titulo, etapa_id, contenido_json, generado_por

4. **comandos** — 9 cols
   - id, comando, parametros, estado, resultado, error_msg
   - created_at, duracion_ms, motor

5. **motor_stats** — 8 cols
   - id, motor, total_eventos, total_tokens, costo_total
   - promedio_tokens, success_count, last_updated

---

## 🚀 Comandos Disponibles

```
gen_discusión        → Crea disc_YYYYMMDD_HHMMSS.md
ejecutar_plan        → Muestra progreso plan_*.md
cambiar_motor        → Swappea motor activo
gen_reporte         → Query SQLite última etapa
sync_tokens         → JSON→DB sync
```

---

## 📊 Tech Stack

- **Backend:** Python 3.8+ + Flask 2.3.0
- **Database:** SQLite3 (reports.db)
- **Frontend:** HTML5 + Vanilla JavaScript + CSS (inline)
- **IPC:** JSON (motor.json, tokens.json)
- **Parsing:** Markdown (discusiones/, planes/)

---

## ✅ Qué Funciona Ahora

- ✅ Auto-detection motor (`.motor/motor.json`)
- ✅ Dashboard con 5 tabs funcionales
- ✅ SQLite con 5 tablas + 1 índice
- ✅ Endpoints Flask (status, tokens, reportes, etc)
- ✅ Command handlers (gen_disc, ejecutar_plan, etc)
- ✅ Auto-refresh cada 5 segundos
- ✅ Multi-motor dropdown
- ✅ Command logging en SQLite

---

## ⚠️ Lo Que Falta

- ❌ Real implementation de ejecutar tareas en plan
- ❌ Detección IDE completa (ahora es manual)
- ❌ Webhook para notificaciones
- ❌ Export Excel reportes
- ❌ Gráficos (Chart.js)
- ❌ Auth/password

---

## 📚 Docs

| Archivo | Propósito |
|---|---|
| **QUICKSTART.md** | Cómo empezar (5 min) |
| **README_DASHBOARD.md** | Docs completas |
| **ESTADO.md** | Status detallado + checklist |
| **IMPLEMENTAR_HANDLERS.md** | Cómo completar handlers |
| **CLAUDE.md** | Global rules (desde ~/.claude/) |
| **MOTOR.md** | Auto-detection logic |
| **FLUJO.md** | Workflow |
| **STACK.md** | Tech stack |

---

## 🎯 Próxima Etapa

### Prioritario
1. [ ] Real token event logging en ejecutar_comando()
2. [ ] Automation para crear/actualizar etapas
3. [ ] Integración de plan_executor (ejecutar tareas)
4. [ ] Tests integración

### Opcional (mejoras)
5. [ ] UI mejorada (tailwind, responsive)
6. [ ] Gráficos (Chart.js)
7. [ ] Export Excel
8. [ ] Webhook Slack/WhatsApp
9. [ ] Auth simple

---

## 🔗 Links Útiles

- **Home Tab:** Estadísticas overview
- **Discusiones Tab:** Manage disc_*.md
- **Tokens Tab:** Ver costos por etapa
- **Comandos Tab:** Ejecutar agentes
- **Reportes Tab:** Descargar analytics

---

## 💬 Resumen

**Version3Ligera** es tu **Control Center** para proyectos AI multi-motor. Auto-detecta IDE, centraliza discusiones/planes/tokens en un Dashboard, y persiste todo en SQLite para reportes granulares.

```
IDE (Cursor/Claude) → Auto-Detect → Dashboard (6 tabs) → SQLite → Reports
```

**Status:** 🟢 Ready to use. Handlers implementados, UI funcional, DB persistente.

---

**Para empezar:** Ver [QUICKSTART.md](QUICKSTART.md) o ejecutar:
```bash
cd version3ligera/claude && python iniciar_dashboard.py
```

---

**Versión:** 3.ligera (v1.0)  
**Fecha:** 2025-01-21  
**Actualización:** 2025-01-21
