# PROMPT DE INSTALACIÓN — Sistema Multi-IA v2.7
> Pega esto a cualquier IA al inicio de un proyecto nuevo.

---

```
Instala el sistema multi-IA en este proyecto.

PASO 1 — Clona el sistema:
git clone git@github.com:Nelver13/ClaudeMachote.git sistema-ia

PASO 2 — Ejecuta el instalador:
python sistema-ia/machote/instalar.py

Esto hace TODO automáticamente:
- Crea archivos raíz (ESTADO.md, AGENTS.md, INICIO.md, etc.)
- Crea carpetas (planes/, discusiones/, bugs/, memoria/)
- Configura .claude/settings.json con hooks
- Borra .git/ de sistema-ia (sin repo anidado)
- Crea discusión de visión (0-vision)
- Crea backlog de bugs
- Genera run.bat/run.sh base
- Instala dependencias del bug reporter

PASO 3 — Configúrame el proyecto. Pregúntame UNA por UNA:
1. ¿Nombre del proyecto?
2. ¿Stack? (backend / frontend / fullstack / mobile / desktop)
3. ¿IAs que van a trabajar? (Claude / Kimi / Codex / Gemini)
4. ¿Rol de cada IA? (ARQUITECTO o DESARROLLADOR)

Con esas respuestas actualiza ESTADO.md y los archivos de IA.

PASO 4 — Listo. Arranca la discusión de visión (0-vision).

Reglas:
- Sin saludos ni relleno. Respuestas cortas.
- Una pregunta a la vez.
- git commit/push/add — NUNCA.
```
