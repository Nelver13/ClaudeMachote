# STACK.md
> Completar al iniciar un proyecto nuevo con esta plantilla.
> Claude lee este archivo en el inicio de sesión para entender el contexto técnico.

---

## Proyecto

- **Nombre:** [nombre del proyecto]
- **Descripción breve:** [qué hace en una línea]
- **Estado:** [Nuevo | En desarrollo | Producción]

---

## Stack tecnológico

| Capa | Tecnología | Versión |
|---|---|---|
| Backend | Django + DRF | - |
| Frontend | React + Vite | - |
| Base de datos | PostgreSQL | - |
| Auth | JWT (SimpleJWT) | - |
| Mobile | - | - |
| Desktop | - | - |
| Infra | Docker / n8n | - |

> Borrar las filas que no aplican. Agregar las que faltan.

---

## Entorno

- **OS destino:** [Windows / Linux / macOS]
- **Python:** [versión]
- **Node:** [versión]
- **Puerto backend:** [ej: 8000]
- **Puerto frontend:** [ej: 5173]
- **Puerto n8n:** [ej: 5678]

---

## Convenciones

- API: RESTful, versionada `/api/v1/`
- Auth: JWT en header `Authorization: Bearer <token>`
- Env: `.env` + `.env.example` — nunca secrets en código
- Git: el arquitecto administra commits y pushes

---

## Notas

_(dependencias especiales, restricciones, decisiones de arquitectura)_
