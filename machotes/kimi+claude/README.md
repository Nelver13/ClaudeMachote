# kimi+claude — Machote

Dos terminales con Claude Code. Ambas usan kimi-k2.5 via Moonshot AI.
Al iniciar cada una pregunta el rol: Arquitecto (Kimi) o Desarrollador.

---

## Setup (una sola vez)

**1. Copiar el machote al proyecto:**
```bash
cp -r machotes/kimi+claude/. ../mi-proyecto/
```

**2. Agregar el token en `.claude/settings.json`:**
```json
"ANTHROPIC_AUTH_TOKEN": "tu_token_real_aqui"
```
Obtener token en: https://platform.moonshot.ai

**3. Agregar `.claude/settings.json` al `.gitignore` del proyecto:**
```
.claude/settings.json
```

**4. Probar avisos:**
```bash
python claude/acciones/avisar.py --test
```

---

## Uso diario

```
Terminal 1          Terminal 2
──────────          ──────────
claude              claude
→ A (Kimi)          → B (Desarrollador)
```

---

## Como verificar que modelo estas consumiendo

Dentro de cualquier terminal Claude Code, ejecutar:
```
/model
```
Debe mostrar `kimi-k2.5`. Si muestra otro modelo, revisar `.claude/settings.json`.

O via Bash:
```bash
echo $ANTHROPIC_MODEL
echo $ANTHROPIC_BASE_URL
```

---

## Flujo

```
Terminal Kimi                     Terminal Desarrollador
────────────────────              ────────────────────
Discutis la idea
Kimi crea disc_tema.md → avisa
Refinás → "0"
Kimi crea plan_001.md  → avisa    escribis "sigue"
                                  Claude ejecuta → avisa por tarea
                                  Termina → "En revision" → avisa
Ves el trabajo → "ok"
Kimi aprueba → avisa
```

---

## Reglas de oro

- Kimi no escribe codigo. Claude no crea planes.
- `git commit/push` solo vos.
- `claude/` nunca va a git.
- `.claude/settings.json` nunca va a git (tiene el token).
