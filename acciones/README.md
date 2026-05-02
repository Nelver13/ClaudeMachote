# claude/acciones/ — Scripts del sistema

## Quien llama cada script

| Script | Quien lo llama | Cuando |
|---|---|---|
| `avisar.py "msg" tipo` | Claude (Opus y Sonnet) | Al terminar cada respuesta y al cerrar etapa |
| `actualizar_checklist.py <plan> <N>` | Claude Sonnet | Al completar cada tarea del plan |
| `finalizar_etapa.py [nombre]` | Claude Sonnet | Al cerrar etapa completa |
| `backup_n8n.py [N]` | Claude Sonnet | Al cerrar etapa (si hay n8n) |
| `backup_sql.py [N]` | Claude Sonnet | Al cerrar etapa (si hay DB) |
| `check_secrets.py` | Hook PreToolUse | Antes de cada Bash |

## Tipos de aviso
- `suave` — respuesta lista, tarea completada
- `normal` — plan generado, etapa terminada
- `urgente` — error bloqueante, secreto detectado

## Canales
- Windows popup (espera click) + sonido local (aviso_*.mp3)
- Webhook JSON (Discord/Slack)

## Diagnostico
```bash
python claude/acciones/avisar.py --test
```
Log: `claude/logs/notificaciones.log`

## Credenciales
En `credenciales.md` — mismo directorio.
Tener la credencial = permiso de usarla.
Si no esta → parar y pedirla antes de continuar.
