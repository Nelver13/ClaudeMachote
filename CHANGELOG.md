# Changelog

## v2.1 — 2026-04-16
### Agregado
- `auto_setup.py` — SessionStart hook: detecta proyecto nuevo vs existente, carga contexto automático
- `cerrar_sesion.py` — guarda resumen comprimido del día en memoria/sesiones/
- `comprimir_discusion.py` — comprime temas cerrados en discusiones largas
- `migrar.py` — migra proyectos con sistema IA viejo al nuevo
- `PROMPT_INSTALAR.md` — prompt listo para instalar en proyecto nuevo
- `PROMPT_MIGRAR.md` — prompt listo para migrar proyecto viejo
- Skill `caveman` — modo comunicación ultra-comprimido (-75% tokens)

### Mejorado
- `avisar.py` — guarda checkpoint en ESTADO.md antes de notificar
- `finalizar_discusion.py` — genera JSON handoff además del PROMPT_DEV.txt
- `modo-dev/SKILL.md` — flujo explícito: ejecuta → marca [x] → actualiza ESTADO.md → avisa por tarea
- `modo-arquitecto/SKILL.md` — debate en archivo, avisa en cada paso, cierra sesión al aprobar
- `INICIO.md` — reducido a 35 líneas (carga lazy)
- `settings.json` — permisos automáticos + hook SessionStart

### Estructura nueva
- `sistema-ia/handoff/` — JSON de traspaso arquitecto → dev
- `sistema-ia/memoria/sesiones/` — contexto diario comprimido

---

## v2.0 — 2026-04-15
- Primer machote virgen multi-IA (Claude / Kimi / Codex / Gemini)
- Sistema arquitecto/dev con roles intercambiables
- Scripts base: avisar.py, cambiar_rol.py, finalizar_plan.py, finalizar_discusion.py
