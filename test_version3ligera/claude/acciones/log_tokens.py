#!/usr/bin/env python3
"""
Log Tokens — Registra automáticamente tokens consumidos
Ejecuta: Al final de cada discusión/plan generado

Registra:
- Tokens entrada/salida
- Motor usado
- Etapa (discusión, plan, ejecución)
- Timestamps
- Metadata (versión, iteraciones, etc)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import hashlib

def log_token_event(event_type, event_name, tokens_in, tokens_out, motor, etapa, metadata=None):
    """
    Registra un evento de tokens
    
    Args:
        event_type: "discusión" | "plan" | "ejecución"
        event_name: "disc_api_v1.md" | "plan_001.md"
        tokens_in: int
        tokens_out: int
        motor: "claude" | "cursor" | "copilot" | "antigravity"
        etapa: "discusión" | "ejecución"
        metadata: dict opcional
    """
    
    base_dir = Path(__file__).parent.parent.parent
    logs_dir = base_dir / 'claude' / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    tokens_file = logs_dir / 'tokens.json'
    
    # Total tokens
    total_tokens = tokens_in + tokens_out
    
    # Calcular costo (valores por defecto, pueden customizarse)
    costo = calcular_costo(motor, tokens_in, tokens_out)
    
    # Generar ID único
    event_id = hashlib.md5(f"{event_name}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
    
    # Crear registro
    registro = {
        "id": event_id,
        "tipo": event_type,
        "nombre": event_name,
        "motor": motor,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "total_tokens": total_tokens,
        "costo_estimado": costo,
        "fecha_inicio": datetime.now().isoformat() + "Z",
        "fecha_fin": None,
        "duracion_segundos": None,
        "etapa": etapa,
        "estado": "en_progreso",
        "metadata": metadata or {}
    }
    
    # Cargar JSON existente
    if tokens_file.exists():
        with open(tokens_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"registros": [], "resumen": {}}
    
    # Agregar registro
    data['registros'].append(registro)
    
    # Actualizar resumen
    actualizar_resumen(data)
    
    # Guardar
    with open(tokens_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Tokens registrados: {event_name}")
    print(f"   Tokens: {tokens_in} → {tokens_out} (total: {total_tokens})")
    print(f"   Costo: ${costo:.4f}")
    
    return event_id

def finalizar_evento(event_id, duracion_segundos, estado="completado", metadata_update=None):
    """Marca evento como completado"""
    base_dir = Path(__file__).parent.parent.parent
    tokens_file = base_dir / 'claude' / 'logs' / 'tokens.json'
    
    if not tokens_file.exists():
        return
    
    with open(tokens_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Buscar evento
    for registro in data['registros']:
        if registro['id'] == event_id:
            registro['fecha_fin'] = datetime.now().isoformat() + "Z"
            registro['duracion_segundos'] = duracion_segundos
            registro['estado'] = estado
            if metadata_update:
                registro['metadata'].update(metadata_update)
            break
    
    # Actualizar resumen
    actualizar_resumen(data)
    
    with open(tokens_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def calcular_costo(motor, tokens_in, tokens_out):
    """Calcula costo estimado según motor y tokens"""
    
    # Precios por defecto (OpenAI 2026)
    precios = {
        'claude': {'input': 0.0005, 'output': 0.0015},
        'copilot': {'input': 0, 'output': 0},
        'cursor': {'input': 0, 'output': 0},
        'antigravity': {'input': 0.001, 'output': 0.001},
    }
    
    # Intentar cargar desde credenciales.md
    base_dir = Path(__file__).parent.parent.parent
    cred_file = base_dir / 'credenciales.md'
    if cred_file.exists():
        content = cred_file.read_text(encoding='utf-8')
        # TODO: parser de credenciales
    
    precio = precios.get(motor, {'input': 0.001, 'output': 0.001})
    
    costo_in = (tokens_in / 1000) * precio['input']
    costo_out = (tokens_out / 1000) * precio['output']
    
    return round(costo_in + costo_out, 6)

def actualizar_resumen(data):
    """Recalcula resumen de tokens y costos"""
    registros = data['registros']
    
    total_tokens = sum(r['total_tokens'] for r in registros)
    total_costo = sum(r['costo_estimado'] for r in registros)
    
    tokens_por_motor = {}
    tokens_por_etapa = {}
    tiempo_total = 0
    
    for r in registros:
        motor = r['motor']
        tokens_por_motor[motor] = tokens_por_motor.get(motor, 0) + r['total_tokens']
        
        etapa = r['etapa']
        tokens_por_etapa[etapa] = tokens_por_etapa.get(etapa, 0) + r['total_tokens']
        
        if r['duracion_segundos']:
            tiempo_total += r['duracion_segundos']
    
    data['resumen'] = {
        'total_tokens': total_tokens,
        'total_costo': round(total_costo, 4),
        'tokens_por_motor': tokens_por_motor,
        'tokens_por_etapa': tokens_por_etapa,
        'tiempo_total_segundos': tiempo_total,
        'registros_activos': len([r for r in registros if r['estado'] == 'en_progreso']),
        'registros_completados': len([r for r in registros if r['estado'] == 'completado'])
    }

# Ejemplo de uso
if __name__ == '__main__':
    # Simular: discusión generada
    event_id = log_token_event(
        event_type='discusión',
        event_name='disc_api_rest_v1.md',
        tokens_in=450,
        tokens_out=1200,
        motor='claude',
        etapa='discusión',
        metadata={
            'version': 'v1',
            'feedback_iteraciones': 0,
            'lineas_generadas': 45
        }
    )
    
    print(f"\nEvento registrado con ID: {event_id}")