# PROMPT DE INSTALACIÓN — Sistema Multi-IA
> Pega esto a cualquier IA (Claude Code, Kimi, Codex, Gemini) al inicio de un proyecto nuevo.

---

```
Eres parte de un sistema multi-IA. Vas a instalar y configurar el sistema en este proyecto.

PASO 1 — Clona el sistema en la raíz del proyecto:
```bash
git clone git@github.com:Nelver13/ClaudeMachote.git sistema-ia
```

PASO 2 — Ejecuta el instalador:
```bash
python sistema-ia/instalar.py
```

PASO 3 — Ahora configura el proyecto. Pregúntame UNA por UNA:
1. ¿Nombre del proyecto?
2. ¿Stack? (backend / frontend / fullstack / mobile)
3. ¿IAs que van a trabajar? (Claude / Kimi / Codex / Gemini)
4. ¿Rol de cada IA hoy? (ARQUITECTO o DESARROLLADOR)

PASO 4 — Con esas respuestas:
- Actualiza sistema-ia/ESTADO.md (reemplaza NOMBRE_PROYECTO y ajusta roles)
- Actualiza CLAUDE.md / KIMI.md / CODEX.md / GEMINI.md con el nombre real
- Copia estos archivos a la raíz del proyecto:
  sistema-ia/INICIO.md → ./INICIO.md
  sistema-ia/AGENTS.md → ./AGENTS.md
  sistema-ia/ESTADO.md → ./ESTADO.md
  sistema-ia/CLAUDE.md → ./CLAUDE.md (y los demás según IAs usadas)

PASO 5 — Verifica que sistema-ia/ está en .gitignore del proyecto.
Si no está, agrégalo.

PASO 6 — Avisa: "Listo — [nombre proyecto] configurado — revisa."

Reglas desde ya:
- Sin saludos ni relleno. Fragmentos OK.
- Una pregunta a la vez. Espera respuesta antes de la siguiente.
- Al terminar cada paso: avisa.
- git commit/push/pull/add — NUNCA. Solo el humano toca git.
```
