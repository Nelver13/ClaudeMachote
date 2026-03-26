# 📇 Index — Version3Ligera

**Todos los archivos principales en un lugar.**

---

## 🚀 START HERE

| Archivo | QUÉ LEER | CUÁNDO |
|---|---|---|
| **[MANUAL_IMPLEMENTACION.md](MANUAL_IMPLEMENTACION.md)** | 📖 **Manual completo** | Implementar desde cero |
| **[QUICKSTART.md](QUICKSTART.md)** | 5 min tutorial | Primer uso |
| **[SUMMARY.md](SUMMARY.md)** | Overview técnico | Entender qué es |
| **[README_DASHBOARD.md](README_DASHBOARD.md)** | Documentación completa | Referencia |

---

## 📊 DOCUMENTACIÓN (nivel tecnico)

### Core System
| Archivo | Contenido |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Global rules (proyecto meta) |
| [MOTOR.md](MOTOR.md) | Auto-detection logic |
| [FLUJO.md](FLUJO.md) | Workflow base |
| [STACK.md](STACK.md) | Tech stack |

### Estado & Progreso
| Archivo | Contenido |
|---|---|
| [ESTADO.md](ESTADO.md) | Status detallado + checklist |
| [IMPLEMENTAR_HANDLERS.md](IMPLEMENTAR_HANDLERS.md) | Cómo completar command handlers |
| **[MANUAL_IMPLEMENTACION.md](MANUAL_IMPLEMENTACION.md)** | 📖 **Guía completa de implementación** |

### Referencia
| Archivo | Contenido |
|---|---|
| [README_DASHBOARD.md](README_DASHBOARD.md) | Dashboard reference completa |

---

## 💻 CÓDIGO FUENTE

### Backend (Python + Flask)
| Archivo | Función | Líneas |
|---|---|---|
| `claude/dashboard/app.py` | Flask app + routes | ~300 |
| `claude/acciones/init_db.py` | SQLite schema | ~150 |
| `claude/acciones/sync_tokens.py` | JSON→SQLite | ~100 |
| `claude/acciones/log_tokens.py` | Token logger | ~80 |
| `claude/acciones/gen_report.py` | Report generator | ~120 |
| `claude/acciones/motor_detect.py` | IDE detector | ~100 |

### Frontend (HTML + JavaScript)
| Archivo | Función | Features |
|---|---|---|
| `claude/dashboard/templates/index.html` | Dashboard UI | 5 tabs, auto-refresh |
| `claude/dashboard/static/` | CSS/JS | (incluido inline en HTML) |

### Scripts Auxiliares
| Archivo | Función |
|---|---|
| `claude/acciones/iniciar_dashboard.py` | Cross-platform launcher |
| `claude/acciones/iniciar_dashboard.bat` | Windows launcher |
| `claude/acciones/README.md` | Instructions |

---

## 📁 ESTRUCTURA DE CARPETAS

### version3ligera/ (raíz)
```
version3ligera/
├── QUICKSTART.md              ← ⭐ Comienza aquí
├── SUMMARY.md                 ← Overview técnico
├── README_DASHBOARD.md        ← Docs completas
├── ESTADO.md                  ← Status + checklist
├── IMPLEMENTAR_HANDLERS.md    ← Next steps
├── INDEX.md                   ← Este archivo
├── CLAUDE.md                  ← Global config
├── MOTOR.md                   ← Auto-detect
├── FLUJO.md                   ← Workflow
├── STACK.md                   ← Tech
├── .motor/
│   └── motor.json            ← Motor config (auto-gen)
└── motores/                  ← Por-IDE context
    ├── claude/
    ├── cursor/
    ├── copilot/
    └── antigravity/
```

### claude/ (working area)
```
claude/
├── discusiones/              ← Tus discussiones
│   ├── borrador/             ← En edición (disc_*.md)
│   └── final/                ← Aprobadas
├── planes/                   ← Planes (plan_*.md)
├── reports/                  ← SQLite db
├── logs/                     ← Token events (JSON)
├── dashboard/                ← Flask app
│   ├── app.py                ← Main (NO TOCAR)
│   ├── templates/
│   │   └── index.html        ← HTML (5 tabs)
│   └── requirements.txt       ← Dependencies
└── acciones/                 ← Scripts
    ├── init_db.py
    ├── sync_tokens.py
    ├── log_tokens.py
    ├── gen_report.py
    └── ... más scripts
```

---

## 🎯 QUICK NAVIGATION

### Si quiero...

**...entender qué es esto**
→ [SUMMARY.md](SUMMARY.md) (3 min)

**...empezar ahora**
→ [QUICKSTART.md](QUICKSTART.md) (5 min)

**...saber status actual**
→ [ESTADO.md](ESTADO.md) (10 min)

**...implementar handlers**
→ [IMPLEMENTAR_HANDLERS.md](IMPLEMENTAR_HANDLERS.md) (20 min)

**...referencia completa del dashboard**
→ [README_DASHBOARD.md](README_DASHBOARD.md)

**...entender workflow**
→ [FLUJO.md](FLUJO.md)

**...auto-detection**
→ [MOTOR.md](MOTOR.md)

**...tech stack**
→ [STACK.md](STACK.md)

**...global rules**
→ [CLAUDE.md](CLAUDE.md)

**...ver todo mapeado**
→ Este archivo (INDEX.md)

---

## ⚡ COMANDOS ÚTILES

```bash
# Iniciar dashboard
cd version3ligera/claude
python iniciar_dashboard.py

# Abrir en navegador
http://localhost:5000

# Ver logs
tail -f logs/tokens.json

# Crear discusión manual
touch claude/discusiones/borrador/disc_FECHA.md

# Crear plan manual
touch claude/planes/plan_NNN.md

# Sincronizar tokens a SQLite
python acciones/sync_tokens.py

# Generar reporte HTML
python acciones/gen_report.py
```

---

## 📈 ROADMAP

### ✅ Hecho
- [x] Auto-detection (`.motor/motor.json`)
- [x] Dashboard HTML 5-tabs
- [x] SQLite schema (5 tablas)
- [x] Flask endpoints (7 routes)
- [x] Command handlers (gen_disc, etc)
- [x] Token logging system

### 🔄 En Progreso
- [ ] Real token event in/out
- [ ] Etapa automation
- [ ] Plan executor

### 📋 Pendiente
- [ ] Tests integración
- [ ] UI mejorada (Tailwind)
- [ ] Gráficos (Chart.js)
- [ ] Export Excel

---

## 🔗 FILE DIAGRAM

```
INDEX.md (tú estás aquí)
├── QUICKSTART.md ← Empieza aquí
├── SUMMARY.md ← Overview
├── README_DASHBOARD.md ← Referencia UI
├── ESTADO.md ← Status actual
├── IMPLEMENTAR_HANDLERS.md ← Próximos pasos
├── CLAUDE.md ← Global config
├── MOTOR.md ← Auto-detect
├── FLUJO.md ← Workflow
└── STACK.md ← Tech

código/
├── claude/dashboard/app.py (Flask)
├── claude/dashboard/templates/index.html (5 tabs)
└── claude/acciones/ (scripts)
```

---

## 💡 TIPS

**Todas las decisiones arquitectónicas están documentadas en estos archivos.**

**Si algo no está claro:**
1. Busca en INDEX.md (este archivo)
2. Lee SUMMARY.md (overview)
3. Consulta README_DASHBOARD.md (detalle)

**Si quieres agregar features:**
1. Lee ESTADO.md (checklist)
2. Lee IMPLEMENTAR_HANDLERS.md (patrón)
3. Sigue el mismo patrón

---

**Última actualización:** 2025-01-21  
**Versión:** 3.ligera (v1.0)

🚀 **Listo para empezar? Abre [QUICKSTART.md](QUICKSTART.md)**
