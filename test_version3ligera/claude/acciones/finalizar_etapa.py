#!/usr/bin/env python3
"""
Script de Finalización de Etapa
Ejecuta automáticamente al finalizar una etapa:
- Lee documentación generada (discusiones, planes)
- Extrae métricas e información clave
- Registra en SQLite como variables
- Evita que la IA consuma tokens en análisis manual
"""

import json
import re
from pathlib import Path
from datetime import datetime
import sqlite3

def extraer_info_discusion(filepath):
    """Extrae información clave de una discusión"""
    try:
        content = Path(filepath).read_text(encoding='utf-8')
        
        info = {
            'titulo': '',
            'lineas_totales': len(content.split('\n')),
            'secciones': [],
            'palabras_clave': [],
            'estado': 'borrador'
        }
        
        # Extraer título
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            info['titulo'] = title_match.group(1).strip()
        
        # Extraer secciones
        section_matches = re.findall(r'^## (.+)$', content, re.MULTILINE)
        info['secciones'] = section_matches
        
        # Estado
        if 'Estado: Final' in content or 'final/' in str(filepath):
            info['estado'] = 'final'
        
        # Palabras clave (búsqueda simple)
        keywords = ['API', 'database', 'frontend', 'backend', 'seguridad', 'testing']
        for keyword in keywords:
            if keyword.lower() in content.lower():
                info['palabras_clave'].append(keyword)
        
        return info
        
    except Exception as e:
        return {'error': str(e)}

def extraer_info_plan(filepath):
    """Extrae información clave de un plan"""
    try:
        content = Path(filepath).read_text(encoding='utf-8')
        
        info = {
            'titulo': '',
            'tareas_totales': 0,
            'tareas_completadas': 0,
            'progreso': 0,
            'etapas': []
        }
        
        # Extraer título
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            info['titulo'] = title_match.group(1).strip()
        
        # Contar tareas
        info['tareas_totales'] = content.count('[ ]') + content.count('[x]')
        info['tareas_completadas'] = content.count('[x]')
        
        if info['tareas_totales'] > 0:
            info['progreso'] = (info['tareas_completadas'] / info['tareas_totales']) * 100
        
        # Extraer etapas del plan
        lines = content.split('\n')
        current_section = None
        for line in lines:
            if line.startswith('## '):
                current_section = line[3:].strip()
            elif line.startswith('- [') and current_section:
                info['etapas'].append({
                    'seccion': current_section,
                    'tarea': line[6:].strip(),
                    'completada': '[x]' in line
                })
        
        return info
        
    except Exception as e:
        return {'error': str(e)}

def calcular_metricas_etapa(etapa_nombre):
    """Calcula métricas generales de la etapa"""
    base_dir = Path(__file__).parent.parent.parent
    
    metricas = {
        'discusiones_generadas': 0,
        'planes_creados': 0,
        'archivos_totales': 0,
        'lineas_codigo': 0,
        'tiempo_estimado': 0
    }
    
    # Contar discusiones
    disc_dir = base_dir / 'claude' / 'discusiones'
    if disc_dir.exists():
        borrador = len(list(disc_dir.glob('borrador/disc_*.md')))
        final = len(list(disc_dir.glob('final/disc_*.md')))
        metricas['discusiones_generadas'] = borrador + final
    
    # Contar planes
    planes_dir = base_dir / 'claude' / 'planes'
    if planes_dir.exists():
        metricas['planes_creados'] = len(list(planes_dir.glob('plan_*.md')))
    
    # Estimar tiempo (basado en archivos)
    metricas['tiempo_estimado'] = metricas['discusiones_generadas'] * 5 + metricas['planes_creados'] * 10  # minutos
    
    return metricas

def registrar_info_etapa(etapa_id, info_extraida):
    """Registra la información extraída en SQLite"""
    base_dir = Path(__file__).parent.parent.parent
    db_path = base_dir / 'claude' / 'reports' / 'reports.db'
    
    if not db_path.exists():
        print("❌ Base de datos no existe")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Actualizar etapa con información extraída
        cursor.execute('''
        UPDATE etapas SET 
            info_extraida = ?,
            metricas_calculadas = ?,
            updated_at = ?
        WHERE id = ?
        ''', (
            json.dumps(info_extraida, ensure_ascii=False),
            json.dumps(calcular_metricas_etapa(''), ensure_ascii=False),
            datetime.now().isoformat(),
            etapa_id
        ))
        
        conn.commit()
        print(f"✅ Información registrada para etapa {etapa_id}")
        
    except Exception as e:
        print(f"❌ Error registrando: {e}")
    
    finally:
        conn.close()

def main(etapa_id=None):
    """Función principal - ejecuta al finalizar etapa"""
    base_dir = Path(__file__).parent.parent.parent
    
    print("🔍 Extrayendo información de etapa finalizada...")
    
    # Si no se especifica etapa_id, usar la más reciente
    if not etapa_id:
        db_path = base_dir / 'claude' / 'reports' / 'reports.db'
        if db_path.exists():
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM etapas ORDER BY id DESC LIMIT 1')
            row = cursor.fetchone()
            conn.close()
            if row:
                etapa_id = row[0]
    
    if not etapa_id:
        print("❌ No se encontró etapa para procesar")
        return
    
    print(f"📋 Procesando etapa ID: {etapa_id}")
    
    # Extraer información de archivos recientes
    info_extraida = {
        'timestamp': datetime.now().isoformat(),
        'discusiones': [],
        'planes': [],
        'metricas': {}
    }
    
    # Procesar discusiones recientes
    disc_dir = base_dir / 'claude' / 'discusiones'
    if disc_dir.exists():
        for disc_file in disc_dir.glob('**/disc_*.md'):
            if disc_file.stat().st_mtime > (datetime.now().timestamp() - 3600):  # Última hora
                info = extraer_info_discusion(disc_file)
                info['archivo'] = str(disc_file.relative_to(base_dir))
                info_extraida['discusiones'].append(info)
    
    # Procesar planes recientes
    planes_dir = base_dir / 'claude' / 'planes'
    if planes_dir.exists():
        for plan_file in planes_dir.glob('plan_*.md'):
            if plan_file.stat().st_mtime > (datetime.now().timestamp() - 3600):  # Última hora
                info = extraer_info_plan(plan_file)
                info['archivo'] = str(plan_file.relative_to(base_dir))
                info_extraida['planes'].append(info)
    
    # Calcular métricas generales
    info_extraida['metricas'] = calcular_metricas_etapa('')
    
    # Registrar en base de datos
    registrar_info_etapa(etapa_id, info_extraida)
    
    print("✅ Extracción completada")
    print(f"   Discusiones procesadas: {len(info_extraida['discusiones'])}")
    print(f"   Planes procesados: {len(info_extraida['planes'])}")
    print(f"   Métricas calculadas: {len(info_extraida['metricas'])}")

if __name__ == '__main__':
    import sys
    etapa_id = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(etapa_id)