# Modo IA - Claude Code Workflow

## 🚀 Flujo Integrado: Discusión → Plan → Checklist Vivo

### 1. **Discusión Inteligente**
- Claude detecta módulos automáticamente (django-drf, react-vite, etc.)
- Genera plan completo **editable** dentro de la discusión misma
- Arquitecto modifica el plan antes de aprobar

### 2. **Plan Editable en Discusión**
- Sección "## Plan de ejecución (editable)" con checkboxes
- Área de modificaciones para el arquitecto
- Checklist de aprobación integrada

### 3. **Checklist Vivo**
- Se extrae automáticamente de la discusión aprobada
- Se actualiza automáticamente durante ejecución
- Memoria registra cada cambio para continuidad

### 4. **Ejecución con Memoria**
- IA marca tareas completadas automáticamente
- Avisos en cada actualización
- Arquitecto mantiene control total

### 5. **Cierre con Memoria**
- Backup automático de estado
- Memoria actualizada para próximos ciclos
- Arquitecto decide próximos pasos

## 📁 Estructura

```
modo_ia/
├── CLAUDE.md          # Instrucciones principales
├── STACK.md           # Tecnologías soportadas
├── VISION.md          # Visión multi-solución
├── MAPA.md            # Mapa del proyecto
├── setup.py           # Instalación
├── claude/            # Carpeta de memoria y scripts
│   ├── acciones/      # Scripts de automatización
│   ├── discusiones/   # Discusiones activas
│   ├── planes/        # Planes ejecutables
│   ├── backups/       # Backups automáticos
│   ├── imagenes/      # Referencias visuales
│   ├── logs/          # Logs de ejecución
│   └── memoria/       # Memoria del sistema
└── motores/           # Motores especializados
    ├── antigravity/   # Motor Python
    ├── claude/        # Motor Claude
    ├── copilot/       # Motor Copilot
    └── cursor/        # Motor Cursor
```

## 🛠️ Instalación

```bash
python setup.py install
```

## 🎯 Inicio Rápido

1. **Crear discusión inteligente:**
   ```bash
   python claude/acciones/crear_discusion.py "Mi nueva idea"
   ```

2. **Modificar plan en la discusión** (arquitecto)

3. **Aprobar con `0`** → genera checklist automático

4. **Ejecutar checklist** → actualizaciones automáticas

## 📋 Scripts Disponibles

- `crear_discusion.py` - Crea discusión con plan automático
- `crear_plan.py` - Extrae plan de discusión aprobada
- `actualizar_checklist.py` - Actualiza checklist durante ejecución
- `avisar.py` - Sistema de notificaciones
- `backup_n8n.py` - Backup de flujos n8n
- `backup_sql.py` - Backup de base de datos

## 🔧 Tecnologías

- **Backend:** Django + DRF + PostgreSQL + JWT
- **Frontend:** React + Vite
- **Mobile:** React Native + Expo / Flutter
- **Desktop:** WinForms (VB o C#)
- **Automatización:** n8n
- **API:** RESTful, versionada `/api/v1/`
- **Auth:** JWT siempre

## 📞 Contacto

Sistema diseñado para optimizar el flujo de trabajo entre arquitecto e IA, manteniendo el control humano total mientras aprovecha la eficiencia de la automatización.