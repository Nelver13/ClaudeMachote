# 🚀 **Manual de Uso — Plantilla Virgen Version3Ligera**

## 📋 **Resumen Ejecutivo**

Esta plantilla implementa un **sistema de gestión de proyectos con IA** que minimiza el consumo de tokens mediante automatización inteligente. Incluye dashboard web, logging automático de tokens, base de datos SQLite y scripts de automatización.

**Tiempo de setup:** 5 minutos  
**Dependencias:** Python 3.8+, Flask, SQLite  
**Compatibilidad:** Windows, macOS, Linux

---

## 🎯 **Paso 1: Copiar Plantilla**

### Opción A: Copia Simple
```bash
# Desde el directorio donde tienes la plantilla
cp -r plantillavirgen/ mi_nuevo_proyecto/
cd mi_nuevo_proyecto/
```

### Opción B: Desde Git (si está versionado)
```bash
git clone [url-del-repo] mi_nuevo_proyecto
cd mi_nuevo_proyecto
# Copiar solo la carpeta plantillavirgen
cp -r plantillavirgen/* ./
```

---

## 🔧 **Paso 2: Instalar Dependencias**

### Instalar Python (si no tienes)
- **Windows:** Descarga de [python.org](https://python.org)
- **macOS:** `brew install python`
- **Linux:** `sudo apt install python3`

### Instalar Flask
```bash
pip install flask
```

**Verificar instalación:**
```bash
python -c "import flask; print('✅ Flask OK')"
```

---

## 🗄️ **Paso 3: Inicializar Base de Datos**

Ejecuta **una sola vez** para crear las tablas SQLite:

```bash
python claude/acciones/init_db.py
```

**Qué hace:**
- ✅ Crea `claude/reports/reports.db`
- ✅ Genera 5 tablas: `token_events`, `etapas`, `reportes`, `comandos`, `motor_stats`
- ✅ Configura índices para rendimiento óptimo

**Salida esperada:**
```
✅ Base de datos inicializada
📊 Tablas creadas: 5
```

---

## 🤖 **Paso 4: Detectar Motor de IA**

Ejecuta para configurar el entorno de IA:

```bash
python claude/acciones/motor_detect.py
```

**Qué detecta:**
- ✅ VS Code + GitHub Copilot
- ✅ VS Code + Claude
- ✅ Cursor IDE
- ✅ Otros motores

**Crea:**
- ✅ Directorio `.motor/`
- ✅ Archivo `motor.json` con configuración

---

## 📊 **Paso 5: Iniciar Dashboard**

### Opción A: Script Automático (Recomendado)
```bash
python claude/acciones/iniciar_dashboard.py
```

### Opción B: Manual
```bash
cd claude/dashboard
python app.py
```

**Resultado:**
- 🌐 Servidor web en `http://localhost:5000`
- 📱 Navegador se abre automáticamente
- 🎛️ Dashboard con 6 pestañas funcionales

---

## 🎮 **Paso 6: Usar el Sistema**

### **Interfaz Web (Dashboard)**
Abre `http://localhost:5000` y verás:

1. **📊 Status** - Estado general del proyecto
2. **💬 Discusiones** - Documentos de análisis
3. **📋 Planes** - Checklists de tareas
4. **💰 Tokens** - Costos y métricas
5. **⚡ Comandos** - Ejecutor automático
6. **📈 Reportes** - Estadísticas por etapas

### **Comandos Disponibles**
Desde el dashboard, puedes ejecutar:

- `gen_discusión` - Crear nueva discusión
- `ejecutar_plan` - Procesar tareas pendientes
- `cambiar_motor` - Cambiar IA activa
- `gen_reporte` - Crear reporte de etapa
- `sync_tokens` - Sincronizar métricas

### **Flujo de Trabajo Típico**

```
1. Crear discusión → gen_discusión
2. Desarrollar plan → Dashboard web
3. Ejecutar tareas → ejecutar_plan
4. Monitorear progreso → Dashboard
5. Generar reporte → gen_reporte
```

---

## 📁 **Estructura de Archivos**

```
mi_proyecto/
├── .motor/                    # Configuración de IA
│   └── motor.json
├── claude/                    # Sistema de gestión
│   ├── acciones/              # Scripts automatizados
│   │   ├── init_db.py        # Inicializar DB
│   │   ├── motor_detect.py   # Detectar IA
│   │   ├── log_tokens.py     # Logging automático
│   │   ├── iniciar_dashboard.py # Launcher
│   │   └── finalizar_etapa.py # Extractor de métricas
│   ├── dashboard/            # Interfaz web
│   │   ├── app.py           # Servidor Flask
│   │   └── templates/       # HTML
│   ├── logs/                # Registros JSON
│   ├── reports/             # Base de datos SQLite
│   ├── discusiones/         # Documentos de análisis
│   │   ├── borrador/        # Trabajos en progreso
│   │   └── final/           # Aprobados
│   └── planes/              # Checklists ejecutables
```

---

## 🔍 **Verificación de Funcionamiento**

### Test 1: Base de Datos
```bash
# Verificar que existe
ls -la claude/reports/reports.db

# Verificar tablas
python -c "
import sqlite3
conn = sqlite3.connect('claude/reports/reports.db')
cursor = conn.cursor()
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")
print('Tablas:', [row[0] for row in cursor.fetchall()])
conn.close()
"
```

### Test 2: Dashboard
```bash
# Verificar que responde
curl http://localhost:5000/api/status
```

### Test 3: Logging
```bash
# Verificar que registra
python -c "
from claude.acciones import log_tokens
log_tokens.log_token_event('test', 'prueba', 10, 20, 'copilot', 'test')
print('✅ Logging funciona')
"
```

---

## 🛠️ **Solución de Problemas**

### **Error: "Flask no instalado"**
```bash
pip install flask
```

### **Error: "Base de datos no existe"**
```bash
python claude/acciones/init_db.py
```

### **Error: "Puerto 5000 ocupado"**
```bash
# Cambiar puerto en app.py
# Línea: app.run(debug=True, port=5000)
# Cambiar a: app.run(debug=True, port=5001)
```

### **Error: "Motor no detectado"**
```bash
# Verificar que estás en VS Code
python claude/acciones/motor_detect.py
```

### **Dashboard no carga**
```bash
# Verificar archivos
ls -la claude/dashboard/
# Reiniciar
python claude/acciones/iniciar_dashboard.py
```

---

## 📈 **Métricas y Costos**

### **Tokens Ahorrados**
- **Sin análisis manual:** Scripts extraen métricas automáticamente
- **Base de datos persistente:** Conocimiento reutilizable
- **Dashboard visual:** Monitoreo sin consultas externas

### **Costos Típicos**
- **Setup inicial:** ~$0.01 (detección + DB)
- **Por discusión:** $0.05-0.20
- **Por plan:** $0.03-0.10
- **Dashboard:** $0.00 (local)

---

## 🎯 **Próximos Pasos**

1. **Personalizar** - Edita `claude/dashboard/templates/index.html`
2. **Integrar** - Conecta con tus workflows existentes
3. **Extender** - Agrega nuevos comandos en `app.py`
4. **Monitorear** - Revisa métricas en el dashboard

---

## 📞 **Soporte**

Si algo no funciona:
1. Verifica los logs en `claude/logs/`
2. Revisa la consola del dashboard
3. Ejecuta tests de verificación arriba

**El sistema está diseñado para ser robusto y auto-diagnosticar problemas.**

---

*🚀 ¡Listo para revolucionar tu workflow con IA!* 🎉</content>
<parameter name="filePath">f:\GitHub\ClaudeMachote\version3ligera\plantillavirgen\README.md