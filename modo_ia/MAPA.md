# MAPA — modo ia
> Mapa estructural del proyecto. La IA lee esto al inicio para orientarse rápido.
> Se regenera automáticamente al cerrar cada etapa (`finalizar_etapa.py`).
> Última actualización: 2026-03-24 (inicial — plantilla)

---

## Motor activo
`(detectar con motor_detect.py)`

---

## Árbol funcional

```
claude/acciones/              → scripts que Claude ejecuta (no tocar sin leer README.md)
  avisar.py                   → notificación sonido + WhatsApp
  notificar.py                → hook Notification
  check_secrets.py            → hook PreToolUse — bloquea secrets
  log_escritura.py            → hook PostToolUse — registra archivos escritos
  iniciar_sesion.py           → registro inicio de sesión
  cerrar_sesion.py            → registro cierre + tokens reales
  iniciar_dashboard.py        → lanza Flask + sesión (hook UserPromptSubmit)
  motor_detect.py             → detecta IDE/motor activo
  init_db.py                  → inicializa SQLite (ejecutar una vez)
  finalizar_etapa.py          → cierra etapa + regenera este MAPA
  backup_n8n.py               → exporta flujos n8n a JSON
  backup_sql.py               → dump PostgreSQL
  credenciales.md             → credenciales del proyecto (no a git)

claude/discusiones/
  creaciones/                 → ideas nuevas, features, funcionalidades
  soluciones/                 → bugs, gaps, mejoras a algo existente

claude/planes/                → checklists de ejecución aprobados (plan_XXX.md)
claude/dashboard/             → app Flask de control (localhost:5000)
claude/logs/                  → tokens, sesiones, escrituras
claude/backups/n8n/           → backups de flujos n8n
claude/backups/sql/           → dumps PostgreSQL
claude/imagenes/errores/      → screenshots de bugs
claude/imagenes/mejoras/      → referencias UI

.claude/settings.json         → 4 hooks automáticos de Claude Code
.claude/skills/               → instrucciones de stack por tecnología
  django-drf/                 → Django + DRF
  react-vite/                 → React + Vite + git security
  mobile/                     → Flutter + React Native + Electron
  n8n-flows/                  → n8n + agentes IA en JSON
  git-security/               → siempre activo — .gitignore + bloqueo secrets
  docker-prod/                → deploy producción
  docker-test/                → deploy rápido de prueba

motores/                      → instrucciones por motor de IA
  claude/                     → Claude Code CLI
  cursor/                     → Cursor IDE
  copilot/                    → VS Code + Copilot
  antigravity/                → Google Antigravity

.motor/motor.json             → motor detectado (se actualiza solo)
CLAUDE.md                     → protocolo (la IA lo lee)
MAPA.md                       → este archivo
STACK.md                      → stack del arquitecto
```

---

## Discusiones

**Creaciones:** (ninguna aún)
**Soluciones:** (ninguna aún)

---

## Planes activos

(ninguno aún)

---

## Estado actual

```
(estado.log vacío — proyecto nuevo)
```

---

## Reglas para la IA

- Antes de modificar cualquier archivo → verificar en este árbol para qué sirve
- Para discusión nueva → elegir carpeta según tipo: `creaciones/` o `soluciones/`
- Para credenciales → siempre en `claude/acciones/credenciales.md`
- Para secretos → siempre en `.env`, nunca en código
- `claude/` nunca sube a git
- Al cerrar etapa → `finalizar_etapa.py` regenera este archivo automáticamente
