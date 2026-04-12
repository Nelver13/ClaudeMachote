# 🗺️ MAPA DEL PROYECTO — Multi-IA System
> Formato: embedding-optimized | Auto-generado: 2026-04-12 17:54

```
[PROYECTO] mi-proyecto
[RAIZ] ./
[ESTADO] 0% — definir plan
[ESTRUCTURA] 5 dirs | 12 MD | 9 PY | 3 audio
```

---

## 📁 DIRECTORIOS (5)

| Path | Contenido |
|------|-----------|
| `./acciones/` | 14 archivos |
| `./benchmark/` | 2 archivos |
| `./discs/` | 1 archivos |
| `./logs/` | 1 archivos |
| `./{claude,acciones,planes,memoria,benchmark,logs,discs}/` | 0 archivos |

---

## 📄 ARCHIVOS CORE (leer al inicio)

| Archivo | Propósito | Tokens est. |
|---------|-----------|-------------|
| `AGENT.md` | Reglas universales TODAS las IAs | ~300 |
| `MAPA.md` | Este archivo — índice del proyecto | ~600 |
| `estado.log` | Estado actual | ~50 |

---

## 🤖 CONFIG POR IA (leer según quién soy)

| Archivo | Para | Tokens |
|---------|------|--------|
| `CLAUDE.md` | Claude | ~200 |
| `KIMI.md` | Kimi | ~150 |
| `CODEX.md` | Codex | ~150 |
| `GEMINI.md` | Gemini | ~200 |

---

## ⚡ SCRIPTS (`./acciones/`)

| Script | Función | Args |
|--------|---------|------|
| `avisar.py` | Notificar | `"msg" tipo` |
| `actualizar_checklist.py` | Marcar tarea | `<plan> <N>` |
| `finalizar_etapa.py` | Cerrar etapa | `[nombre]` |
| `backup_n8n.py` | Backup n8n | `[N]` |
| `backup_sql.py` | Backup DB | `[N]` |
| `check_secrets.py` | Detectar secretos | — |
| `actualizar_mapa.py` | Actualizar este archivo | — |

---

## 🎯 FLUJO RÁPIDO

```
1. Leer AGENT.md + MAPA.md + estado.log
2. modo:arquitecto → discs/[modulo]/v[N].md
3. modo:dev → estado.log → tarea → avisar.py → [x]
4. finalizar_etapa.py → backup → avisar.py
```

---

## 📊 ESTADO ACTUAL

```
PROYECTO: mi-proyecto
MODULO: (vacío)
PLAN: v1
IA: ninguna
TAREA_ACTUAL: 1
PROGRESO: 0%
NEXT_TASK: definir plan
```

---

## 🔔 COMANDOS

```bash
# Notificar (suave|normal|urgente)
python ./acciones/avisar.py "Tarea N: X" normal

# Actualizar este mapa
python ./acciones/actualizar_mapa.py

# Test
python ./acciones/avisar.py --test
```

---

## ⚠️ REGLAS

1. No hablar. Hacer. Avisar.
2. Una tarea por sesión (modo:dev)
3. NUNCA git commit/push
4. Siempre avisar.py al terminar
5. **Actualizar MAPA.md tras cambios estructurales**

---

```
[AUTO] Regenerado: 2026-04-12 17:54 | Archivos: 26 | Dirs: 5
[ACCION] Si cambiaste estructura: python ./acciones/actualizar_mapa.py
```
