# 🚀 Inicio Rápido — version3ligera

Copiaste el sistema de `version3` y lo adaptaste para que funcione con múltiples motores de IA (Copilot, Claude, Cursor, Google Antigravity). Acá está cómo empezar.

---

## 1️⃣ Setup Inicial

**Auto-Detect:** El sistema detecta motor automáticamente. No necesitás correr nada.

Cuando inicies, `motor_detect.py` se ejecuta solo:
- ¿Estás en VS Code?
- ¿Qué extensiones de IA tenés?
- ¿Cursor IDE?
- Actualiza `.motor/motor.json` automático

---

## 2️⃣ Ver Status

```bash
python claude/acciones/motor_status.py
```

Te muestra:

- Motor detectado
- Integraciones activas
- Si están completadas las credenciales

---

## 3️⃣ Completar Credenciales (opcional)

Abrí `credenciales.md` y agregá:

- API keys de Copilot/Claude/Cursor (si usás APIs)
- **CALLMEBOT_PHONE** y **CALLMEBOT_APIKEY** (para WhatsApp)
- Keys de n8n, DBs, etc.

**Importante**: Este archivo NUNCA vai a git (está en `.gitignore`)

---

## 4️⃣ Iniciar Dashboard

```bash
cd claude/dashboard
pip install -r requirements.txt
python app.py
```

Abre: `http://localhost:5000`

**Características:**
- 🔌 Motor activo en vivo (con dropdown para cambiar)
- 📄 Discusiones: borrador → final (evolución visual)
- 📝 Planes en ejecución (% completado)
- ⏱️ Timestamps de cambios
- 🔄 Auto-refresh cada 5 segundos

---

## 5️⃣ Empezar a Trabajar

El flujo es el mismo en TODOS los motores:

```
TÚ:      "Necesito una API que..."
         ↓
MOTOR:   Crea disc_[tema].md
         → "📝 disc_[tema].md — marca 1 cuando hayas leído"
         ↓
TÚ:      Leés, respondés
         
         1 = Re-lee
         R:/ [nota] = Incorpora feedback
         0 = APROBADO ✅
         ↓
MOTOR:   Genera plan_XXX.md
         → Ejecuta todas las tareas
         → Marca [x] al terminar
         → Avisos por cada etapa
```

Lé [FLUJO.md](../FLUJO.md) para detalles.

---

## 📚 Archivos Clave

| Archivo                 | Qué es                                 |
| ----------------------- | -------------------------------------- |
| [MOTOR.md](../MOTOR.md) | Explicación del sistema multi-motor    |
| [FLUJO.md](../FLUJO.md) | El workflow completo                   |
| `credenciales.md`       | API keys centralizadas (en .gitignore) |
| `.motor/motor.json`     | Config del motor activo                |
| `claude/`               | Carpeta de trabajo (en .gitignore)     |

---

## 🔧 Scripts Disponibles

| Script            | Usa                                               |
| ----------------- | ------------------------------------------------- |
| `motor_detect.py` | `python claude/acciones/motor_detect.py`          |
| `motor_status.py` | `python claude/acciones/motor_status.py`          |
| `avisar.py`       | `python cladue/acciones/avisar.py "mensaje" tipo` |

---

## 💡 Ejemplo Completo

```bash
# 1. Setup
python claude/acciones/motor_detect.py
python claude/acciones/motor_status.py

# 2. Completar credenciales.md (si necesitás avisos)
# (editar el archivo)

# 3. Dashboard (opcional)
python claude/dashboard/app.py &

# 4. En el chat de tu IDE:
# "Necesito una función que valide emails en Python"
#
# → Motor crea: disc_validar-emails.md
# Vos respondés: "1" (re-lee) o "0" (aprobado)
#
# → Se genera: plan_XXX.md
# → Se ejecuta todo automático
```

---

## 🤔 Preguntas Frecuentes

**¿Funciona con Copilot y Claude al mismo tiempo?**
No. Motor detecta uno activo y lo usa. Podés cambiar con `motor_switch.py` (próxima versión). r/ no esta mal la idea si cambio para no perder tiempo en crear o asi si paso cambio eso me gustaria que se haga automatico lo dectete siuempre 
r/ la otra que cuadno este en el dashboard pueda uno cambiar eso ya el usaurio sabe que esta hbaciendo eso para enriquecer un poco el dinamismo algo mas bonito si me entieudes tener una carpeta para cada esenario donde funcione claude para cluade code cursor para cursor ya si con cada uno que oponmeas
**¿Y si cambio de IDE (ej: VS Code → Cursor)?**
Ejecutá `motor_detect.py` de nuevo. Se actualiza `.motor/motor.json`. r/ si eso se ejecuta cada vez que incie en consola eso 

**¿Las credenciales se sincronizan entre máquinas?**
No. Cada máquina tiene su `credenciales.md` local. Está en `.gitignore` por seguridad.

**¿Puedo customizar el flujo?**
Sí. Editá `FLUJO.md` o `MOTOR.md` según necesites.

---

## 🚀 Próximas Features

- ✅ `motor_detect.py` — Auto-ejecuta en cada inicio
- ✅ Dashboard con dropdown de motores
- ✅ Carpetas por motor (`motores/claude/`, etc.)
- ✅ Discusiones: borrador/ + final/
- ✅ Planes como memoria de IA
- [ ] Timeline visual con diffs de cambios
- [ ] Auto-refresh historial en dashboard

---

**¿Listo? Empezá:** Abrí tu IDE y describe la primera tarea. Motor hará el resto. 🎯