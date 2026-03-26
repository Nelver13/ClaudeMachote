# Version3Ligera — Plantilla Virgen

Esta es la plantilla mínima para iniciar un nuevo proyecto con Version3Ligera.

## � LECTURA OBLIGATORIA

> **⚠️ IMPORTANTE:** Antes de usar el sistema, lee completamente **[ROADMAP.md](ROADMAP.md)** — contiene las reglas para usar eficientemente el sistema y evitar gasto innecesario de tokens.

## 🚀 Inicio Rápido

1. **Leer ROADMAP.md** completamente (5 minutos)
2. **Copiar plantilla**: Copia esta carpeta completa a tu nuevo proyecto
3. **Instalar dependencias**: `pip install -r claude/dashboard/requirements.txt`
4. **Inicializar base de datos**: `python claude/acciones/init_db.py`
5. **Iniciar dashboard**: `python claude/acciones/iniciar_dashboard.py`

## 📁 Estructura

```
claude/
├── acciones/           # Scripts de automatización
│   ├── init_db.py      # Inicializa SQLite
│   ├── log_tokens.py   # Tracking de tokens
│   ├── motor_detect.py # Detección de IDE/motor
│   └── finalizar_etapa.py # Extracción automática
├── dashboard/          # Dashboard web
│   ├── app.py          # Flask application
│   ├── requirements.txt
│   └── templates/
│       └── index.html  # Dashboard UI
├── discusiones/        # Discusiones (borrador/final)
├── planes/            # Planes de ejecución
├── reports/           # Reportes generados
└── logs/              # Logs del sistema
```

## 🔧 Funcionalidades

- **Dashboard web** con métricas en tiempo real
- **Tracking automático** de tokens y costos
- **Detección automática** de motor AI (Claude/Cursor/Copilot)
- **Gestión de etapas** con extracción automática de información
- **Base de datos SQLite** para persistencia

## 📊 API Endpoints

- `GET /api/status` — Estado general del sistema
- `GET /api/tokens/etapas` — Tokens por etapa
- `GET /api/tokens/motores` — Estadísticas por motor
- `POST /api/comandos/ejecutar` — Ejecutar comandos
- `POST /api/etapas/crear` — Crear nueva etapa
- `POST /api/etapas/{id}/finalizar` — Finalizar etapa

## 🛠️ Desarrollo

Para agregar nuevas funcionalidades:

1. Editar `claude/dashboard/app.py` para nuevos endpoints
2. Agregar scripts en `claude/acciones/`
3. Actualizar `claude/dashboard/templates/index.html` para nueva UI

## 📝 Notas

- Todo el código está en Python 3.8+
- Base de datos SQLite (sin configuración adicional)
- Dashboard se abre automáticamente en el navegador
- Auto-refresh cada 5 segundos