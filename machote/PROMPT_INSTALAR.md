# PROMPT DE INSTALACIÓN — Sistema Multi-IA v2.4
> Pega esto a Claude Code al inicio de un proyecto nuevo.

---

```
Instala el sistema multi-IA en este proyecto. Sigue los pasos en orden.

PASO 1 — Clona el sistema en la raíz del proyecto:
git clone git@github.com:Nelver13/ClaudeMachote.git sistema-ia

PASO 2 — Ejecuta el instalador:
python sistema-ia/machote/instalar.py

Esto crea: archivos raíz del proyecto, carpetas sistema-ia/, .claude/settings.json con hooks automáticos.

PASO 3 — Configúrame el proyecto. Pregúntame UNA por UNA:
1. ¿Nombre del proyecto?
2. ¿Stack? (backend / frontend / fullstack / mobile / otro)
3. ¿IAs que van a trabajar? (Claude / Kimi / Codex / Gemini)
4. ¿Rol de cada IA hoy? (ARQUITECTO o DESARROLLADOR)

PASO 4 — Con esas respuestas actualiza:
- ESTADO.md → reemplaza NOMBRE_PROYECTO, ajusta roles
- CLAUDE.md / KIMI.md / CODEX.md / GEMINI.md → reemplaza NOMBRE_PROYECTO

PASO 5 — Verifica que sistema-ia/ está en .gitignore. Si no, agrégalo.

PASO 6 — Avisa: "Listo — [nombre] configurado. Abre Claude Code para empezar."

Reglas desde ya:
- Sin saludos ni relleno. Respuestas cortas.
- Una pregunta a la vez. Espera respuesta antes de la siguiente.
- git commit/push/pull/add — NUNCA. Solo el humano toca git.
```
