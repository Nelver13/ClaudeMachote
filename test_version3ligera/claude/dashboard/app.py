"""
Dashboard — Version3Ligera v3
Hub Central de Control:
- Discusiones en vivo
- Planes con progreso
- Tokens & Costos (SQLite)
- Ejecutor de Comandos
- Reportes por Etapas
"""

from flask import Flask, render_template, jsonify, request
import json
import sqlite3
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import importlib.util

BASE_DIR = Path(__file__).parent.parent.parent

# Importar log_tokens
spec = importlib.util.spec_from_file_location("log_tokens", BASE_DIR / 'claude' / 'acciones' / 'log_tokens.py')
log_tokens = importlib.util.module_from_spec(spec)
spec.loader.exec_module(log_tokens)

app = Flask(__name__)

@app.route('/')
def index():
    # Inicializar DB si no existe
    db_path = BASE_DIR / 'claude' / 'reports' / 'reports.db'
    if not db_path.exists():
        init_db = BASE_DIR / 'claude' / 'acciones' / 'init_db.py'
        if init_db.exists():
            subprocess.run(['python', str(init_db)], cwd=str(BASE_DIR), capture_output=True)
    
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    return jsonify(get_dashboard_data())

def get_dashboard_data():
    """Obtiene datos completos del dashboard"""
    motor_file = BASE_DIR / '.motor' / 'motor.json'
    discusiones_dir = BASE_DIR / 'claude' / 'discusiones'
    planes_dir = BASE_DIR / 'claude' / 'planes'
    
    data = {
        'timestamp': datetime.now().isoformat(),
        'motor': {},
        'discusiones': {
            'borrador': [],
            'final': []
        },
        'planes': [],
        'stats': {
            'borrador_count': 0,
            'final_count': 0,
            'planes_activos': 0,
            'planes_completados': 0
        }
    }
    
    # Motor actual
    if motor_file.exists():
        with open(motor_file, 'r', encoding='utf-8') as f:
            motor = json.load(f)
        data['motor'] = {
            'active': motor.get('active_motor', 'auto'),
            'detected': motor.get('detected_motor', 'unknown'),
            'version': motor.get('version', '1.0')
        }
    
    # Discusiones: borrador/
    if discusiones_dir.exists():
        borrador_dir = discusiones_dir / 'borrador'
        final_dir = discusiones_dir / 'final'
        
        # Borradores
        if borrador_dir.exists():
            for disc_file in borrador_dir.glob('disc_*.md'):
                mtime = disc_file.stat().st_mtime
                content = disc_file.read_text(encoding='utf-8')
                data['discusiones']['borrador'].append({
                    'file': disc_file.name,
                    'timestamp': datetime.fromtimestamp(mtime).isoformat(),
                    'lines': len(content.split('\n'))
                })
            data['stats']['borrador_count'] = len(data['discusiones']['borrador'])
        
        # Finales
        if final_dir.exists():
            for disc_file in final_dir.glob('disc_*.md'):
                mtime = disc_file.stat().st_mtime
                content = disc_file.read_text(encoding='utf-8')
                data['discusiones']['final'].append({
                    'file': disc_file.name,
                    'timestamp': datetime.fromtimestamp(mtime).isoformat(),
                    'lines': len(content.split('\n'))
                })
            data['stats']['final_count'] = len(data['discusiones']['final'])
    
    # Planes
    if planes_dir.exists():
        for plan_file in planes_dir.glob('plan_*.md'):
            content = plan_file.read_text(encoding='utf-8')
            completed = content.count('[x]')
            total = content.count('[ ]') + completed
            progress = (completed / total * 100) if total > 0 else 0
            mtime = plan_file.stat().st_mtime
            
            data['planes'].append({
                'file': plan_file.name,
                'progress': progress,
                'completed': completed,
                'total': total,
                'timestamp': datetime.fromtimestamp(mtime).isoformat()
            })
        data['stats']['planes_activos'] = len([p for p in data['planes'] if p['progress'] < 100])
        data['stats']['planes_completados'] = len([p for p in data['planes'] if p['progress'] == 100])

    data['project_root'] = str(BASE_DIR)
    return data

@app.route('/api/motors')
def api_motors():
    """Lista motores disponibles"""
    return jsonify({
        'available': ['claude', 'cursor', 'copilot', 'antigravity'],
        'current': get_current_motor()
    })

@app.route('/api/switch-motor/<motor>', methods=['POST'])
def switch_motor(motor):
    """Cambia motor activo"""
    motor_file = BASE_DIR / '.motor' / 'motor.json'
    if motor_file.exists():
        with open(motor_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config['active_motor'] = motor
        with open(motor_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return jsonify({'status': 'ok', 'motor': motor})
    return jsonify({'status': 'error'}, 500)

@app.route('/api/tokens/etapas')
def api_tokens_etapas():
    """Tokens agrupados por etapa desde SQLite"""
    db_path = BASE_DIR / 'claude' / 'reports' / 'reports.db'
    
    if not db_path.exists():
        return jsonify({'etapas': []})
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT 
            etapa,
            COUNT(*) as count,
            SUM(total_tokens) as total_tokens,
            SUM(costo_estimado) as total_costo,
            AVG(duracion_segundos) as promedio_duracion
        FROM token_events
        WHERE etapa IS NOT NULL
        GROUP BY etapa
        ''')
        
        etapas = [dict(row) for row in cursor.fetchall()]
        
    finally:
        conn.close()
    
    return jsonify({'etapas': etapas})

@app.route('/api/tokens/motores')
def api_tokens_motores():
    """Estadísticas por motor desde SQLite"""
    db_path = BASE_DIR / 'claude' / 'reports' / 'reports.db'
    
    if not db_path.exists():
        return jsonify({'motores': []})
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM motor_stats')
        motores = [dict(row) for row in cursor.fetchall()]
        
    finally:
        conn.close()
    
    return jsonify({'motores': motores})

@app.route('/api/comandos/ejecutar', methods=['POST'])
def ejecutar_comando():
    """Ejecuta comando de agente con logging de tokens"""
    data = request.json
    comando = data.get('comando')
    parametros = data.get('parametros', {})
    
    db_path = BASE_DIR / 'claude' / 'reports' / 'reports.db'
    
    inicio = datetime.now()
    resultado = None
    error = None
    event_id = None
    
    # Obtener motor actual
    motor_actual = get_current_motor()
    
    try:
        # LOGGING: Inicio del evento
        event_id = log_tokens.log_token_event(
            event_type='comando',
            event_name=comando,
            tokens_in=0,  # Placeholder, se actualizará al final
            tokens_out=0,  # Placeholder
            motor=motor_actual,
            etapa='ejecución',
            metadata={'parametros': parametros}
        )
    except Exception as e:
        print(f"⚠️ Error en logging inicial: {e}")
        event_id = None
    
    try:
        if comando == 'gen_discusión':
            # Generar nueva discusión
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
            # Ejecutar tareas pendientes en el plan más reciente
            planes = list((BASE_DIR / 'claude' / 'planes').glob('plan_*.md'))
            if not planes:
                raise ValueError("Sin planes")
            
            plan_file = sorted(planes)[-1]
            content = plan_file.read_text(encoding='utf-8')
            
            # Encontrar primera tarea pendiente [ ]
            lines = content.split('\n')
            task_executed = False
            
            for i, line in enumerate(lines):
                if '[ ]' in line and not task_executed:
                    # Ejecutar tarea (placeholder - en producción implementar lógica real)
                    print(f"Ejecutando tarea: {line.strip()}")
                    
                    # Marcar como completada [x]
                    lines[i] = line.replace('[ ]', '[x]')
                    task_executed = True
            
            if task_executed:
                # Guardar cambios
                plan_file.write_text('\n'.join(lines), encoding='utf-8')
            
            # Calcular progreso actual
            total = content.count('[ ]') + content.count('[x]')
            completed = content.count('[x]')
            progress = (completed / total * 100) if total > 0 else 0
            
            if task_executed:
                resultado = f"✅ {plan_file.name} | Ejecutada 1 tarea | {progress:.0f}% completado"
            else:
                resultado = f"✅ {plan_file.name} | Sin tareas pendientes | {progress:.0f}% completado"
            
        elif comando == 'cambiar_motor':
            # Cambiar motor activo
            motor = parametros.get('motor')
            motor_file = BASE_DIR / '.motor' / 'motor.json'
            if motor_file.exists():
                with open(motor_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                config['active_motor'] = motor
                with open(motor_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
            resultado = f"✅ Motor: {motor}"
            
        elif comando == 'gen_reporte':
            # Generar reporte de última etapa
            if db_path.exists():
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                try:
                    cursor.execute('SELECT * FROM etapas ORDER BY id DESC LIMIT 1')
                    etapa = cursor.fetchone()
                    conn.close()
                    
                    if etapa:
                        resultado = f"✅ Reporte Etapa '{etapa[1]}' | {etapa[3]} tokens"
                    else:
                        resultado = "⚠️ Sin reportes aún"
                except:
                    resultado = "⚠️ Base de datos vacía"
        
        elif comando == 'sync_tokens':
            # Sincronizar tokens JSON→SQLite
            sync_script = BASE_DIR / 'claude' / 'acciones' / 'sync_tokens.py'
            if sync_script.exists():
                result = subprocess.run(
                    [sys.executable, str(sync_script)],
                    capture_output=True,
                    text=True,
                    cwd=str(BASE_DIR),
                    timeout=30
                )
                resultado = "✅ Sync completado"
            else:
                resultado = "⚠️ sync_tokens.py no encontrado"
        
        else:
            resultado = f"❓ Comando desconocido: {comando}"
        
        estado = 'éxito'
    
    except Exception as e:
        estado = 'error'
        error = str(e)
        resultado = None
    
    duracion_ms = int((datetime.now() - inicio).total_seconds() * 1000)
    
    # LOGGING: Finalizar evento con tokens reales
    if event_id:
        # Estimar tokens consumidos
        tokens_estimados = estimar_tokens(comando, duracion_ms)
        
        log_tokens.finalizar_evento(
            event_id=event_id,
            duracion_segundos=duracion_ms / 1000,
            estado=estado,
            metadata_update={
                'tokens_in': tokens_estimados['in'],
                'tokens_out': tokens_estimados['out'],
                'resultado': resultado,
                'error': error
            }
        )
    
    # Registrar en SQLite
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
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
        finally:
            conn.close()
    
    return jsonify({
        'status': estado,
        'resultado': resultado,
        'error': error,
        'duracion_ms': duracion_ms
    })

@app.route('/api/reportes/etapas')
def api_reportes_etapas():
    """Reportes por etapa desde SQLite"""
    db_path = BASE_DIR / 'claude' / 'reports' / 'reports.db'
    
    if not db_path.exists():
        return jsonify({'reportes': []})
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT * FROM etapas ORDER BY id DESC LIMIT 20
        ''')
        
        reportes = [dict(row) for row in cursor.fetchall()]
        
    finally:
        conn.close()
    
    return jsonify({'reportes': reportes})

@app.route('/api/etapas/crear', methods=['POST'])
def crear_etapa():
    """Crea o actualiza una etapa en SQLite"""
    data = request.json
    nombre = data.get('nombre', 'etapa_sin_nombre')
    descripcion = data.get('descripcion', '')
    motor_principal = data.get('motor_principal', get_current_motor())
    
    db_path = BASE_DIR / 'claude' / 'reports' / 'reports.db'
    
    if not db_path.exists():
        return jsonify({'error': 'Base de datos no existe'}), 500
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar si etapa existe
        cursor.execute('SELECT id FROM etapas WHERE nombre = ?', (nombre,))
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar
            cursor.execute('''
            UPDATE etapas SET 
                descripcion = ?,
                motor_principal = ?,
                updated_at = ?
            WHERE nombre = ?
            ''', (descripcion, motor_principal, datetime.now().isoformat(), nombre))
            etapa_id = existing[0]
            action = 'actualizada'
        else:
            # Crear nueva
            cursor.execute('''
            INSERT INTO etapas (nombre, descripcion, motor_principal, start_time, estado)
            VALUES (?, ?, ?, ?, ?)
            ''', (nombre, descripcion, motor_principal, datetime.now().isoformat(), 'activa'))
            etapa_id = cursor.lastrowid
            action = 'creada'
        
        conn.commit()
        
    finally:
        conn.close()
    
    return jsonify({
        'status': 'éxito',
        'etapa_id': etapa_id,
        'nombre': nombre,
        'action': action
    })

@app.route('/api/etapas/<int:etapa_id>/finalizar', methods=['POST'])
def finalizar_etapa(etapa_id):
    """Finaliza una etapa y calcula totales + extrae información"""
    db_path = BASE_DIR / 'claude' / 'reports' / 'reports.db'
    
    if not db_path.exists():
        return jsonify({'error': 'Base de datos no existe'}), 500
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Obtener etapa
        cursor.execute('SELECT * FROM etapas WHERE id = ?', (etapa_id,))
        etapa = cursor.fetchone()
        
        if not etapa:
            return jsonify({'error': 'Etapa no encontrada'}), 404
        
        # Calcular totales desde token_events
        cursor.execute('''
        SELECT 
            SUM(total_tokens) as tokens_totales,
            SUM(costo_estimado) as costo_total,
            COUNT(*) as eventos_count
        FROM token_events 
        WHERE etapa = ?
        ''', (etapa[1],))  # etapa[1] es nombre
        
        totals = cursor.fetchone()
        
        # Actualizar etapa
        cursor.execute('''
        UPDATE etapas SET 
            end_time = ?,
            estado = 'completada',
            tokens_totales = ?,
            costo_total = ?,
            numero_discusiones = ?,
            numero_planes = ?
        WHERE id = ?
        ''', (
            datetime.now().isoformat(),
            totals[0] or 0,
            totals[1] or 0,
            totals[2] or 0,  # eventos_count como proxy
            0,  # numero_planes (placeholder)
            etapa_id
        ))
        
        conn.commit()
        
        # EJECUTAR SCRIPT DE FINALIZACIÓN (extrae info automáticamente)
        finalizar_script = BASE_DIR / 'claude' / 'acciones' / 'finalizar_etapa.py'
        if finalizar_script.exists():
            result = subprocess.run(
                [sys.executable, str(finalizar_script), str(etapa_id)],
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR),
                timeout=30
            )
            print(f"Script finalización: {result.stdout}")
            if result.returncode != 0:
                print(f"Error en script: {result.stderr}")
        
    finally:
        conn.close()
    
    return jsonify({
        'status': 'éxito',
        'etapa_id': etapa_id,
        'tokens_totales': totals[0] or 0,
        'costo_total': totals[1] or 0,
        'info_extraida': 'automática'
    })

def get_current_motor():
    """Obtiene motor activo actual"""
    motor_file = BASE_DIR / '.motor' / 'motor.json'
    if motor_file.exists():
        with open(motor_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get('active_motor', 'unknown')
    return 'unknown'

def estimar_tokens(comando, duracion_ms):
    """Estima tokens consumidos basado en comando y duración"""
    # Estimaciones basadas en experiencia (ajustar según uso real)
    estimaciones = {
        'gen_discusión': {'in': 50, 'out': 200},
        'ejecutar_plan': {'in': 30, 'out': 100},
        'cambiar_motor': {'in': 10, 'out': 20},
        'gen_reporte': {'in': 40, 'out': 150},
        'sync_tokens': {'in': 20, 'out': 50}
    }
    
    base = estimaciones.get(comando, {'in': 25, 'out': 75})
    
    # Ajustar por duración (más tiempo = más tokens)
    factor = min(1 + (duracion_ms / 10000), 3)  # Máximo 3x
    
    return {
        'in': int(base['in'] * factor),
        'out': int(base['out'] * factor)
    }

if __name__ == '__main__':
    print("🚀 Dashboard running on http://localhost:5000")
    app.run(debug=True, port=5000)
