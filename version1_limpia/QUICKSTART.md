# 🚀 QUICKSTART — Claude Machote v1.0 (Visión-First)

## Inicio rápido

### 1. Definir la visión del proyecto (OBLIGATORIO)
```bash
python claude/acciones/crear_discusion.py "definir-vision-proyecto" definicion_vision
```

- Edita la discusión creada
- Define soluciones (S1-S4) y módulos
- Cambia `Estado: En discusión` → `Estado: Aprobado`
- Ejecuta: `python claude/acciones/procesar_aprobacion.py "disc_definir-vision-proyecto.md"`

### 2. Desarrollar módulos
```bash
python claude/acciones/crear_discusion.py "nombre-modulo" creacion
```

- Sistema detecta automáticamente la solución correcta
- Edita y aprueba la discusión
- Sistema genera plan automáticamente

## Stack tecnológico
- **S1 API:** Django + DRF + PostgreSQL + JWT
- **S2 Web:** React + Vite + TypeScript
- **S3 Mobile:** React Native + Expo
- **S4 Desktop:** WinForms + C#

## Estructura
```
version1_limpia/
├── CLAUDE.md              # Documentación principal
├── STACK.md               # Definición de tecnologías
├── .gitignore            # Archivos ignorados
└── claude/
    ├── RESUMEN.md        # Estado del proyecto
    ├── estado.log        # Estado granular
    ├── acciones/         # Scripts automatizados
    │   ├── crear_discusion.py
    │   ├── procesar_aprobacion.py
    │   ├── generar_vision.py
    │   ├── crear_plan.py
    │   ├── actualizar_checklist.py
    │   ├── avisar.py
    │   ├── notificar.py
    │   ├── credenciales.md
    │   └── README.md
    └── discusiones/
        └── TEMPLATE_DISCUSION.md
```

## Notificaciones
- **Discord:** Configurado en `credenciales.md`
- **Sonidos:** `aviso_*.mp3` incluidos
- **Windows:** Notificaciones toast

¡Listo para replicar en cualquier proyecto!