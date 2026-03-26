# Plan #001 — modo ia
**Fecha:** 2026-03-24
**Estado:** En ejecución
**Discusión origen:** disc_modoia.md

---

## Tareas

### 1. Estructura base
- [x] 1.1 Crear carpeta `modo_ia/` en la raíz
- [x] 1.2 Crear árbol de subcarpetas completo
- [x] 1.3 Crear `.gitignore`

### 2. Scripts de acciones
- [x] 2.1 `avisar.py` — notificación sonido + WhatsApp
- [x] 2.2 `notificar.py` — hook de Notification
- [x] 2.3 `check_secrets.py` — hook PreToolUse
- [x] 2.4 `log_escritura.py` — hook PostToolUse
- [x] 2.5 `iniciar_sesion.py` — registro inicio
- [x] 2.6 `cerrar_sesion.py` — registro cierre + tokens
- [x] 2.7 `motor_detect.py` — detectar motor activo
- [x] 2.8 `backup_n8n.py`
- [x] 2.9 `backup_sql.py`
- [x] 2.10 `iniciar_dashboard.py` — lanza Flask
- [x] 2.11 `finalizar_etapa.py` — cierra etapa + regenera MAPA.md
- [x] 2.12 `init_db.py` — inicializa SQLite con schema completo
- [x] 2.13 `credenciales.md` — plantilla vacía
- [x] 2.14 `README.md` — descripción de cada script

### 3. SQLite schema
- [x] 3.1 Tabla `sesiones` (id, motor, inicio, fin, tokens, costo)
- [x] 3.2 Tabla `etapas` (id, nombre, estado, fecha_inicio, fecha_fin)
- [x] 3.3 Tabla `token_events` (id, sesion_id, timestamp, tipo, valor)
- [x] 3.4 Tabla `discusiones` (id, tipo, nombre, estado, fecha)
- [x] 3.5 Tabla `planes` (id, nombre, tareas_total, tareas_ok, estado)
- [x] 3.6 Tabla `motor_stats` (motor, sesiones, tokens_total, costo_total)

### 4. Dashboard Flask — nuevo desde cero
- [x] 4.1 `app.py` — estructura base Flask + rutas
- [x] 4.2 Tab Inicio — estado proyecto, motor activo, sesión en curso
- [x] 4.3 Tab Discusiones — lista creaciones/ y soluciones/ con estado
- [x] 4.4 Tab Planes — checklist activo, handler marcar [x] funcional
- [x] 4.5 Tab Tokens — consumo real por sesión/etapa, costo estimado
- [x] 4.6 Tab Motores — motor activo, cambiar motor, estado agentes
- [x] 4.7 Tab Reportes — historial etapas, backups, resumen sesiones
- [x] 4.8 `templates/index.html` — UI limpia, funcional
- [x] 4.9 `requirements.txt`

### 5. Token tracking real
- [x] 5.1 Leer archivos desde `~/.claude/projects/` (patrón de version3)
- [x] 5.2 Integrar en `cerrar_sesion.py`
- [x] 5.3 Guardar en SQLite tabla `sesiones`
- [x] 5.4 Mostrar en Tab Tokens del dashboard

### 6. Hooks Claude Code
- [x] 6.1 `.claude/settings.json` con 4 hooks funcionales
  - [x] PreToolUse → check_secrets.py
  - [x] PostToolUse → log_escritura.py
  - [x] Notification → notificar.py
  - [x] UserPromptSubmit → iniciar_dashboard.py

### 7. Skills
- [x] 7.1 `django-drf/SKILL.md` (desde version3)
- [x] 7.2 `react-vite/SKILL.md` (desde version3 + sección git-security)
- [x] 7.3 `mobile/SKILL.md` (nuevo — Flutter + React Native + Electron)
- [x] 7.4 `n8n-flows/SKILL.md` (desde version3 + regla agentes en JSON)
- [x] 7.5 `git-security/SKILL.md` (nuevo — .gitignore por stack, bloqueo secrets)
- [x] 7.6 `docker-prod/SKILL.md` (nuevo — build y deploy producción)
- [x] 7.7 `docker-test/SKILL.md` (nuevo — deploy rápido a servidor de prueba)

### 8. Motores
- [x] 8.1 `motores/claude/.instructions.md`
- [x] 8.2 `motores/cursor/.instructions.md`
- [x] 8.3 `motores/copilot/.instructions.md` (VS Code + Copilot)
- [x] 8.4 `motores/antigravity/.instructions.md` (Google)
- [x] 8.5 `.motor/motor.json` — config base + auto-detect

### 9. Archivos raíz
- [x] 9.1 `CLAUDE.md` v1.0 — protocolo compacto
- [x] 9.2 `MAPA.md` — mapa vectorizado para IA
- [x] 9.3 `STACK.md`

### 10. Prueba en sandbox
- [x] 10.1 Copiar `modo_ia/` a `pruebaversion3/`
- [x] 10.2 Ejecutar `init_db.py` — SQLite creado con 9 tablas
- [x] 10.3 Ejecutar `motor_detect.py` — detectó: copilot / Windows
- [x] 10.4 Levantar dashboard — 6 endpoints responden OK
- [x] 10.5 Simular sesión completa — inicio/sesion + finalizar_etapa OK
- [ ] 10.6 Verificar hooks en Claude Code (requiere abrir Claude Code con modo_ia)

---

## Notas de ejecución
- Bugs encontrados y corregidos en sandbox:
  - `finalizar_etapa.py`: `Path.parent.parent.parent` era un nivel de más → `parent.parent`
  - `motor_detect.py`: mismo bug de path → corregido
  - `app.py`: carácter `→` no compatible con cp1252 en Windows → reemplazado por `->`
  - SQLite no acepta `UPDATE ... ORDER BY ... LIMIT` → usar subquery
  - `iniciar_sesion.py`: `dict.get('detected_motor', default)` no maneja `null` → usar `or`
- Sandbox `pruebaversion3/` tiene la versión probada y funcional
- Token tracking real está en `cerrar_sesion.py` (de version3, probado)
- Hook 10.6 requiere abrir Claude Code con `modo_ia/` como directorio de trabajo
