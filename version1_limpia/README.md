# Claude Machote v1.0 — Visión-First Development System

## 🎯 Sistema de Desarrollo Visión-First

Este es un sistema completo para desarrollo de software con **enfoque visión-first**, donde la definición estratégica del proyecto precede a cualquier desarrollo técnico.

### ✨ Características principales

- **Visión Obligatoria:** Todo proyecto inicia con VISION.md que define soluciones y módulos
- **Detección Inteligente:** Cada módulo se desarrolla automáticamente en su solución tecnológica correcta
- **Flujo Automatizado:** Discusiones → Planes → Checklists con actualización automática
- **Multi-Solución:** Soporte para API Backend, Web Frontend, Mobile y Desktop
- **Control Arquitecto:** Modifica planes antes de aprobar, mantiene control total

### 🏗️ Stack Tecnológico

| Solución | Plataforma | Stack | Propósito |
|---|---|---|---|
| **S1** | Django + DRF | Python + PostgreSQL + JWT | API Backend central |
| **S2** | React + Vite | JavaScript/TypeScript | Frontend Web |
| **S3** | React Native + Expo | JavaScript | App Móvil |
| **S4** | WinForms | C# o VB.NET | App Desktop |

### 🚀 Inicio Rápido

Ver `QUICKSTART.md` para instrucciones detalladas.

### 📁 Estructura

```
version1_limpia/
├── CLAUDE.md              # Documentación completa del sistema
├── STACK.md               # Definición tecnológica
├── QUICKSTART.md          # Guía de inicio rápido
├── .gitignore            # Archivos ignorados por git
└── claude/               # Sistema de gestión
    ├── RESUMEN.md        # Estado actual del proyecto
    ├── estado.log        # Log granular de actividades
    ├── acciones/         # Scripts automatizados
    └── discusiones/      # Plantillas y discusiones
```

### 🔄 Flujo de Trabajo

1. **Definir Visión** → `crear_discusion.py "definir-vision" definicion_vision`
2. **Aprobar** → `procesar_aprobacion.py` → Genera VISION.md automáticamente
3. **Desarrollar** → `crear_discusion.py "modulo" creacion` → Detecta solución automáticamente
4. **Ejecutar** → Planes y checklists se actualizan automáticamente

### 📢 Notificaciones

- **Discord Webhook:** Configurado para avisos automáticos
- **Sonidos locales:** Tres tipos de notificación (suave, normal, urgente)
- **Windows Toast:** Notificaciones del sistema

### 🎨 Modo Virgen

Esta versión está completamente limpia y lista para replicar en cualquier proyecto nuevo. Solo contiene lo esencial que funciona.

---

**Desarrollado para optimizar el flujo de trabajo con IAs en desarrollo fullstack multi-plataforma.**