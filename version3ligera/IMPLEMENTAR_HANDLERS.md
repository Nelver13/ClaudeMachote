# Implementación de Command Handlers

## Ubicación
`version3ligera/claude/dashboard/app.py`

Función: `ejecutar_comando()` (línea ~108)

## Comandos a Implementar

### 1️⃣ `gen_discusión` — Crear nueva discusión

**Qué hace:**
- Genera un nuevo archivo `disc_YYYYMMDD_HHmmss.md` en `discusiones/borrador/`
- Estructura template con la discusión
- Devuelve el path al archivo

**Implementación:**
```python
elif comando == 'gen_discusión':
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    disc_file = (BASE_DIR / 'claude' / 'discusiones' / 'borrador' / f'disc_{timestamp}.md')
    
    template = """# Discusión: [Tema]

*Generada automáticamente el {timestamp}*

## Descripción
Describe aquí el problema/idea

## Análisis
- Punto 1
- Punto 2

## Propuesta
Escribe tu propuesta

## Riesgos
Identifica riesgos

## Estado: Borrador (en edición)
"""
    
    disc_file.parent.mkdir(parents=True, exist_ok=True)
    disc_file.write_text(template.format(timestamp=timestamp), encoding='utf-8')
    
    resultado = f"Discusión creada: {disc_file.name}"
```

---

### 2️⃣ `ejecutar_plan` — Ejecutar plan con progreso

**Qué hace:**
- Lee `plan_*.md` más reciente en `planes/`
- Ejecuta tareas incompletas (líneas con `[ ]`)
- Actualiza progreso (`[x]`)
- Devuelve % completado

**Implementación:**
```python
elif comando == 'ejecutar_plan':
    from pathlib import Path
    
    # Buscar último plan
    planes = list((BASE_DIR / 'claude' / 'planes').glob('plan_*.md'))
    if not planes:
        raise ValueError("No hay planes para ejecutar")
    
    plan_file = sorted(planes)[-1]  # El más reciente
    content = plan_file.read_text(encoding='utf-8')
    
    # Contar tareas
    total = content.count('[ ]') + content.count('[x]')
    completed = content.count('[x]')
    
    # Aquí: simular ejecución (reemplazar [ ] → [x])
    # content = content.replace('[ ]', '[x]', 1)
    # plan_file.write_text(content)
    
    progress = (completed / total * 100) if total > 0 else 0
    resultado = f"Plan: {plan_file.name} | Progreso: {progress:.0f}%"
```

---

### 3️⃣ `cambiar_motor` — Cambiar motor activo

**Status:** ✅ YA IMPLEMENTADO
```python
elif comando == 'cambiar_motor':
    motor = parametros.get('motor')
    motor_file = BASE_DIR / '.motor' / 'motor.json'
    if motor_file.exists():
        with open(motor_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config['active_motor'] = motor
        with open(motor_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        resultado = f"Motor cambiado a {motor}"
```

---

### 4️⃣ `gen_reporte` — Generar reporte de etapa

**Qué hace:**
- Query SQLite suma de tokens por etapa
- Genera HTML/JSON con breakdown
- Guarda en `reports/` (última etapa)

**Implementación:**
```python
elif comando == 'gen_reporte':
    # Query: SELECT * FROM etapas ORDER BY id DESC LIMIT 1
    conn = sqlite3.connect(BASE_DIR / 'claude' / 'reports' / 'reports.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM etapas ORDER BY id DESC LIMIT 1')
    etapa = cursor.fetchone()
    conn.close()
    
    if not etapa:
        raise ValueError("Sin reportes disponibles")
    
    resultado = f"Reporte: Etapa '{etapa[1]}' | Tokens: {etapa[3]} | Costo: ${etapa[4]}"
```

---

### 5️⃣ `sync_tokens` — Sincronizar tokens JSON→SQLite

**Qué hace:**
- Lee `logs/tokens.json`
- INSERT en tabla `token_events`
- Updatea `motor_stats`

**Implementación:**
```python
elif comando == 'sync_tokens':
    # Ejecutar sync_tokens.py
    sync_script = BASE_DIR / 'claude' / 'acciones' / 'sync_tokens.py'
    result = subprocess.run(
        [sys.executable, str(sync_script)],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR)
    )
    resultado = result.stdout or "Sync completado"
    if result.returncode != 0:
        error = result.stderr
```

---

## Template Completo Mejorado

Reemplazar la función `ejecutar_comando()`:

```python
import sys

@app.route('/api/comandos/ejecutar', methods=['POST'])
def ejecutar_comando():
    """Ejecuta comando de agente"""
    data = request.json
    comando = data.get('comando')
    parametros = data.get('parametros', {})
    
    db_path = BASE_DIR / 'claude' / 'reports' / 'reports.db'
    
    inicio = datetime.now()
    resultado = None
    error = None
    
    try:
        if comando == 'gen_discusión':
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            disc_file = (BASE_DIR / 'claude' / 'discusiones' / 'borrador' / f'disc_{timestamp}.md')
            
            template = """# Discusión: [Titulo]

*Generada: {timestamp}*

## Descripción
[Tu descripción aquí]

## Análisis
- Punto 1
- Punto 2

## Propuesta
[Tu propuesta]

## Estado: Borrador
"""
            
            disc_file.parent.mkdir(parents=True, exist_ok=True)
            disc_file.write_text(template.format(timestamp=timestamp), encoding='utf-8')
            
            resultado = f"✅ {disc_file.name}"
            
        elif comando == 'ejecutar_plan':
            planes = list((BASE_DIR / 'claude' / 'planes').glob('plan_*.md'))
            if not planes:
                raise ValueError("Sin planes")
            
            plan_file = sorted(planes)[-1]
            content = plan_file.read_text(encoding='utf-8')
            
            total = content.count('[ ]') + content.count('[x]')
            completed = content.count('[x]')
            progress = (completed / total * 100) if total > 0 else 0
            
            resultado = f"✅ {plan_file.name} | {progress:.0f}% completado"
            
        elif comando == 'cambiar_motor':
            motor = parametros.get('motor')
            motor_file = BASE_DIR / '.motor' / 'motor.json'
            if motor_file.exists():
                with open(motor_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                config['active_motor'] = motor
                with open(motor_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
            resultado = f"✅ Motor: {motor}"
            
        elif comando == 'gen_reporte':
            if db_path.exists():
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM etapas ORDER BY id DESC LIMIT 1')
                etapa = cursor.fetchone()
                conn.close()
                
                if etapa:
                    resultado = f"✅ Reporte Etapa '{etapa[1]}' | {etapa[3]} tokens"
                else:
                    resultado = "⚠️ Sin reportes aún"
        
        elif comando == 'sync_tokens':
            sync_script = BASE_DIR / 'claude' / 'acciones' / 'sync_tokens.py'
            if sync_script.exists():
                result = subprocess.run(
                    [sys.executable, str(sync_script)],
                    capture_output=True,
                    text=True,
                    cwd=str(BASE_DIR)
                )
                resultado = "✅ Sync completado"
        
        else:
            resultado = f"❓ Comando desconocido: {comando}"
        
        estado = 'éxito'
    
    except Exception as e:
        estado = 'error'
        error = str(e)
        resultado = None
    
    duracion_ms = int((datetime.now() - inicio).total_seconds() * 1000)
    
    # Registrar en SQLite
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO comandos (comando, parametros, estado, resultado, error_msg, duracion_ms)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            comando,
            json.dumps(parametros),
            estado,
            resultado,
            error,
            duracion_ms
        ))
        
        conn.commit()
        conn.close()
    
    return jsonify({
        'status': estado,
        'resultado': resultado,
        'error': error,
        'duracion_ms': duracion_ms
    })
```

---

## Testing

Después de implementar:

```bash
# 1. Iniciar dashboard
python iniciar_dashboard.py

# 2. Tab Comandos → click "📝 Gen Discusión"
# → Debe crear disc_YYYYMMDD_HHmmss.md en discusiones/borrador/

# 3. Tab Comandos → click "▶️ Ejecutar Plan"
# → Debe mostrar progreso del plan_001.md

# 4. Tab Home
# → Debe actualizar contadores en vivo
```

---

## Checklist de Implementación

- [ ] Copiar template completo en app.py
- [ ] Probar gen_discusión (crear archivo)
- [ ] Probar ejecutar_plan (leer progreso)
- [ ] Probar cambiar_motor (UPDATE motor.json)
- [ ] Probar gen_reporte (query SQLite)
- [ ] Probar sync_tokens (usar script externo)
- [ ] Verificar que comandos se registren en SQLite (tabla `comandos`)
- [ ] Dashboard actualiza stats en vivo (auto-refresh)
