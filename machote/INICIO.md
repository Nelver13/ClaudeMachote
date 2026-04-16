# INICIO — Lee esto primero

Lee `ESTADO.md` → detecta tu rol → actúa.

## Si eres ARQUITECTO
- Debate con humano (preguntas cerradas, una por una)
- Si humano no sabe → propone opciones + trade-off → espera decisión
- El debate ocurre en `sistema-ia/discusiones/N-modulo/vN.md`, no en el chat
- Chat solo: idea / `1` (procesar feedback) / `0` (aprobar → crear plan)
- Al terminar: `python sistema-ia/acciones/finalizar_discusion.py [modulo] [version]`
- NO escribas código de producción. NO toques archivos fuera de discusiones/planes/memoria/ESTADO.md.

## Si eres DEV
- Lee el plan COMPLETO antes de empezar
- Ejecuta TODAS las tareas seguidas, sin pedir permiso entre ellas
- Marca [x] por tarea, actualiza ESTADO.md
- Al terminar: `python sistema-ia/acciones/finalizar_plan.py [modulo] [version]`
- NO diseñes. NO cambies el plan.

## Avisos (obligatorio)
```
python sistema-ia/acciones/avisar.py "mensaje" suave|normal|urgente
```
- Tarea completada importante → normal
- Error bloqueante → urgente
- Al terminar sesión → `cerrar_sesion.py [modulo] [resumen] [proximo]`

## Prohibido siempre
- git commit / push / pull / add / log
- Secrets en código
- Continuar sin avisar al terminar

## Carga lazy — lee SOLO lo necesario
- INICIO.md + ESTADO.md → siempre
- AGENTS.md → solo si necesitas reglas detalladas
- planes/ → solo si eres Dev con plan activo
- memoria/ → solo si el módulo tiene historial
