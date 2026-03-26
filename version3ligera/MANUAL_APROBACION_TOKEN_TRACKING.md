# MANUAL DE APROBACIÓN — Token Tracking

Leé todo. Aprueban cada feature. Marca qué SÍ y qué NO.

---

## 📋 Features Propuestos

### ✅ 1. Log Automático de Tokens (log_tokens.py)

**Qué hace:**
```python
log_token_event(
    event_type='discusión',
    event_name='disc_api_v1.md',
    tokens_in=450,      # Tokens entrada
    tokens_out=1200,    # Tokens salida
    motor='claude',
    etapa='discusión'
)
```

Se ejecuta automáticamente cuando IA genera:
- Discusiones → registra tokens_in + tokens_out
- Planes → registra tokens consumidos
- Tareas ejecutadas → registra iteraciones

**Archivos generados:**
```
claude/logs/tokens.json  ← JSON acumulativo
```

**Qué registra:**
- ID único de evento
- Tipo (discusión, plan, ejecución)
- Tokens entrada/salida
- Motor activo
- Etapa (discusión, ejecución)
- Timestamps
- Duración
- Metadata (versión, iteraciones, etc)

**NO registra:**
- ❌ Contenido de discusiones (privacidad)
- ❌ Texto completo (solo metadata)

**Aprueban?**
```
☐ SÍ — log_tokens.py
☐ NO — no quiero tracking de tokens
☐ CAMBIOS — solo registrar X, no Y
```

---

### ✅ 2. Schema JSON para Guardar (tokens.json)

**Estructura:**
```json
{
  "registros": [
    {
      "id": "abc123",
      "tipo": "discusión",
      "nombre": "disc_api.md",
      "motor": "claude",
      "tokens_in": 450,
      "tokens_out": 1200,
      "costo_estimado": 0.0165,
      "fecha_inicio": "2026-03-23T10:30:00Z",
      "estado": "completado",
      "metadata": { ... }
    }
  ],
  "resumen": {
    "total_tokens": 2700,
    "total_costo": 0.027,
    "tokens_por_motor": { ... },
    "tokens_por_etapa": { ... }
  }
}
```

**En .gitignore**: SÍ (NO sube a git)

**Aprueban?**
```
☐ SÍ — schema JSON
☐ NO — otro formato
☐ CAMBIOS — agregar/quitar fields
```

---

### ✅ 3. Reportes (gen_report.py)

**Ejecutar:**
```bash
# Generar HTML
python claude/acciones/gen_report.py --format html
# → claude/reports/reporte_2026-03-23_10-30.html

# Generar JSON
python claude/acciones/gen_report.py --format json

# Generar texto
python claude/acciones/gen_report.py --format text
```

**Qué genera:**
- Tabla de tokens por etapa
- Gráfico visual (%) en HTML
- Desglose por motor
- Últimos registros
- Timestamps

**Ejemplo reporte:**
```
═══════════════════════════════════════════
📊 REPORTE TOKENS — version3ligera
═══════════════════════════════════════════

RESUMEN GENERAL
─────────────────────────────────────────
Total tokens:       2700
Costo total:        $0.027
Registros completados: 2

DESGLOSE POR ETAPA
─────────────────────────────────────────
Discusión:   1650 tokens (61%)
Ejecución:   1050 tokens (39%)

DESGLOSE POR MOTOR
─────────────────────────────────────────
Claude:      2700 tokens (100%)
```

**Aprueban?**
```
☐ SÍ — gen_report.py
☐ NO — no quiero reportes
☐ CAMBIOS — formato diferente, no incluir X
```

---

### ✅ 4. Costos por Motor

**Precios por defecto:**
```
Claude (Anthropic):
  Input: $0.0005 / 1K tokens
  Output: $0.0015 / 1K tokens

Copilot: $0 (incluido)
Cursor: $0 (incluido)
Google: $0.001 / 1K tokens
```

**Se puede customizar en credenciales.md:**
```markdown
## Token Pricing
CLAUDE_INPUT_COST: 0.0005
CLAUDE_OUTPUT_COST: 0.0015
COPILOT_COST: 0
CURSOR_COST: 0
GOOGLE_COST: 0.001
```

**Aprueban?**
```
☐ SÍ — costos automáticos
☐ NO — manejo manual de precios
☐ CAMBIOS — otros motores, otros precios
```

---

### ✅ 5. Dashboard con Tab de Tokens

**Integración al dashboard:** Agregar tab "💰 Tokens"

**Contenido:**
```
┌─────────────────────────────────────┐
│ 💰 Tokens                           │
├─────────────────────────────────────┤
│ Total: 2700 | Costo: $0.027        │
│                                     │
│ Por Etapa:                          │
│ Discusión  [████░░░░░░] 1650 tk   │
│ Ejecución  [███░░░░░░░] 1050 tk   │
│                                     │
│ Por Motor:                          │
│ Claude     [██████████] 2700 tk   │
│                                     │
│ [Descargar Reporte HTML]            │
└─────────────────────────────────────┘
```

**Aprueban?**
```
☐ SÍ — tab en dashboard
☐ NO — solo reportes, no en dashboard
☐ CAMBIOS — otra visualización
```

---

### ✅ 6. Recomendaciones de IA (Futuro)

**Idea:** Cuando haces `gen_report.py`, IA analiza:
- "Etapa X consume 70% tokens → puede optimizarse"
- "Claude es 5x más caro que Copilot"
- "Iteraciones bajaron 20% (mejora)"

**Requiere:** Conectar a API de IA (Claude/Copilot)

**Aprueban?**
```
☐ SÍ — análisis automático  
☐ NO — solo datos
☐ DESPUÉS — implementar luego
```

---

## 🎯 APROBACIÓN FINAL

Leé TODAS las secciones arriba. Luego:

**Opción 1: Todo OK**
```
R:/ OK TOKEN TRACKING — implementá todo exacto como está
```

**Opción 2: Cambios específicos**
```
R:/ TOKEN TRACKING:
  - Sí a log_tokens.py
  - Sí a gen_report.py
  - SÍ dashboard tab
  - NO análisis IA (para después)
  - CAMBIO: precios en USD, no dólares
```

**Opción 3: No querés esto**
```
R:/ NO TOKEN TRACKING — no implementes nada
```

---

## 📌 Espero aprobación antes de integrar todo

**La IA no tocará nada hasta que apruebes.** Solo estoy haciendo propuesta.

Revisá TOKEN_TRACKING.md también (tiene toda la info).

¿Qué dicen?
