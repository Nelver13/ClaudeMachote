# 🚀 Version3Ligera — Guía Rápida

## ¿Qué es Version3Ligera?

**Tu Hub Central** para gestionar proyectos con múltiples motores AI:
- 🔌 **Auto-Detecta** qué IDE/motor usas (Claude, Cursor, Copilot, Google)
- 📊 **Dashboard** con 6 tabs para control total
- 💰 **Token Tracking** automático (costos por etapa)
- 🤖 **Command Executor** para correr agentes
- 📋 **SQLite** para persistencia

---

## ⚡ Quickstart (5 minutos)

### 1. Abrir Terminal
```bash
# Windows
cd f:\GitHub\ClaudeMachote\version3ligera\claude
python iniciar_dashboard.py
```

### 2. Brower se abre automáticamente
```
http://localhost:5000
```

### 3. Ver Dashboard
Te recibe el **Home Tab** con:
- Motor detectado
- Discusiones (borradores vs finales)
- Planes activos
- Tokens totales

---

## 🎮 Cómo Usar (Workflow)

### Opción A: Crear Nueva Discusión
1. Click **Tab "⚙️ Comandos"**
2. Click **"📝 Gen Discusión"** 
3. Se crea `disc_YYYYMMDD_HHMMSS.md` en `discusiones/borrador/`
4. Edita en tu IDE (Cursor/Claude/etc)
5. Cuando esté "OK" → mueve a `discusiones/final/`
6. Tab **"📄 Discusiones"** muestra ambas listas

### Opción B: Ejecutar Plan
1. Click Tab **"📋 Planes"**
2. Ve progreso con % (completados/total)
3. Click Tab **"⚙️ Comandos"** → **"▶️ Ejecutar Plan"**
4. Ejecuta tareas (placeholder por ahora)

### Opción C: Ver Costos/Tokens
1. Click Tab **"💰 Tokens"**
2. Breakdown por **Etapa** y **Motor**
3. Costos estimados en USD
4. % de éxito por motor

### Opción D: Generar Reporte
1. Click Tab **"⚙️ Comandos"**
2. Click **"📊 Gen Reporte"**
3. Tab **"📊 Reportes"** muestra tabla de etapas
4. Descarga/exporta stats

---

## 📂 Carpetas Importantes

```
version3ligera/
├── .motor/
│   └── motor.json          ← Config de motor (auto-generado)
├── motores/                ← Instrucciones por IDE
│   ├── claude/
│   ├── cursor/
│   ├── copilot/
│   └── antigravity/
└── claude/
    ├── discusiones/        ← Tus discussions
    │   ├── borrador/       ← En edición (disc_*.md)
    │   └── final/          ← Aprobadas
    ├── planes/             ← Tus planes (plan_*.md)
    ├── reports/            ← SQLite database
    ├── logs/               ← Token events (JSON)
    ├── dashboard/          ← Flask app (no tocar)
    └── acciones/           ← Scripts auxiliares
```

---

## 🔧 Controles Principales

| Botón | Qué hace |
|---|---|
| **🔌 Motor: Claude/Cursor/Copilot** | Cambiar IDE activo |
| **📝 Gen Discusión** | Crear nueva discussion |
| **▶️ Ejecutar Plan** | Correr último plan_*.md |
| **📊 Gen Reporte** | Generar reporte stats |
| **⬇️ Sync Tokens** | Sincronizar JSON→SQLite |

---

## 📊 Tabs Explicados

### 📊 Home
Overview general:
- Motor detectado
- Contadores (discusiones, planes, tokens)
- Costos acumulados

### 📄 Discusiones
Dos columnas:
- **Borradores** — disc_*.md en edición
- **Finales** — disc_*.md aprobadas

### 📋 Planes
Progress bars:
- `plan_*.md` con checklist
- **Completadas:** `[x]` tareas
- **Pendientes:** `[ ]` tareas

### 💰 Tokens
Breakdown de costos:
- **Por Etapa** — suma de tokens+costo
- **Por Motor** — stats de cada IDE

### ⚙️ Comandos
Botones de acción:
- Generar/Ejecutar/Cambiar motor
- **Historial** — últimos comandos ejecutados

### 📊 Reportes
Tabla de etapas:
- Nombre etapa
- Tokens usados
- Costo USD
- Número de discusiones
- Estado

---

## 💡 Tips & Tricks

### ✅ Workflow Óptimo
1. **Mañana:** Abrir dashboard, ver status
2. **Generar:** Click "Gen Discusión"
3. **Editar:** IDE (Cursor/Claude/etc)
4. **Revisar:** Tab Discusiones (borrador)
5. **Aprobar:** Mover a final/
6. **Ejecutar:** Plan → Tab Planes ves progreso
7. **Reportar:** Click "Gen Reporte" → Tab Reportes

### 🚀 Auto-Bootstrap
- Dashboard se abre en `http://localhost:5000` automáticamente
- SQLite se crea automáticamente en `claude/reports/reports.db`
- Motor se detecta automáticamente (ve `.motor/motor.json`)

### 📝 Editar Discusiones
```bash
# Abrir en tu IDE preferido
cursor claude/discusiones/borrador/disc_*.md
# o manuamente:
# 1. Abre la carpeta claudemachote en Cursor
# 2. Navega a version3ligera/claude/discusiones/borrador/
# 3. Edita el disc_*.md que quieras
# 4. Cuando esté OK, mueve a final/
```

### 🔄 Actualización Manual
- Dashboard auto-refresca cada 5 segundos
- Si necesitas force-refresh: **F5** en navegador

### 🔌 Cambiar Motor sin UI
Edita `version3ligera/.motor/motor.json`:
```json
{
  "active_motor": "cursor",  ← Cambiar aquí
  "detected_motor": "auto",
  "version": "3.ligera"
}
```

---

## ⚠️ Troubleshooting

| Error | Solución |
|---|---|
| `ModuleNotFoundError: Flask` | `pip install Flask==2.3.0` |
| Dashboard no abre en navegador | Ingresa manual: `http://localhost:5000` |
| Botones no funcionan | Verifica Flask en terminal (muestra errores) |
| SQLite "database is locked" | Cierra otras pestañas/instancias del dashboard |
| `motor.json` no existe | Corre `python motor_detect.py` en terminal |

---

## 📚 Ver Más

- **Documentación completa:** [README_DASHBOARD.md](README_DASHBOARD.md)
- **Estado actual:** [ESTADO.md](ESTADO.md)
- **Implementar handlers:** [IMPLEMENTAR_HANDLERS.md](IMPLEMENTAR_HANDLERS.md)

---

## 🎯 Próxima Etapa (cuando apruebes)

- [ ] Botones generan/ejecutan realmente
- [ ] Tokens se registran automáticamente
- [ ] Reportes con gráficos
- [ ] Export a Excel
- [ ] Webhook para notificaciones

---

**¿Dudas?** — Consulta [README_DASHBOARD.md](README_DASHBOARD.md) o [ESTADO.md](ESTADO.md)

**¿Listo?** — Abre terminal y corre:
```bash
cd version3ligera/claude && python iniciar_dashboard.py
```
