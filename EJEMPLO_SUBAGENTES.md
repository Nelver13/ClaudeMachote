# 💡 EJEMPLO REAL: Cómo Claude Ejecuta Subagentes

## 🎬 ESCENARIO: Arquitecto quiere "Sistema de Blog con Comentarios"

### **PASO 1: Arquitecto da la idea**
```bash
# Arquitecto abre Claude Code y escribe:
"Crear un sistema de blog con posts, comentarios y usuarios autenticados"
```

### **PASO 2: Claude ejecuta subagente de análisis (automático)**
```bash
# Claude detecta automáticamente el motor y ejecuta:
runSubagent("Explore", "Analizar workspace y detectar stack para blog system")
```

**Output del subagente:**
```
📊 ANÁLISIS COMPLETADO:
- Stack detectado: Django + DRF + React + Vite
- Archivos existentes: manage.py, package.json
- Dependencias: Django 4.2, DRF 3.14, React 18
- Patrón sugerido: API-first con JWT auth
```

### **PASO 3: Claude crea discusión inteligente**
```bash
# Script automático genera discusión
python claude/acciones/crear_discusion.py "sistema-blog" creacion
```

**Resultado:**
```
📝 CREADO: claude/discusiones/creaciones/disc_sistema-blog.md

## Análisis automático
Stack detectado: django-drf + react-vite
Complejidad estimada: Media (4-6 horas)
Archivos afectados: ~15

## Plan de ejecución (editable)
- [ ] Crear modelos Post y Comment
- [ ] API REST para posts/comentarios
- [ ] Autenticación JWT
- [ ] Frontend React con editor de posts
- [ ] Sistema de comentarios en tiempo real
- [ ] Dashboard de administración

## Modificaciones del arquitecto
_(Aquí puedes agregar, quitar o modificar tareas)_

## Checklist de aprobación
- [ ] Plan revisado y aprobado
- [ ] Todas las tareas claras
- [ ] Prioridades correctas
```

### **PASO 4: Arquitecto modifica y aprueba**
```bash
# Arquitecto lee el archivo y modifica:
# Agrega: "- [ ] Moderación de comentarios"
# Aprueba: marca checklist y dice "0"
```

### **PASO 5: Claude extrae plan y comienza ejecución**
```bash
# Claude ejecuta:
python claude/acciones/crear_plan.py disc_sistema-blog.md

# Resultado: claude/planes/plan_002.md creado
# Notificación: "plan_002.md listo — empezando ejecución"
```

### **PASO 6: EJECUCIÓN - Claude orquesta subagentes especializados**

#### **Subagente 1: Model Design**
```bash
# Claude ejecuta subagente específico para modelos
runSubagent("Database Design", "Crear modelos Post y Comment con relaciones para blog")
```

**Código generado automáticamente:**
```python
# blog/models.py
class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    moderado = models.BooleanField(default=False)
```

```bash
# Checklist actualizado automáticamente
python actualizar_checklist.py "claude/planes/plan_002.md" "Crear modelos Post y Comment"
# Resultado: [x] Crear modelos Post y Comment (33% completado)
```

#### **Subagente 2: API Generation**
```bash
# Claude ejecuta subagente para APIs
runSubagent("API Design", "Generar DRF API completa para blog con JWT y permisos")
```

**Archivos generados:**
- `blog/serializers.py` - PostSerializer, CommentSerializer
- `blog/views.py` - PostViewSet, CommentViewSet
- `blog/permissions.py` - IsAuthorOrReadOnly, IsModerator
- `core/urls.py` - Inclusión de rutas de blog

```bash
# Actualización en tiempo real
python actualizar_checklist.py "claude/planes/plan_002.md" "API REST para posts/comentarios"
# Resultado: [x] API REST para posts/comentarios (67% completado)
```

#### **Subagente 3: React Components**
```bash
# Claude ejecuta subagente para frontend
runSubagent("React Components", "Crear interfaz completa de blog con posts, comentarios y auth")
```

**Componentes generados:**
- `frontend/src/pages/Blog.jsx` - Lista de posts
- `frontend/src/pages/PostDetail.jsx` - Vista individual con comentarios
- `frontend/src/components/PostEditor.jsx` - Crear/editar posts
- `frontend/src/components/CommentForm.jsx` - Sistema de comentarios
- `frontend/src/context/AuthContext.jsx` - Gestión de autenticación

```bash
# Progreso actualizado
python actualizar_checklist.py "claude/planes/plan_002.md" "Frontend React con editor de posts"
# Resultado: [x] Frontend React con editor de posts (83% completado)
```

#### **Subagente 4: Real-time Features**
```bash
# Claude ejecuta subagente para funcionalidades avanzadas
runSubagent("Real-time Integration", "Implementar comentarios en tiempo real y moderación")
```

**Funcionalidades agregadas:**
- WebSocket para comentarios en vivo
- Sistema de moderación de comentarios
- Notificaciones en tiempo real
- Dashboard administrativo

```bash
# Tarea final completada
python actualizar_checklist.py "claude/planes/plan_002.md" "Sistema de comentarios en tiempo real"
python actualizar_checklist.py "claude/planes/plan_002.md" "Dashboard de administración"
python actualizar_checklist.py "claude/planes/plan_002.md" "Moderación de comentarios"
# Resultado: [x] Todas las tareas completadas (100%)
```

### **PASO 7: CIERRE - Subagentes de finalización**
```bash
# Subagente de testing
runSubagent("Testing", "Ejecutar suite completa de tests para blog system")

# Subagente de documentación
runSubagent("Documentation", "Generar docs de API y guía de usuario")

# Scripts de cierre
python claude/acciones/finalizar_etapa.py "Sistema de Blog"
python claude/acciones/backup_sql.py 2
python claude/acciones/avisar.py "Etapa completada - Blog System" normal
```

## 🎯 LO QUE VE EL ARQUITECTO

### **Notificaciones en tiempo real:**
```
🔔 "disc_sistema-blog.md listo — marca 1"
🔔 "plan_002.md listo — empezando ejecución"
🔔 "Crear modelos Post y Comment — 1/6 completado"
🔔 "API REST generada — 2/6 completado"
🔔 "Frontend React creado — 3/6 completado"
🔔 "Comentarios en tiempo real — 4/6 completado"
🔔 "Dashboard admin listo — 5/6 completado"
🔔 "Moderación implementada — 6/6 completado"
🔔 "Etapa completada - Sistema de Blog"
```

### **Dashboard visual:**
```
📊 PROYECTO: Sistema de Blog
├── ✅ Modelos creados (Django)
├── ✅ API REST completa (DRF + JWT)
├── ✅ Frontend funcional (React)
├── ✅ Tiempo real (WebSocket)
├── ✅ Moderación (Admin)
└── 📈 Métricas: 100% completado, 0 errores
```

### **Checklist vivo:**
```markdown
# Plan #002 — Sistema de Blog
**Estado:** Completado
**Progreso:** 100%

## Tareas
- [x] Crear modelos Post y Comment
- [x] API REST para posts/comentarios
- [x] Autenticación JWT
- [x] Frontend React con editor de posts
- [x] Sistema de comentarios en tiempo real
- [x] Dashboard de administración
- [x] Moderación de comentarios (agregado por arquitecto)

## Memoria de continuidad
- **Última tarea:** Moderación de comentarios (2026-03-26 16:30)
- **Tiempo total:** 2.5 horas
- **Calidad:** Alta (tests pasaron)
- **Arquitecto:** Aprobado para producción
```

---

## 🔑 PUNTOS CLAVE DEL FLUJO

1. **Subagentes especializados** ejecutan tareas específicas
2. **Contexto compartido** mantiene consistencia
3. **Validación automática** en cada paso
4. **Memoria viva** registra todo el progreso
5. **Control humano** en decisiones importantes
6. **Recuperación automática** de errores

*El resultado es un sistema completo generado automáticamente, pero con el control creativo del arquitecto en cada decisión importante.*