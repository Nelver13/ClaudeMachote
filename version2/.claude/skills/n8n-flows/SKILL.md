# Skill: n8n Flows
name: n8n-flows
description: Patrones para automatizaciones con n8n. Se activa al hablar de flujos, webhooks, automatizaciones, integraciones o docker-compose con n8n.
allowed tools: Read, Grep, Glob, Bash

---

## Convenciones

- Nombres de flujo: `[Contexto] - [Acción]` (ej: `Usuarios - Registro completado`)
- Credenciales: nombradas con servicio + entorno (ej: `Postgres DEV`)
- Webhooks: path descriptivo `/webhook/[contexto]-[accion]`
- Nunca hardcodear valores → usar variables de entorno de n8n
- Backup obligatorio antes de modificar flujos en producción

## Estructura de backup

```
claude/backups/n8n/
└── etapa_XX_YYYY-MM-DD/
    ├── flujo_nombre.json
    └── resumen.md
```

## Acceso

- URL local: `http://localhost:5678`
- Credenciales en: `claude/acciones/credenciales.md`
- Script de backup: `python claude/acciones/backup_n8n.py [N]`

## Patrones frecuentes

### Webhook → Procesar → Notificar
```
Webhook → IF (validar datos) → Set (transformar) → HTTP Request (API) → Respond
```

### Trigger periódico → DB → Acción
```
Schedule → Postgres (leer) → IF (condición) → [acción] → Postgres (actualizar estado)
```

### Error handling
```
Nodo principal → [Error Output] → Set (formatear error) → avisar.py urgente
```

## Antes de modificar un flujo

1. Hacer backup: `python claude/acciones/backup_n8n.py [etapa]`
2. Verificar credenciales en `credenciales.md`
3. Probar en entorno de desarrollo primero
