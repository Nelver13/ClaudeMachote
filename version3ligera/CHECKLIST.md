# ✅ CHECKLIST — Validar que Version3Ligera Funciona

**Antes de usar en producción, seguí estos pasos.**

---

## 🚀 Pre-Launch (Antes de Iniciar)

- [ ] `version3ligera/` existe
- [ ] Tenés Python 3.8+
- [ ] Pip install OK

```bash
python --version  # >= 3.8
pip install Flask==2.3.0
```

---

## 🎯 Bootstrap

### 1. Carpetas Existen
```bash
cd version3ligera/claude

# Verificar que existen:
ls discusiones/borrador/      # ✅ Existe
ls discusiones/final/         # ✅ Existe
ls planes/                    # ✅ Existe
ls dashboard/                 # ✅ Existe con app.py
ls acciones/                  # ✅ Existe con scripts
ls reports/                   # ✅ Creada automáticamente
ls logs/                      # ✅ Creada automáticamente
```

### 2. Archivos Clave Existen
```bash
# Root
ls -la ../QUICKSTART.md              # ✅
ls -la ../SUMMARY.md                # ✅
ls -la ../README_DASHBOARD.md       # ✅
ls -la ../ESTADO.md                 # ✅
ls -la ../INDEX.md                  # ✅

# Dashboard
ls -la dashboard/app.py              # ✅
ls -la dashboard/templates/index.html # ✅
ls -la dashboard/requirements.txt     # ✅

# Acciones
ls -la acciones/init_db.py           # ✅
ls -la acciones/sync_tokens.py       # ✅
ls -la acciones/log_tokens.py        # ✅
ls -la acciones/gen_report.py        # ✅
ls -la acciones/motor_detect.py      # ✅
ls -la acciones/iniciar_dashboard.py # ✅
```

### 3. Motor Config Existe
```bash
ls -la ../.motor/motor.json  # ✅
cat ../.motor/motor.json     # ✅ Ver contenido
```

---

## 🔧 Iniciar Dashboard

```bash
cd version3ligera/claude
python iniciar_dashboard.py
```

✅ **Esperar que diga:**
```
🚀 Dashboard running on http://localhost:5000
```

---

## 🌐 Validar en Navegador

1. **Abrir** `http://localhost:5000`
   - [ ] Dashboard carga sin errores
   - [ ] 6 tabs visibles (Home, Discusiones, Planes, Tokens, Comandos, Reportes)

2. **Tab Home**
   - [ ] Motor detectado muestra algo
   - [ ] Contador de discusiones = 1 (tenemos disc_ejemplo_01.md)
   - [ ] Contador finales = 1 (tenemos disc_flujo_base.md)
   - [ ] Planes = 1 (tenemos plan_001.md)

3. **Tab Discusiones**
   - [ ] Borradores list muestra "disc_ejemplo_01.md"
   - [ ] Finales list muestra "disc_flujo_base.md"

4. **Tab Planes**
   - [ ] Muestra "plan_001.md" con progress bar
   - [ ] Muestra completadas vs pendientes

5. **Tab Tokens**
   - [ ] "Sin datos" (normal, no hay eventos aún)

6. **Tab Comandos**
   - [ ] 6 botones visibles
   - [ ] Table de historial vacía (OK)

7. **Tab Reportes**
   - [ ] "Sin reportes" (OK, DB vacía)

---

## 🤖 Validar Comandos

En **Tab Comandos**, clickea cada botón y verifica:

### 1️⃣ Gen Discusión
```bash
[ ] Click "📝 Gen Discusión"
[ ] Ves: "✅ disc_YYYYMMDD_HHMMSS.md"
[ ] Verifica: discusiones/borrador/disc_*.md creado
```

### 2️⃣ Ejecutar Plan
```bash
[ ] Click "▶️ Ejecutar Plan"
[ ] Ves: "✅ plan_001.md | XX%"
[ ] Tab Planes ahora muestra el progreso
```

### 3️⃣ Cambiar Motor (en Dropdown)
```bash
[ ] Selecciona "cursor" en dropdown
[ ] .motor/motor.json actualizado:
    cat ../.motor/motor.json | grep active_motor
```

### 4️⃣ Gen Reporte
```bash
[ ] Click "📊 Gen Reporte"
[ ] Ves algo como: "⚠️ Sin reportes aún" (normal)
```

### 5️⃣ Sync Tokens
```bash
[ ] Click "⬇️ Sync Tokens"
[ ] Ves: "✅ Sync completado"
```

---

## 💾 Validar SQLite

```bash
# 1. Ver que reports.db existe
ls -la reports/reports.db  # ✅

# 2. Verificar schema con sqlite3
sqlite3 reports/reports.db ".tables"
# Debe mostrar: comandos  etapas  motor_stats  reportes  token_events

# 3. Ver contenido
sqlite3 reports/reports.db "SELECT * FROM comandos LIMIT 5;"
# Debe mostrar filas de comandos ejecutados
```

---

## 📊 Validar Datos

### A. Verificar que discusiones se crean
```bash
ls -la discusiones/borrador/  # Debe tener disc_*.md
ls -la discusiones/final/     # Debe tener disc_flujo_base.md
```

### B. Verificar que planes existen
```bash
ls -la planes/  # Debe tener plan_001.md y lo que genere gen_discusión
cat planes/plan_001.md  # Muestra contenido
```

### C. Verificar que comandos se registran
```bash
sqlite3 reports/reports.db "SELECT comando, estado, resultado FROM comandos LIMIT 5;"
# Debe mostrar filas: gen_discusión, ejecutar_plan, sync_tokens, etc con estado='éxito'
```

---

## 📈 Auto-Refresh

- [ ] Dashboard actualiza cada 5 segundos
- [ ] Timestamp en footer cambia (formato HH:MM:SS)
- [ ] Contadores se actualizan si creatés archivos mientras está abierto

---

## 🔗 API Endpoints

Testea en curl o Postman:

```bash
# 1. Status
curl http://localhost:5000/api/status | jq .

# 2. Motors
curl http://localhost:5000/api/motors | jq .

# 3. Tokens
curl http://localhost:5000/api/tokens/etapas | jq .

# 4. Motores stats
curl http://localhost:5000/api/tokens/motores | jq .

# 5. Reportes
curl http://localhost:5000/api/reportes/etapas | jq .

# 6. Ejecutar comando (POST)
curl -X POST http://localhost:5000/api/comandos/ejecutar \
  -H "Content-Type: application/json" \
  -d '{"comando": "gen_discusión", "parametros": {}}'
```

✅ Todos deben retornar JSON válido

---

## 🧪 Full Workflow Test

1. **Abrir Dashboard** → `http://localhost:5000`
2. **Gen Discusión** → Click botón en Comandos
3. **Revisar** → Tab Discusiones ve en borrador
4. **Mover a Final** (manual)
   ```bash
   mv discusiones/borrador/disc_*.md discusiones/final/
   ```
5. **Refresh** → Dashboard actualiza automáticamente
6. **Ejecutar Plan** → Click botón
7. **Ver Progreso** → Tab Planes actualiza
8. **Generar Reporte** → Click botón
9. **Ver Reportes** → Tab Reportes (aún vacío, pero no errores)

---

## 📋 Validación Final

| Chequeo | Status |
|---|---|
| ✅ Todos los archivos existen | ☐ |
| ✅ Dashboard carga sin errores | ☐ |
| ✅ 6 tabs funcionan | ☐ |
| ✅ Discusiones se crean | ☐ |
| ✅ Planes se leen | ☐ |
| ✅ Comandos se ejecutan | ☐ |
| ✅ SQLite registra eventos | ☐ |
| ✅ API endpoints responden | ☐ |
| ✅ Auto-refresh funciona | ☐ |
| ✅ Motor switch funciona | ☐ |

---

## 🚨 Si Algo No Funciona

### Error: "Flask not found"
```bash
pip install Flask==2.3.0 Werkzeug==2.3.0
```

### Error: "Port 5000 already in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

### Error: "Module not found"
```bash
cd version3ligera/claude
python -m pip install -r dashboard/requirements.txt
```

### Dashboard no descarga discusiones
- Verifica que `discusiones/borrador/` y `final/` tienen archivos `.md`
- Los nombres deben empezar con `disc_` para que se detecten

### SQLite error
```bash
rm -f reports/reports.db
python acciones/init_db.py
```

---

## ✨ Si Todo Funciona

🎉 **Version3Ligera está lista para usar.**

Próximos pasos:
- [ ] Leer [QUICKSTART.md](../QUICKSTART.md) para workflow
- [ ] Leer [README_DASHBOARD.md](../README_DASHBOARD.md) para referencia
- [ ] Creatálos primeros archivos: `discusiones/`, `planes/`

---

## 📞 Referencia Rápida

| Acción | Comando |
|---|---|
| Iniciar dashboard | `cd version3ligera/claude && python iniciar_dashboard.py` |
| Abrir en navegador | `http://localhost:5000` |
| Ver logs | `tail -f logs/tokens.json` |
| Resetear BD | `rm reports/reports.db && python acciones/init_db.py` |
| Sincronizar tokens | `python acciones/sync_tokens.py` |
| Ver motor config | `cat ../.motor/motor.json` |

---

**Última actualización:** 2025-01-21  
**Versión:** 3.ligera (v1.0)

🚀 **Listo? Comenza en [QUICKSTART.md](../QUICKSTART.md)**
