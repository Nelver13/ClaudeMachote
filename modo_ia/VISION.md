# VISION.md — Definir Vision Proyecto
**Generado:** 2026-03-26
**Última actualización:** 2026-03-26

## Qué hace el sistema
Sistema de gestión de proyectos colaborativo para equipos técnicos Dirigido a desarrolladores, managers técnicos y empresas de software El problema principal es la falta de herramientas integradas que conecten gestión de proyectos con desarrollo de código

## Soluciones previstas
| ID | Solución | Plataforma | Stack | Estado |
|---|---|---|---|---|
| S1 | API Backend | Django + DRF | Python + PostgreSQL | En desarrollo |
| S2 | Web Frontend | React + Vite | JavaScript/TypeScript | Pendiente |
| S3 | Mobile App | React Native + Expo | JavaScript | Pendiente |
| S4 | Desktop App | WinForms | C# o VB.NET | Pendiente |

## Backend compartido
- **API Base:** `/api/v1/`
- **Autenticación:** JWT (SimpleJWT) — válido para todas las plataformas
- **Base de datos:** PostgreSQL
- **Servidor:** Django + Gunicorn (producción)

## Módulos y qué solución los usa
| Módulo | S1 API | S2 Web | S3 Mobile | S4 Desktop | Endpoint |
|---|---|---|---|---|---|
| Autenticación | ✅ | ✅ | ✅ | ✅ | /api/v1/autenticación/ |
| Proyectos | ✅ | ✅ | 🔄 | ❌ | /api/v1/proyectos/ |
| Tareas | ✅ | ✅ | ✅ | 🔄 | /api/v1/tareas/ |
| Usuarios | ✅ | ✅ | ❌ | ❌ | /api/v1/usuarios/ |

**Leyenda:**
- ✅ Implementado y funcional
- 🔄 En desarrollo
- ❌ No aplica

## Reglas derivadas de esta visión
- **API First:** Todo desarrollo parte de la API RESTful
- **JWT Universal:** Un token válido en web, mobile y desktop
- **Serializers Reutilizables:** Mismos serializers para todas las plataformas
- **Paginación Consistente:** Cursor-based para web y mobile, page-based para desktop
- **Validaciones Compartidas:** Lógica de negocio en backend, no duplicada en frontend

## Restricciones técnicas
**Framework Web:** Solo React + Vite (no Angular, Vue, Svelte)
- **Base de datos:** PostgreSQL obligatorio (no MySQL, SQLite para prod)
- **Autenticación:** JWT obligatorio (no sessions, OAuth2 directo)
- **Frontend:** Solo React + Vite con TypeScript
- **Mobile:** Solo React Native + Expo (no Flutter, native)
- **Desktop:** Solo WinForms (no WPF, Electron)

## Roadmap de implementación
1. **Fase 1:** API Backend completa (S1) — Base para todo
2. **Fase 2:** Web Frontend (S2) — Interfaz principal
3. **Fase 3:** Mobile App (S3) — Extensión móvil
4. **Fase 4:** Desktop App (S4) — Gestión avanzada
