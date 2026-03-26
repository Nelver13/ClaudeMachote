# CLAUDE.md — version3ligera
> Control remoto del sistema. Esto es lo que necesitás saber para usarlo.
> **La IA NO toca esto. Solo VOS.**

---

## 📍 ARQUITECTURA — lo que cambia

```
version3ligera/
├── motores/                    ← NUEVA ESTRUCTURA
│   ├── claude/
│   ├── cursor/
│   ├── copilot/
│   └── antigravity/
├── claude/                     ← Carpeta compartida (trabajo actual)
│   ├── discusiones/
│   │   ├── borrador/          ← IA genera aquí (arquitecto NO toca)
│   │   └── final/             ← IA mueve cuando está pulido
│   ├── planes/                ← IA memoria (si lo ve, se basa)
│   ├── dashboard/
│   ├── acciones/
│   └── imagenes/
├── .motor/
│   └── motor.json             ← Se actualiza AUTO en cada inicio
├── CLAUDE.md                  ← Este archivo (vos decidís)
└── credenciales.md            ← Fuera de git
```

---

## 🔄 FLUJO AUTOMÁTICO (NO requiere manual)

### Al iniciar consola/IDE:

1. **Auto-detect motor** → actualiza `.motor/motor.json`
   ```bash
   # Se ejecuta SOLO (sin que hagas nada)
   python claude/acciones/motor_detect.py
   ```

2. **Motor activo listo** → la IA sabe cuál es

3. **Dashboard sincronizado** → muestra motor actual

---

## 🎨 DASHBOARD — Lo que VOS ves

```
┌─────────────────────────────────────────┐
│ 🚀 Version3Ligera          [Cambiar motor ▼]
├─────────────────────────────────────────┤
│                                         │
│ Motor actual: Claude                    │
│ IDE: VS Code                            │
│ Status: ✅ Listo                        │
│                                         │
├─────────────────────────────────────────┤
│ DISCUSIONES                             │
│ ├─ 📄 Borrador (3)                      │
│ │   └─ disc_api-rest_v1.md              │
│ │   └─ disc_auth_v2.md                  │
│ ├─ ✅ Final (5)                         │
│ │   └─ disc_database_aprobado.md        │
│                                         │
├─────────────────────────────────────────┤
│ PLANES EN EJECUCIÓN                     │
│ ├─ plan_001_api-rest      [████░░] 67% │
│ └─ plan_002_auth          [██░░░░░] 28% │
│                                         │
└─────────────────────────────────────────┘
```

### Botón [Cambiar motor ▼]
Dropdown con: Claude, Cursor, Copilot, Antigravity
- Click → motor_detect actualiza automático
- Recarga dashboard en vivo

---

## 📋 DISCUSIONES — Carpetas automáticas

### borrador/
- IA crea: `disc_tema_v1.md`
- Arquitecto: **NO toca nada**
- IA itera: v1 → v2 → v3 → cuando está listo

### final/
- IA mueve desde borrador cuando está "aprobado"
- Nombre: `disc_tema_aprobado.md`
- Contiene: versión final + timestamp

### Historial automático
- Cada cambio registra: timestamp + diff de qué cambió
- Dashboard lo muestra: "actualizado hace 2 min"

---

## 📝 PLANES — Memoria de IA

Archivo: `claude/planes/plan_XXX.md`

```markdown
# Plan #001 — API REST
**Motor**: Claude
**Discusión origen**: disc_api-rest_aprobado.md
**Estado**: En ejecución

## Checklist
- [x] Tarea 1
- [ ] Tarea 2 ← IA se basa aquí

## Memoria (para IA)
- Decisión: Use DRF + JWT
- Contexto: Cliente pide autenticación estricta
- Próximo: Tests unitarios
```

IA **SIEMPRE** revisa esto antes de actuar.

---

## 🔧 MOTORES - Carpetas por IDE

Cada motor tiene su carpeta:

### motores/claude/
```
├── .instructions.md    ← Instrucciones específicas
├── prompts.json        ← Prompts optimizados para Claude
└── context.md          ← Contexto que Claude necesita
```

### motores/cursor/
```
├── .prompt.md          ← Prompt optimizado para Cursor
├── settings.json       ← Config Cursor
└── context.md
```

### motores/copilot/
```
├── .github/copilot-instructions.md
├── prompts.json
└── context.md
```

### motores/antigravity/
```
├── api.schema          ← API Google adaptada
├── prompts.json
└── context.md
```

---

## 🔐 Reglas Clave

| Acción | Quién | Automático |
|--------|-------|-----------|
| Detectar motor | IA | ✅ Cada inicio |
| Crear borrador | IA | ✅ Cuando pidas algo |
| Pulir discusión | IA | ✅ Iteraciones |
| Mover a final | IA | ✅ Cuando está OK |
| Cambiar motor (dashboard) | VOS | ✅ UI dropdown |
| Editar borrador | VOS | ❌ NO, es de IA |
| Leer plan | IA | ✅ Se basa en eso |
| Modificar CLAUDE.md | VOS | ✅ Controlás todo |

---

## 📊 Dashboard Features

✅ **Auto-refresh** cada 5 segundos
✅ **Dropdown de motores** — cambio dinámico
✅ **Historial de discusiones** — ver evolución
✅ **Timestamp de cambios** — "hace 2 min"
✅ **% progreso planes** — visual de estado
✅ **Diff inline** — qué cambió vs. versión anterior

---

## 🚀 Primeros Pasos (para VOS)

1. **Abrí version3ligera en tu IDE**
2. **No hagas nada** — motor_detect.py se ejecuta solo
3. **Abre dashboard** → `http://localhost:5000`
4. **Ves el motor actual** en la UI
5. **Describe tarea en chat** → IA crea borrador en `discusiones/borrador/`
6. **Dashboard actualiza en vivo** → ves la evolución
7. **Cuando esté listo** → IA mueve a `final/`

---

## 💡 Ejemplo Real

```
TÚ (en Claude/Cursor/Copilot):
  "Quiero una API REST que valide emails"

MOTOR AUTOMÁTICO:
  ✅ Detecta: Claude en VS Code
  ✅ Crea: discusiones/borrador/disc_validar-emails_v1.md
  ✅ Avisos: "🔧 Analizando..."

DASHBOARD (lo ves):
  📄 Borrador (1)
    └─ disc_validar-emails_v1.md ← actualizo ahora mismo

TÚ:
  Leés, das feedback: "R:/ Agregar JWT también"

MOTOR:
  ✅ Actualiza: disc_validar-emails_v2.md
  ✅ Genera también: plan_XXX.md con todo
  
DASHBOARD:
  ✅ Final (1)
    └─ disc_validar-emails_aprobado.md
  
  📝 Plans en ejecución
    └─ plan_001_validar-emails [███░░] 60%
```

---

## 🛑 Qué NO debes hacer

- ❌ Tocar `discusiones/borrador/` (es donde trabaja la IA)
- ❌ Editar `planes/` directamente (son notas de IA)
- ❌ Cambiar motor manualmente (está automatizado)
- ❌ `git commit` o `git push` (vos administrás esto)

---

## 📌 Cambios vs. version3

| Feature | version3 | version3ligera |
|---------|----------|---|
| Auto-detect motor | Manual | ✅ Automático cada inicio |
| Dashboard | Básico | ✅ Con switch dinámico |
| Discusiones | carpeta única | ✅ borrador/ + final/ |
| Planes | Simple | ✅ Memoria para IA |
| Contextualización | Genérica | ✅ Por motor (motores/) |
| Visualización historial | No | ✅ Timeline con diffs |

---

## 🎯 Resumen

**Vos**: Describe ideas, leés feedback, cambias motor (UI)
**IA**: Todo lo demás — detección, creación, evolución, memorización

**Dashboard**: Sincronizado → ves TODO en vivo → sin sorpresas
