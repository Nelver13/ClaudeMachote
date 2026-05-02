# PROMPT DE INSTALACIÓN — Sistema Multi-IA v2.7
> Pega esto a cualquier IA al inicio de un proyecto nuevo.

---

```
Instala el sistema multi-IA en este proyecto.

PASO 1 — Clona y ejecuta:
git clone https://github.com/Nelver13/ClaudeMachote.git sistema-ia
python sistema-ia/instalar.py

Eso hace TODO automáticamente:
- Archivos raíz (ESTADO.md, AGENTS.md, INICIO.md, etc.)
- Carpetas (planes/, discusiones/, bugs/, memoria/)
- .claude/settings.json con hooks
- run.bat y run.sh base
- Discusión 0-vision creada
- Backlog de bugs creado
- Dependencias instaladas (Pillow, pynput, SpeechRecognition, pyaudio)
- Guía de inicio mostrada

PASO 2 — Configúrame el proyecto. Pregúntame UNA por UNA:
1. ¿Nombre del proyecto?
2. ¿Stack? (backend / frontend / fullstack / mobile / desktop)
3. ¿IAs que van a trabajar? (Claude / Kimi / Codex / Gemini)
4. ¿Rol de cada IA? (ARQUITECTO o DESARROLLADOR)

Con esas respuestas actualiza ESTADO.md y los archivos de IA.

PASO 3 — Listo. Arranca la discusión de visión (0-vision).

Reglas:
- Sin saludos ni relleno. Respuestas cortas.
- Una pregunta a la vez.
- git commit/push/add — NUNCA.
```
