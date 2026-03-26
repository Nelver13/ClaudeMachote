# disc_restructura-v3 — Rediseño de ClaudeMachote para mayor eficiencia
**Estado:** En discusión
**Fecha:** 2026-03-23

---

## Pregunta del arquitecto
¿Cómo estructurar mejor el sistema para ser más eficiente en análisis y programar de forma más dinámica y ordenada, desde los cimientos hasta la obra?

---

## Diagnóstico actual — qué frena la eficiencia

### Problema 1 — Arranque pesado
Cada sesión nueva Claude lee: `CLAUDE.md` (enorme) + `STACK.md` + `estado.log` + `RESUMEN.md`.
Son 4 archivos, ~400 líneas de contexto antes de hacer nada.
**Consecuencia:** latencia de contexto alta, riesgo de que Claude pierda el hilo en sesiones largas.

### Problema 2 — version1/ y version2/ conviven en el repo
No hay un mecanismo claro de "esta es la versión activa".
Al copiar a un proyecto nuevo, el arquitecto tiene que recordar que es `version2/`.
**Consecuencia:** confusión, riesgo de copiar la versión equivocada.

### Problema 3 — El CLAUDE.md mezcla protocolo + reglas + estructura
Un solo archivo hace de: manual de flujo, tabla de permisos, formato de logs, reglas de seguridad, instrucciones de proyecto virgen.
**Consecuencia:** Claude tiene que parsear todo para encontrar lo relevante al momento.

### Problema 4 — Skills estáticos
Los skills se cargan por detección de archivos pero no hay un mecanismo de composición.
Un proyecto Django+React+n8n carga 3 skills por separado sin un punto de integración.
**Consecuencia:** Claude puede tener instrucciones contradictorias o gaps entre skills.

### Problema 5 — No hay capa de "cimientos"
El sistema pasa directo de discusión → plan → ejecución.
No hay registro de decisiones de arquitectura (ADR), ni capas: datos → servicios → API → UI.
**Consecuencia:** Claude no tiene contexto de por qué se tomaron ciertas decisiones estructurales.

---

## Propuesta — ClaudeMachote v3 "desde los cimientos"

### Capa 0 — Core (siempre cargado, mínimo)
```
CLAUDE.md          ← solo protocolo de flujo (50 líneas max)
STACK.md           ← stack del arquitecto
.claude/
  settings.json    ← permisos y hooks
  core.md          ← reglas absolutas (nunca commit, nunca secrets, etc.)
```
`CLAUDE.md` delega todo lo no-esencial a archivos específicos.
Claude carga solo `core.md` + `settings.json` al arrancar. Liviano.

### Capa 1 — Memoria del proyecto (claude/)
```
claude/
  estado.log       ← estado granular (igual que ahora)
  RESUMEN.md       ← 5 líneas (igual que ahora)
  ADR.md           ← Architecture Decision Records (NUEVO)
  discusiones/
  planes/
  backups/
  imagenes/
```
**ADR.md** — registro de decisiones tomadas. Ej:
```
[2026-03-10] Se eligió PostgreSQL sobre SQLite por soporte de JSONB
[2026-03-15] Auth con JWT en vez de sesiones por requerimiento mobile
```
Claude lo consulta antes de proponer algo que pueda contradecir una decisión previa.

### Capa 2 — Skills por stack (composición)
Cada skill tiene un archivo `INTEGRA.md` que define cómo convive con otros skills:
```
.claude/skills/
  django-drf/
    SKILL.md
    INTEGRA.md     ← "con react-vite: CORS en settings.py, proxy en vite.config"
  react-vite/
    SKILL.md
    INTEGRA.md     ← "con django-drf: baseURL desde .env, axios interceptors"
```
Cuando Claude detecta stack múltiple, lee los `INTEGRA.md` para tener visión unificada.

### Capa 3 — Flujo de trabajo (igual pero más explícito en capas)
```
Discusión aprobada
      ↓
plan_XXX.md generado con secciones por capa:
  ## Cimientos (modelos, DB, migraciones)
  ## Servicios (lógica de negocio, serializers)
  ## API (vistas, rutas, auth)
  ## UI (componentes, páginas, hooks)
  ## Integración y tests
```
El plan siempre sigue el orden bottom-up. Claude no toca UI hasta terminar la capa de datos.

### Capa 4 — Distribución del template
Eliminar version1/ y version2/. Usar un solo directorio `template/` como fuente de verdad.
Versionado por git tags: `v2.0`, `v3.0`.
```
ClaudeMachote/
  template/        ← lo que se copia a cada proyecto nuevo
  MAPA.md          ← instrucciones de uso (igual que ahora)
  STACK.md
  CLAUDE.md
```

---

## Comparación

| Aspecto | Ahora (v2) | Propuesta (v3) |
|---|---|---|
| Contexto al arrancar | ~400 líneas | ~80 líneas (core.md) |
| Versiones en el repo | version1/ + version2/ | template/ + git tags |
| Decisiones de arquitectura | No existe | ADR.md |
| Skills multi-stack | Carga separada | INTEGRA.md por skill |
| Orden de ejecución | Libre | Bottom-up forzado por secciones del plan |
| CLAUDE.md | Todo en uno | Solo protocolo, delega a core.md |

---

## Preguntas abiertas

1. ¿El ADR.md lo mantiene el arquitecto, Claude, o ambos?
2. ¿Querés que el plan bottom-up sea obligatorio siempre o solo para proyectos nuevos?
3. ¿La carpeta se sigue llamando `version2/` → `template/` o preferís otro nombre?
4. ¿Los `INTEGRA.md` por skill los armamos ahora o en una etapa posterior?

---

## Riesgos

- Migrar proyectos existentes de v2 a v3 requiere mover archivos en `claude/`
- Si `core.md` crece, volvemos al problema del CLAUDE.md pesado — necesita disciplina para mantenerse corto
- ADR.md puede quedar desactualizado si no se incorpora al flujo de cierre de etapa

---

## Próximo paso si se aprueba
Generar plan de refactor de ClaudeMachote mismo: reorganizar dirs, crear ADR.md template, escribir INTEGRA.md para cada skill existente, reescribir CLAUDE.md compacto.
