# TOKEN TRACKING — version3ligera
> Sistema de auditoría: tokens, costos, tiempo por discusión/plan
> Luego genera reportes automáticos con IA

---

## 🎯 Qué se registra

| Métrica | Dónde se guarda | Para qué |
|---------|-----------------|----------|
| **Tokens entrada** | `logs/tokens.json` | Cuántos tokens consumió |
| **Tokens salida** | `logs/tokens.json` | Qué generó la IA |
| **Etapa actual** | `logs/tokens.json` | Discusión, plan, ejecución |
| **Duración** | `logs/tokens.json` | Cuánto tardó |
| **Motor usado** | `logs/tokens.json` | Copilot, Claude, Cursor, etc |
| **Costo estimado** | Calculado en reports | $ por tokens |

---

## 📊 Flujo de Datos

```
IA genera discusión
    ↓
log_tokens.py registra:
    - disc_api_v1.md generada
    - tokens_in: 450
    - tokens_out: 1200
    - motor: claude
    - timestamp: 2026-03-23 10:30:00
    - etapa: discusión
    ↓
JSON acumula en logs/tokens.json
    ↓
Cuando terminas etapa:
    python claude/acciones/gen_report.py
    ↓
IA analiza datos y genera:
    - Reporte de costos por etapa
    - Tendencias
    - Recomendaciones
```

---

## 📝 Estructura de logs/tokens.json

```json
{
  "registros": [
    {
      "id": "disc_001",
      "tipo": "discusión",
      "nombre": "disc_api-rest_v1.md",
      "motor": "claude",
      "tokens_in": 450,
      "tokens_out": 1200,
      "total_tokens": 1650,
      "costo_estimado": 0.0165,
      "fecha_inicio": "2026-03-23T10:30:00Z",
      "fecha_fin": "2026-03-23T10:32:30Z",
      "duracion_segundos": 150,
      "etapa": "discusión",
      "estado": "completado",
      "metadata": {
        "version": "v1",
        "feedback_iteraciones": 2,
        "lineas_generadas": 45
      }
    },
    {
      "id": "plan_001",
      "tipo": "plan",
      "nombre": "plan_001_api-rest.md",
      "motor": "claude",
      "tokens_in": 250,
      "tokens_out": 800,
      "total_tokens": 1050,
      "costo_estimado": 0.0105,
      "fecha_inicio": "2026-03-23T10:35:00Z",
      "fecha_fin": null,
      "duracion_segundos": null,
      "etapa": "ejecución",
      "estado": "en_progreso",
      "metadata": {
        "tareas_totales": 5,
        "tareas_completadas": 3,
        "progreso": 60
      }
    }
  ],
  "resumen": {
    "total_tokens": 2700,
    "total_costo": 0.027,
    "tokens_por_motor": {
      "claude": 2700
    },
    "tokens_por_etapa": {
      "discusión": 1650,
      "ejecución": 1050
    },
    "tiempo_total_segundos": 150
  }
}
```

---

## 🔧 Scripts

### 1. log_tokens.py (automático)
Se ejecuta CUANDO:
- IA genera discusión
- IA crea plan
- IA completa tarea

Registra automáticamente tokens + metadata.

### 2. gen_report.py (bajo demanda)
```bash
python claude/acciones/gen_report.py --format html
# Genera: claude/reports/reporte_YYYY-MM-DD.html
```

Crea:
- Tabla de costos por etapa
- Gráfico de tokens por motor
- Tendencias (mejora/empeora)
- Recomendaciones

### 3. audit.py (validación)
```bash
python claude/acciones/audit.py
# Valida integridad de logs/tokens.json
```

---

## 💰 Cálculo de Costos

Basado en precios OpenAI (2026):
```
Claude (Anthropic):
  - Input: $0.50 / 1M tokens
  - Output: $1.50 / 1M tokens

Copilot (GitHub):
  - Incluido en plan

Cursor:
  - Incluido en plan

Google Antigravity:
  - Según tarifa Google
```

**El usuario puede customizar** en `credenciales.md`:
```markdown
## Token Pricing
CLAUDE_INPUT_COST: 0.0005  # $ por 1K tokens
CLAUDE_OUTPUT_COST: 0.0015
COPILOT_COST: 0  # incluido
CURSOR_COST: 0
GOOGLE_COST: 0.001
```

---

## 📋 Reporte Automático

Cuando terminas una etapa, ejecutás:
```bash
python claude/acciones/gen_report.py
```

Genera (ejemplo):

```
═══════════════════════════════════════════
📊 REPORTE TOKENS — v3ligera
═══════════════════════════════════════════

Período: 2026-03-23 10:00 → 14:30 (4.5 horas)

RESUMEN GENERAL
───────────────────────────────────────────
Total tokens:       2700
Costo total:        $0.027
Motor más usado:    Claude (100%)
Etapa más costosa:  Discusión (61%)


DESGLOSE POR ETAPA
───────────────────────────────────────────
Discusión:   1650 tokens ($0.0165)  [████████░░]
Ejecución:   1050 tokens ($0.0105)  [██████░░░░]


DESGLOSE POR MOTOR
───────────────────────────────────────────
Claude:      2700 tokens ($0.027)   100%


DESGLOSE POR DISCUSIÓN
───────────────────────────────────────────
disc_api-rest_v1.md:     1650 tokens  ✅ Completado
plan_001_api-rest.md:    1050 tokens  ⏳ En progreso


RECOMENDACIONES (IA analiza)
───────────────────────────────────────────
⚠️  Etapa Discusión consume 61% → optimizar prompts
✅ Promedio 1650 tokens/discusión es normal
💡 Probar v2 con fewer tokens (agregar constraints)


TENDENCIAS
───────────────────────────────────────────
Última etapa vs promedio: +15% tokens
Mejora: tokens/tarea bajó 5%

═══════════════════════════════════════════
```

---

## 🔐 Privacidad

- `logs/tokens.json` en `.gitignore`
- **NO registra** contenido de discusiones (solo metadata)
- **Registra**: tokens, tiempos, etapas, motor
- Seguro de compartir reportes (sin datos sensibles)

---

## ✅ Qué aprobás

| Feature | Status | Aprueban |
|---------|--------|----------|
| Log automático de tokens | ✅ | Vos |
| Schema JSON para guardar | ✅ | Vos |
| gen_report.py | ✅ | Vos |
| Costos por motor | ✅ | Vos |
| Reportes con recomendaciones IA | ✅ | Vos |
| Dashboard integrado (+ tab) | ✅ | Vos |

---

## 📌 APROBAR ESTO

Si está OK:

```
R:/ OK TOKEN TRACKING — implementá todo
```

O si querés cambios:

```
R:/ Cambiar X a Y, no incluir Z
```

Espero aprobación antes de codear.
