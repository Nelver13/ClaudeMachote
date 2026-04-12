# Sistema Multi-IA — Guía rápida

## Estructura

```
./
  AGENT.md        ← reglas universales (todas las IAs leen esto)
  CLAUDE.md       ← específico Claude
  CODEX.md        ← específico Codex/GPT
  KIMI.md         ← específico Kimi
  GEMINI.md       ← específico Gemini
  estado.log      ← estado compartido del proyecto
  acciones/
    avisar.py     ← notificaciones (sonido + popup + discord + ntfy)
    credenciales.md ← configurar webhook y ntfy aquí
  planes/         ← planes maestros por módulo
  memoria/        ← historial de progreso
  benchmark/      ← comparar qué IA hace qué mejor
  logs/           ← log de notificaciones
```

## Inicio rápido

### 1. Configurar notificaciones (opcional)
Editar `./acciones/credenciales.md` con tu webhook de Discord o topic de ntfy.

### 2. Iniciar con cualquier IA
Pegar al inicio de la sesión:
```
[Pegar contenido de AGENT.md]
[Pegar contenido de CLAUDE.md / CODEX.md / KIMI.md / GEMINI.md]
[Pegar contenido de estado.log]
```

### 3. Activar modo
```
modo:arquitecto   → diseñar plan
modo:dev          → ejecutar tarea actual
modo:benchmark    → comparar IAs
```

## Cuándo usar cada IA

| IA | Mejor para |
|----|-----------|
| Claude | Razonamiento complejo, refactoring con contexto, documentación |
| Kimi | Contexto muy largo, leer repo completo, planificación detallada |
| Codex | Generación rápida de código, boilerplate, tests |
| Gemini | Tareas con imágenes/PDFs, búsqueda en docs, casos edge |

## Benchmark

Para comparar IAs en la misma tarea:
1. Definir tarea en `./benchmark/tareas_test.md`
2. Darla a cada IA por separado con `modo:benchmark`
3. Ver resultados en `./benchmark/resultados.md`
