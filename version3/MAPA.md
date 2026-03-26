# MAPA — ClaudeMachote v3
> Leé esto una vez. Después el sistema se maneja solo.

---

## ¿Qué es esto?

Un sistema de trabajo para Claude Code. Lo copiás a tu proyecto, hacés el setup una vez, y a partir de ahí escribís `claude` como siempre — pero el dashboard abre solo, la sesión se registra sola, las tareas se trackean solas y el costo se calcula solo.

---

## INSTALACIÓN — una sola vez por máquina

### 1. Copiar a tu proyecto

```bash
cp -r version3/. mi-proyecto/
cd mi-proyecto
```

### 2. Instalar dependencias

```bash
pip install flask
npm install -g @anthropic-ai/claude-code   # si no lo tenés
```

### 3. Instalar el alias de claude

```bash
bash claude/acciones/setup_alias.sh
source ~/.bashrc
```

Esto hace que cada vez que escribís `claude` en este proyecto, el dashboard arranque automáticamente antes de que Claude abra.

**Solo se hace una vez por máquina.** En proyectos nuevos no hace falta repetirlo.

---

## USO DIARIO

```bash
claude
```

Eso es todo. El sistema hace el resto.

---

## QUÉ PASA AL ESCRIBIR `claude`

```
claude
  ↓
alias detecta que estás en un proyecto ClaudeMachote
  ↓
iniciar_dashboard.py corre en background:
  ├── cierra sesión anterior si quedó sin cerrar (lee tokens automático)
  ├── arranca Flask en localhost:5001 si no está corriendo
  └── abre el browser (solo la primera vez del día)
  ↓
Claude Code abre en la terminal (al mismo tiempo)
  ↓
Dashboard listo en el browser — trabajás desde ahí
```

Si no hiciste el setup del alias, el hook `UserPromptSubmit` hace lo mismo al primer mensaje que mandás.

---

## EL DASHBOARD — `http://localhost:5001`

### Barra de acciones (arriba)

```
● Esperando acción
[▶ Continuar trabajando]  [💬 Nueva discusión]  [🔔 Avisar]  [⏹ Terminar el día]
```

| Indicador | Significa |
|---|---|
| Azul — Esperando acción | Listo para elegir |
| Verde parpadeando — Claude trabajando... | Claude está activo, botones deshabilitados |
| Naranja — Cerrando sesión... | Registrando y cerrando |

---

### Botones

#### ▶ Continuar trabajando
Claude abre (o ya está abierto) y lee `estado.log` para saber dónde quedó el proyecto. Te presenta el contexto y pregunta si continuamos.

**Cuándo:** Al empezar el día o retomar trabajo interrumpido.

---

#### 💬 Nueva discusión
Aparece un campo. Escribís el tema → Enter. Claude abre listo para analizar esa idea.

```
[nueva pantalla de login con biometría     ] [Abrir Claude] [Cancelar]
```

Claude crea `claude/discusiones/disc_login-biometria.md` con análisis, propuesta y preguntas.

En el chat respondés con:

| Comando | Qué hace Claude |
|---|---|
| `1` | Relee el `.md`, actualiza si hay cambios, te avisa por WhatsApp |
| `R:/ [texto]` | Incorpora tu feedback al `.md` de inmediato |
| `revisa` | Incorpora notas que escribiste vos en el `.md` |
| `0` | **Aprobado** → genera plan y empieza a ejecutar |

**Cuándo:** Cuando tenés una idea, un problema o algo que querés que Claude analice antes de tocar código.

---

#### 🔔 Avisar
Manda sonido + WhatsApp sin abrir Claude.

```
[revisá el deploy cuando puedas     ]  [Suave] [Normal] [Urgente]  [Enviar]
```

| Tipo | Cuándo |
|---|---|
| Suave | Info, recordatorio |
| Normal | Etapa lista, algo para revisar |
| Urgente | Error crítico, atención inmediata |

---

#### ⏹ Terminar el día
Confirma → cierra la sesión automáticamente:
1. Registra la hora de cierre
2. Lee los tokens desde `~/.claude/projects/` (sin que hagas nada)
3. Calcula el costo real (input / cache / output con tarifas reales)
4. Distribuye los tokens entre las tareas proporcionalmente por tiempo
5. Manda aviso "Día de trabajo terminado"
6. Limpia los flags para que mañana el browser vuelva a abrirse

---

### Sección de pruebas

Cuando vas a probar la app o funcionalidad:

**Cronómetro:**
1. Clic en `Iniciar prueba`
2. Probás, anotás errores
3. Clic en `Detener prueba` → opcional: nota de qué probaste

**Manual:**
1. Clic en `+ Ingresar tiempo manual`
2. Escribís los minutos
3. Guardar

El tiempo de pruebas se registra separado — no cuenta como tokens, es tiempo tuyo.

---

### Calculadora de costo

Estimá el costo antes de empezar o compará entre modelos:

```
[Claude Sonnet 4.x] [Opus 4.x] [GPT-4o] [GPT-4o mini] [Gemini 1.5]

Tokens entrada: [150000]    Precio/1M: [3.00 ]
Tokens salida:  [25000 ]    Precio/1M: [15.00]

Resultado:  $0.8250
  Entrada (150k): $0.4500
  Salida   (25k): $0.3750
```

El `?` al lado de los campos explica dónde encontrar esos números.

---

### Historial y resumen

**Historial de sesiones** — cada día de trabajo:
- Proyecto y etapa
- Duración total
- Tokens y costo

**Resumen por proyecto** — acumulado total:
- Cuántas sesiones trabajadas
- Horas totales invertidas
- Tokens y costo acumulado

---

## EL CICLO DE TRABAJO CON CLAUDE

```
Claude programa / ejecuta tareas
        ↓
Vos revisás (las tareas completadas aparecen solas en el dashboard)
        ↓
Vos probás la app o funcionalidad
   → Iniciás cronómetro en el dashboard
   → Probás
   → Detenés cronómetro
        ↓
     ¿Funciona?
    /           \
   SÍ            NO
    ↓              ↓
Siguiente       Contás el error en el chat
tarea           Claude lo analiza y corrige
```

---

## COMANDOS DE CONTROL EN EL CHAT

Estos comandos los escribís directamente en la terminal donde está Claude:

| Comando | Cuándo | Claude hace |
|---|---|---|
| `1` | Después de leer un disc_ | Relee, actualiza si hay cambios, avisa |
| `R:/ [texto]` | En cualquier momento | Para todo, incorpora tu feedback, confirma |
| `revisa` | Después de editar el disc_ | Incorpora tus notas al archivo |
| `0` | Cuando aprobás una discusión | Genera plan y arranca a ejecutar |

`R:/` tiene prioridad absoluta — Claude para lo que está haciendo y lo incorpora.

---

## QUÉ PASA AUTOMÁTICO (sin que hagas nada)

| Momento | Qué pasa |
|---|---|
| Escribís `claude` | Dashboard arranca, sesión registrada, browser abre |
| Claude marca `[x]` en un plan | La tarea se registra con duración en el dashboard |
| Claude escribe cualquier archivo | Se loguea en `claude/escrituras.log` |
| Antes de cada comando Bash | Se verifica que no haya secrets hardcodeados |
| Claude notifica | Suena + manda WhatsApp |
| Terminás el día | Tokens leídos automáticamente, costo calculado |
| Abrís claude al día siguiente | Sesión anterior cerrada automáticamente si quedó abierta |

---

## PRIMER PROYECTO — proyecto virgen

Cuando copiás `version3/` y escribís `claude` por primera vez:

1. Claude lee `claude/estado.log` → ve que está vacío → sabe que es proyecto nuevo
2. Detecta el stack (busca `manage.py`, `vite.config`, `pubspec.yaml`, `.sln`, etc.)
3. Carga el skill correspondiente (patrones de código para tu stack)
4. Propone roadmap completo: Etapas → Sub-etapas → Pasos
5. Esperá, ajustá con `R:/` o aprobá con `0`

---

## ESTRUCTURA DE ARCHIVOS

```
tu-proyecto/
├── CLAUDE.md              ← protocolo de trabajo (Claude lo lee al abrir)
├── STACK.md               ← tus tecnologías preferidas
├── .gitignore             ← claude/ nunca sube a git
├── .claude/
│   ├── settings.json      ← permisos + hooks automáticos
│   └── skills/            ← patrones por tecnología
│       ├── django-drf/
│       ├── react-vite/
│       ├── react-native/
│       ├── flutter/
│       ├── n8n-flows/
│       └── winforms/
└── claude/                ← memoria del proyecto (nunca a git)
    ├── datos.db           ← SQLite: sesiones, tareas, pruebas, tokens
    ├── estado.log         ← dónde está el proyecto ahora
    ├── RESUMEN.md         ← resumen en 5 líneas
    ├── escrituras.log     ← log de archivos modificados
    ├── discusiones/       ← una carpeta por idea discutida
    ├── planes/            ← checklists de ejecución
    ├── backups/n8n/       ← exports de flujos n8n
    ├── backups/sql/       ← dumps de PostgreSQL
    ├── imagenes/errores/  ← screenshots de bugs
    ├── imagenes/mejoras/  ← referencias de UI o diseño
    ├── dashboard/
    │   ├── app.py         ← Flask en localhost:5001
    │   └── templates/index.html
    └── acciones/
        ├── setup_alias.sh      ← INSTALAR UNA VEZ
        ├── tarea.sh            ← lanzador alternativo con selector de acciones
        ├── iniciar_dashboard.py← arranca dashboard + sesión (llamado por alias)
        ├── iniciar_sesion.py   ← registra inicio en SQLite
        ├── cerrar_sesion.py    ← cierra sesión, lee tokens, calcula costo
        ├── avisar.py           ← sonido + WhatsApp
        ├── backup_n8n.py       ← exporta flujos n8n
        ├── backup_sql.py       ← dump PostgreSQL
        ├── check_secrets.py    ← bloquea secrets hardcodeados
        ├── log_escritura.py    ← registra archivos + detecta tareas [x]
        ├── notificar.py        ← hook de notificaciones
        └── credenciales.md     ← credenciales de servicios externos
```

---

## CREDENCIALES

En `claude/acciones/credenciales.md`. Claude verifica que estén antes de usar cualquier servicio externo.

Para WhatsApp (Callmebot):
```markdown
## Callmebot
- PHONE: +59912345678
- API_KEY: 1234567
- Estado: activa
```

---

## SKILLS — conocimiento por stack

Al detectar tu proyecto, Claude carga el skill correspondiente y ya sabe las convenciones, estructura de carpetas y patrones de código sin que tengas que explicarle nada.

| Indicador en el proyecto | Skill que carga |
|---|---|
| `manage.py` + `vite.config` | Django + DRF + React + Vite |
| `manage.py` solo | Django + DRF |
| `pubspec.yaml` | Flutter |
| `app.json` + expo | React Native + Expo |
| `.sln` o `.csproj` | WinForms / C# |
| `docker-compose` + n8n | n8n flows |
| `package.json` + vite | React standalone |

---

## REGLAS QUE CLAUDE NUNCA ROMPE

- No escribe código sin plan generado desde discusión aprobada (`0`)
- No genera plan sin que vos digas `0`
- No hace `git commit` ni `git push` — git lo manejás vos
- No escribe secrets en código ni en `.env`
- No termina etapa sin actualizar `estado.log` y avisar
- No usa credencial sin verificarla en `credenciales.md`
- No borra imágenes de `claude/imagenes/`

---

_ClaudeMachote v3 — dashboard local + tracking automático + costo real_
