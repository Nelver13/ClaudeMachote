# STACK.md — Stack Personal del Arquitecto
> Este archivo lo mantenés vos. Actualizarlo cuando cambie el stack.
> La IA lo lee al iniciar cada sesión para cargar los skills correspondientes.

---

## Web Fullstack
- **Backend:** Django + Django REST Framework (DRF)
- **Frontend:** React + Vite
- **Base de datos:** PostgreSQL
- **Autenticación:** JWT (SimpleJWT)
- **API:** RESTful, versionada `/api/v1/`

## Mobile
- **Opción A:** React Native + Expo
- **Opción B:** Flutter
- **Desktop cross-platform:** Electron + React

## Automatizaciones
- **n8n** — flujos, webhooks, agentes de IA

## Deploy
- **Producción:** Docker + docker-compose
- **Pruebas:** docker-compose.test.yml en servidor de prueba

## IDE y motores IA
- **IDE principal:** Visual Studio Code
- **Motor IA principal:** Claude Code CLI
- **Motor alternativo:** Copilot (extensión VS Code)

---

## Convenciones

### Django
- `snake_case` en todo
- Serializers en `serializers.py`, validaciones ahí (no en la vista)
- Modelos con `__str__` siempre definido
- Lógica de negocio en `services.py`

### React
- Componentes en `PascalCase`
- Hooks personalizados en `/hooks/`

### API
- Siempre JWT
- Endpoints RESTful — `/api/v1/`
- Nunca hardcodear secrets

### Git
- El arquitecto administra commits y push
- Variables de entorno: siempre `.env` + `.env.example`
- `claude/` siempre en `.gitignore`

_Última actualización: 2026-03-24_
