# 🚀 ROADMAP: Cómo Claude Ejecuta Subagentes en el Flujo

## 📋 EJEMPLO PRÁCTICO: Sistema de Gestión de Usuarios

### **FASE 1: Arquitecto Inicia Idea**
```
Arquitecto: "Vamos a crear un sistema de gestión de usuarios con Django + React"
```

### **FASE 2: Claude Detecta y Prepara (Subagente: Explore)**
```bash
# Claude ejecuta subagente para analizar el workspace
runSubagent("Explore", "Analizar estructura actual y detectar stack Django+React")
```

**Resultado del subagente:**
- ✅ Detecta: `manage.py` + `vite.config.js` → Stack: Django + React
- ✅ Encuentra: Modelos existentes, estructura de API
- ✅ Identifica: Dependencias faltantes, patrones de código

### **FASE 3: Claude Genera Discusión Inteligente**
```bash
# Claude ejecuta script de automatización
python claude/acciones/crear_discusion.py "sistema-usuarios" creacion
```

**Subagente interno genera:**
- 📝 `disc_sistema-usuarios.md` con plan editable
- 🔍 Detección automática de módulo: `django-drf` + `react-vite`
- 📋 Plan preliminar con checkboxes editables

### **FASE 4: Arquitecto Modifica Plan**
```
Arquitecto lee: claude/discusiones/creaciones/disc_sistema-usuarios.md
Arquitecto modifica sección "## Plan de ejecución (editable)":
- [ ] Crear modelo User personalizado
- [ ] API REST con DRF + JWT
- [ ] Frontend React con login/registro
- [ ] Dashboard de administración
Arquitecto: R:/ "Agregar validación de email único"
```

### **FASE 5: Arquitecto Aprueba → Claude Extrae Plan**
```
Arquitecto: "0" (aprobar)
```

```bash
# Claude ejecuta subagente para extraer y validar plan
runSubagent("Explore", "Extraer plan de disc_sistema-usuarios.md y validar dependencias")
```

**Subagente valida:**
- ✅ Todas las dependencias disponibles
- ✅ Estructura de archivos correcta
- ✅ Compatibilidad de versiones

```bash
# Claude genera checklist ejecutable
python claude/acciones/crear_plan.py disc_sistema-usuarios.md
# Resultado: claude/planes/plan_001.md
```

### **FASE 6: EJECUCIÓN - Claude Ejecuta Subagentes por Tarea**

#### **TAREA 1: Crear Modelo User (Subagente: Code Generation)**
```bash
# Claude ejecuta subagente especializado
runSubagent("Code Generation", "Crear modelo User con campos personalizados para Django")
```

**Subagente genera:**
```python
# usuarios/models.py
class User(AbstractUser):
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES_CHOICES, default='usuario')
```

```bash
# Claude marca tarea completada
python actualizar_checklist.py "claude/planes/plan_001.md" "Crear modelo User personalizado"
# Resultado: [x] Crear modelo User personalizado
```

#### **TAREA 2: API REST con DRF (Subagente: API Design)**
```bash
# Claude ejecuta subagente para diseño de API
runSubagent("API Design", "Generar serializers, views y URLs para User API con JWT")
```

**Subagente genera:**
- `usuarios/serializers.py` - UserSerializer con validaciones
- `usuarios/views.py` - UserViewSet con permisos
- `usuarios/urls.py` - Rutas REST
- `core/settings.py` - Configuración JWT

```bash
# Actualización automática
python actualizar_checklist.py "claude/planes/plan_001.md" "API REST con DRF + JWT"
```

#### **TAREA 3: Frontend React (Subagente: React Components)**
```bash
# Claude ejecuta subagente para componentes React
runSubagent("React Components", "Crear componentes de login, registro y dashboard")
```

**Subagente genera:**
- `frontend/src/components/LoginForm.jsx`
- `frontend/src/components/UserDashboard.jsx`
- `frontend/src/services/api.js` - Cliente API
- `frontend/src/App.jsx` - Rutas y navegación

```bash
# Checklist actualizado
python actualizar_checklist.py "claude/planes/plan_001.md" "Frontend React con login/registro"
```

#### **TAREA 4: Dashboard Admin (Subagente: Admin Interface)**
```bash
# Claude ejecuta subagente para interfaz administrativa
runSubagent("Admin Interface", "Crear dashboard de administración de usuarios")
```

**Subagente genera:**
- `frontend/src/components/admin/UserManagement.jsx`
- `frontend/src/components/admin/UserTable.jsx`
- `frontend/src/hooks/useUsers.js` - Custom hooks

```bash
# Última tarea completada
python actualizar_checklist.py "claude/planes/plan_001.md" "Dashboard de administración"
```

### **FASE 7: CIERRE - Claude Ejecuta Subagentes de Finalización**
```bash
# Subagente de testing
runSubagent("Testing", "Ejecutar tests unitarios y de integración")

# Subagente de documentación
runSubagent("Documentation", "Generar documentación de API y README")

# Scripts de cierre automático
python claude/acciones/finalizar_etapa.py "Sistema de Usuarios"
python claude/acciones/backup_sql.py 1
python claude/acciones/avisar.py "Etapa completada - Sistema de Usuarios" normal
```

## 🎯 PUNTOS CLAVE: Cómo Claude Gestiona Subagentes

### **1. Detección Automática**
```python
# Claude analiza el contexto y elige el subagente apropiado
if task_type == "model_design":
    runSubagent("Database Design", task_description)
elif task_type == "api_creation":
    runSubagent("API Design", task_description)
elif task_type == "frontend_components":
    runSubagent("React Components", task_description)
```

### **2. Contexto Compartido**
- **Input**: Descripción de tarea + contexto del proyecto
- **Output**: Código generado + archivos modificados
- **Memoria**: Checklist actualizado automáticamente

### **3. Validación Continua**
```python
# Después de cada subagente, Claude valida
- Sintaxis correcta ✓
- Tests pasan ✓
- Checklist actualizado ✓
- Arquitecto notificado ✓
```

### **4. Recuperación de Errores**
```python
# Si subagente falla
try:
    result = runSubagent(agent, task)
except Exception as e:
    # Claude intenta alternativa o pide feedback
    runSubagent("Debug", f"Resolver error: {e}")
```

## 🚀 RESULTADO FINAL

**Checklist Vivo:**
```
## Tareas
- [x] Crear modelo User personalizado
- [x] API REST con DRF + JWT
- [x] Frontend React con login/registro
- [x] Dashboard de administración

## Memoria de continuidad
- **Última tarea completada:** Dashboard de administración (2026-03-26 15:45)
- **Próxima tarea:** Ninguna tarea pendiente
- **Estado general:** 100%
- **Problemas encontrados:** 0
```

**Arquitecto recibe:**
- ✅ Notificación: "Etapa completada - Sistema de Usuarios"
- ✅ Dashboard actualizado con métricas
- ✅ Memoria lista para próxima idea

---

*Este roadmap muestra cómo Claude orquesta múltiples subagentes especializados, manteniendo el control humano total mientras optimiza la ejecución automática.*