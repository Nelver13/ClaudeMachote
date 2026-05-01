# ClaudeMachote — Sistema Multi-IA para Gestión de Proyectos

Bienvenido al sistema **ClaudeMachote**, una arquitectura basada en roles (Arquitecto y Desarrollador) diseñada para trabajar colaborativamente con IAs como Claude, Kimi, Codex, y Gemini en cualquier proyecto de software. 

Este sistema genera un entorno estandarizado que mantiene un historial claro de diseño (planes y discusiones) y previene pérdida de contexto entre sesiones.

---

## 🚀 Instalar en un proyecto nuevo

Copia este prompt y pégalo a la IA en un proyecto vacío:

```text
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

---

## 🔄 Actualizar un proyecto existente a la última versión

Copia este prompt y pégalo a la IA en tu proyecto actual:

```text
Actualiza el sistema IA de este proyecto.

== REGLAS — NUNCA TOCAR ==
- ESTADO.md
- discusiones/ planes/ memoria/ handoff/
- Código de producción del proyecto
- Nombre del proyecto, stack, roles configurados
Si tienes duda → para y avisa. No adivines.

== PASO 1 — Re-clonar en temporal ==
git clone git@github.com:Nelver13/ClaudeMachote.git sistema-ia-temp

== PASO 2 — Copiar solo scripts y skills ==
Copia SOLO estos directorios del clon nuevo al existente:
- sistema-ia-temp/acciones/ → sistema-ia/acciones/ (reemplazar todo)
- sistema-ia-temp/.claude/skills/ → sistema-ia/.claude/skills/ (reemplazar todo)
- sistema-ia-temp/VERSION → sistema-ia/VERSION

NO tocar: discusiones/ planes/ memoria/ handoff/ ESTADO.md

== PASO 3 — Borrar el clon temporal ==
Elimina sistema-ia-temp/ completamente.

== PASO 4 — Verificar ==
python sistema-ia/acciones/avisar.py "test actualizacion" suave
Debe sonar + popup. Si falla → avisa con error exacto.

== PASO 5 — Leer NOVEDADES.md ==
Lee sistema-ia/NOVEDADES.md y aplica las instrucciones de la versión nueva.

== PASO 6 — Verificar archivos raíz ==
Verifica que existen: INICIO.md, AGENTS.md, ESTADO.md
Si faltan → copiar de sistema-ia-temp/machote/ (antes de borrarlo)
NO sobrescribir los que ya existen con datos del proyecto.

== PASO 7 — Avisar ==
python sistema-ia/acciones/avisar.py "Sistema actualizado a vX.Y" normal

== PASO 8 — Reportar ==
- Versión instalada
- Qué se actualizó
- Plan activo: intacto o no
- Algo raro encontrado

== REGLAS GIT ==
✅ Permitido: git status / git clone (solo para el temporal)
❌ Prohibido: git commit / git push / git add
```

---

## 🐛 Bug Reporter Universal con Dictado por Voz

A partir de la versión v2.7, el sistema incluye un reporte de bugs activable mediante **Alt+R**.
Te permite capturar la pantalla, dibujar rectángulos rojos enumerados para señalar el problema y escribir una descripción. 

Además, cuenta con una función de **🎤 Dictado por Voz (estilo Walkie-Talkie)**: presionas el botón para grabar, hablas tu reporte, vuelves a presionar, y la IA transcribirá automáticamente tu voz a texto.

Los bugs se envían directamente a la cola (`discusiones/bugs/backlog.md`) para que el Arquitecto los pueda procesar en el próximo ciclo de planificación.
