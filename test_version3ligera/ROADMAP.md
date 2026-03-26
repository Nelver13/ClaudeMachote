# 🚀 ROADMAP — Version3Ligera

> **Guía Rápida para Motores AI** — Lee esto PRIMERO para usar eficientemente el sistema

---

## 📖 DOCUMENTACIÓN ESENCIAL

**ANTES DE EMPEZAR:** Lee completamente estos archivos en orden:
1. **[ROADMAP.md](ROADMAP.md)** ← Este archivo (flujo completo)
2. **[.instructions.md](.instructions.md)** ← Reglas para motores AI
3. **[.prompt.md](.prompt.md)** ← Prompt personalizado para IA
4. **[.agent.md](.agent.md)** ← Configuración específica de agente

## 🎯 PROPÓSITO DEL SISTEMA

Version3Ligera es un **framework de desarrollo asistido por IA** que automatiza el ciclo completo de desarrollo de software. El sistema está diseñado para **minimizar el gasto de tokens** mediante:

- **Automatización inteligente** de tareas repetitivas
- **Base de datos SQLite** para persistir conocimiento
- **Scripts especializados** para cada etapa
- **Dashboard web** para monitoreo en tiempo real

---

## 🧭 FLUJO DE TRABAJO PRINCIPAL

### 1. **INICIO DEL PROYECTO** (1 sola vez)
```bash
# Copiar plantilla
cp -r plantillavirgen/ mi_proyecto/

# Instalar dependencias
pip install -r claude/dashboard/requirements.txt

# Inicializar base de datos
python claude/acciones/init_db.py

# Iniciar dashboard
python claude/acciones/iniciar_dashboard.py
```

### 2. **CICLO DE DESARROLLO** (por cada feature/etapa)

#### **FASE DE ANÁLISIS** 📋
1. **Crear Discusión** → `discusiones/borrador/disc_[tema].md`
   - Analizar requerimiento
   - Definir alcance
   - Identificar riesgos

2. **Aprobar Discusión** → Mover a `discusiones/final/`
   - Cambiar `Estado: Aprobado`
   - El sistema detecta automáticamente

#### **FASE DE EJECUCIÓN** ⚙️
3. **Generar Plan** → `planes/plan_[numero].md`
   - Checklist detallado
   - Tareas específicas
   - Criterios de aceptación

4. **Ejecutar Plan** → Marcar `[x]` cada tarea completada
   - El sistema actualiza automáticamente el progreso
   - Dashboard muestra métricas en tiempo real

#### **FASE DE CIERRE** ✅
5. **Finalizar Etapa** → Ejecutar automáticamente
   ```bash
   python claude/acciones/finalizar_etapa.py
   ```
   - Extrae métricas automáticamente
   - Registra en base de datos
   - Calcula costos y tiempos

---

## 📁 ESTRUCTURA DEL PROYECTO

```
mi_proyecto/
├── claude/                    # Sistema de automatización
│   ├── acciones/             # Scripts ejecutables
│   │   ├── init_db.py        # Inicializar SQLite
│   │   ├── log_tokens.py     # Registrar uso de tokens
│   │   ├── motor_detect.py   # Detectar IDE/motor
│   │   ├── finalizar_etapa.py # Extraer métricas
│   │   └── iniciar_dashboard.py # Iniciar web UI
│   ├── dashboard/            # Interfaz web
│   │   ├── app.py           # Servidor Flask
│   │   └── templates/index.html # Dashboard
│   ├── discusiones/          # Documentación
│   │   ├── borrador/        # En edición
│   │   └── final/           # Aprobadas
│   ├── planes/              # Checklists de ejecución
│   ├── reports/             # Base de datos SQLite
│   └── logs/                # JSON de tokens/costos
└── .motor                    # Configuración del motor actual
```

---

## ⚡ REGLAS PARA MINIMIZAR TOKENS

### ❌ **NO HACER** (gasta tokens innecesariamente)
- Analizar código que ya existe → usar `grep_search` o `semantic_search`
- Leer archivos completos → usar `read_file` con rangos específicos
- Repetir explicaciones → referenciar archivos existentes
- Preguntar por estructura → leer este ROADMAP.md
- Debuggear manualmente → usar herramientas automatizadas

### ✅ **SÍ HACER** (optimiza el uso)
- **Usar herramientas especializadas** para cada tarea
- **Leer ROADMAP.md** antes de cualquier acción
- **Ejecutar scripts** en lugar de código manual
- **Consultar base de datos** para información histórica
- **Usar dashboard** para métricas en tiempo real

---

## 🛠️ HERRAMIENTAS Y SCRIPTS DISPONIBLES

### **Scripts de Automatización** (ejecutar directamente)
```bash
# Base de datos
python claude/acciones/init_db.py          # Crear tablas SQLite

# Tokens y costos
python claude/acciones/log_tokens.py       # Registrar evento de tokens

# Detección
python claude/acciones/motor_detect.py     # Detectar IDE/motor actual

# Finalización
python claude/acciones/finalizar_etapa.py  # Extraer métricas automáticamente

# Dashboard
python claude/acciones/iniciar_dashboard.py # Iniciar interfaz web
```

### **API Endpoints** (desde dashboard)
- `GET /api/status` → Estado general del sistema
- `GET /api/tokens/etapas` → Costos por etapa
- `GET /api/tokens/motores` → Estadísticas por motor
- `POST /api/etapas/crear` → Nueva etapa
- `POST /api/etapas/{id}/finalizar` → Cerrar etapa

---

## 📊 DASHBOARD WEB

**URL:** `http://localhost:5000`

### **Pestañas Disponibles:**
- **📊 Home** → Métricas generales, motor activo, progreso
- **📄 Discusiones** → Lista de borradores y finales
- **📋 Planes** → Progreso de planes activos
- **💰 Tokens** → Costos por etapa y motor
- **⚙️ Comandos** → Ejecutar acciones del sistema
- **📊 Reportes** → Estadísticas históricas

### **Auto-refresh:** Cada 5 segundos
- No requiere recargar manualmente
- Muestra cambios en tiempo real

---

## 🔄 CICLO DE RETROALIMENTACIÓN

### **Para cada tarea/feature:**

1. **DISCUSIÓN** → Crear `disc_[tema].md` en borrador
2. **APROBACIÓN** → Mover a final cuando esté listo
3. **PLAN** → Generar checklist detallado
4. **EJECUCIÓN** → Marcar `[x]` cada tarea completada
5. **CIERRE** → Script extrae métricas automáticamente

### **Archivos que se generan automáticamente:**
- `claude/logs/tokens.json` → Historial de uso
- `claude/reports/reports.db` → Base de datos SQLite
- `claude/planes/plan_XXX.md` → Checklists
- `.motor/motor.json` → Configuración detectada

---

## 🎯 DECISIONES DE DISEÑO

### **Por qué esta arquitectura:**
- **SQLite** → Persistencia sin configuración externa
- **Flask** → Servidor web simple y rápido
- **JSON logs** → Historial legible y versionable
- **Scripts especializados** → Automatización de tareas repetitivas
- **Dashboard web** → Interfaz visual para monitoreo

### **Separación de responsabilidades:**
- **acciones/** → Scripts ejecutables (automatización)
- **dashboard/** → Interfaz web (visualización)
- **discusiones/** → Documentación (análisis)
- **planes/** → Checklists (ejecución)
- **reports/** → Datos persistentes (historial)

---

## 🚨 ERRORES COMUNES A EVITAR

### **No ejecutar scripts manualmente**
```python
# ❌ MAL - Gasta tokens recreando lógica
import sqlite3
# ... 50 líneas de código SQL manual

# ✅ BIEN - Usar script existente
subprocess.run(['python', 'claude/acciones/init_db.py'])
```

### **No leer archivos completos sin necesidad**
```python
# ❌ MAL - Lee todo el archivo
content = read_file('archivo.py', 1, 1000)

# ✅ BIEN - Buscar específicamente
grep_search(query='class MiClase', includePattern='*.py')
```

### **No repetir análisis ya hechos**
```python
# ❌ MAL - Reanalizar estructura cada vez
print("Analizando estructura del proyecto...")
# ... análisis completo

# ✅ BIEN - Referenciar ROADMAP.md
print("Ver ROADMAP.md para estructura del proyecto")
```

---

## 📈 MÉTRICAS Y OPTIMIZACIÓN

### **Tokens por etapa** (promedio esperado)
- **Discusión:** 200-500 tokens
- **Plan:** 100-300 tokens
- **Ejecución:** 50-150 tokens por tarea
- **Total por feature:** 500-2000 tokens

### **Tiempo estimado**
- **Setup inicial:** 5 minutos
- **Discusión:** 10-15 minutos
- **Plan + ejecución:** 30-60 minutos
- **Cierre automático:** 2-5 segundos

---

## 🔧 CONFIGURACIÓN AVANZADA

### **Personalizar costos de tokens**
Editar `claude/acciones/log_tokens.py`:
```python
precios = {
    'claude': {'input': 0.0005, 'output': 0.0015},
    'copilot': {'input': 0, 'output': 0},
    # ... agregar más motores
}
```

### **Modificar dashboard**
Editar `claude/dashboard/templates/index.html` para nueva UI.

### **Agregar scripts personalizados**
Crear en `claude/acciones/` siguiendo el patrón existente.

---

## 🎯 CHECKLIST PARA NUEVOS PROYECTOS

- [ ] Copiar plantilla a nueva ubicación
- [ ] Instalar dependencias con pip
- [ ] Ejecutar `init_db.py` para crear base de datos
- [ ] Verificar que `.motor` existe
- [ ] Iniciar dashboard y verificar funcionamiento
- [ ] Leer ROADMAP.md completamente antes de empezar
- [ ] Usar scripts automatizados en lugar de código manual

---

**🚀 RECUERDA:** Este sistema está diseñado para **maximizar eficiencia** y **minimizar costos**. Lee este ROADMAP.md **ANTES** de cualquier acción, y **USA LOS SCRIPTS** disponibles en lugar de recrear lógica.