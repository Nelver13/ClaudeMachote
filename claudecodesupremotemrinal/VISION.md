# VISION.md — [Nombre del proyecto]
> Claude genera este archivo en la discusión inicial del proyecto virgen.
> No editar a mano — para modificar la visión, usar disc_vision-update-[tema].md.
> **Generado:** [YYYY-MM-DD] | **Última actualización:** [YYYY-MM-DD]

---

## Qué hace el sistema
[Descripción en 1-3 líneas — qué problema resuelve, para quién]

---

## Soluciones previstas
| ID | Solución | Plataforma | Stack | Orden de construcción | Estado |
|---|---|---|---|---|---|
| S1 | [nombre] | [Web/iOS/Android/Windows/etc.] | [tecnologías] | 1° | Pendiente |

---

## Backend compartido
- **API:** RESTful, versionada `/api/v1/`
- **Auth:** JWT — válido para todos los canales
- **Base de datos:** [PostgreSQL / SQLite / etc.]
- **URL local:** http://localhost:[puerto]

---

## Módulos y qué solución los usa
| Módulo | [S1] | [S2] | [S3] | Endpoint base |
|---|---|---|---|---|
| Auth | Login | Login | Login | /api/v1/auth/ |
| [Módulo] | [operaciones] | [operaciones] | [operaciones] | /api/v1/[ruta]/ |

---

## Reglas de diseño
_(generadas en la discusión según el stack y las soluciones previstas)_

- La API no tiene lógica de presentación — sirve datos, no vistas
- Auth JWT válido para todos los canales desde el inicio
- Permisos por rol, no por plataforma
- [agregar reglas específicas del proyecto]

---

## Restricciones
_(deadline, presupuesto, equipo, infra existente — lo que el arquitecto mencionó)_

- [ninguna por ahora]

---

## Historial de cambios de visión
| Fecha | Cambio | Disc origen |
|---|---|---|
| [YYYY-MM-DD] | Versión inicial | disc_vision-[proyecto].md |
