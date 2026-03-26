#!/usr/bin/env python3
"""
Init DB — Inicializa SQLite con schema para reportes y auditoría
Ejecutar una sola vez: python init_db.py
"""

import sqlite3
from pathlib import Path
from datetime import datetime

def init_database():
    """Crea tablas en SQLite"""
    
    base_dir = Path(__file__).parent.parent.parent
    db_path = base_dir / 'claude' / 'reports' / 'reports.db'
    
    # Crear directorio si no existe
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabla: token_events
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS token_events (
        id TEXT PRIMARY KEY,
        tipo TEXT NOT NULL,           -- 'discusión', 'plan', 'ejecución'
        nombre TEXT NOT NULL,
        motor TEXT NOT NULL,          -- 'claude', 'cursor', 'copilot', 'antigravity'
        tokens_in INTEGER,
        tokens_out INTEGER,
        total_tokens INTEGER,
        costo_estimado REAL,
        fecha_inicio TIMESTAMP,
        fecha_fin TIMESTAMP,
        duracion_segundos INTEGER,
        etapa TEXT,                   -- 'discusión', 'ejecución'
        estado TEXT,                  -- 'en_progreso', 'completado', 'error'
        version TEXT,
        iteraciones INTEGER DEFAULT 0,
        lineas_generadas INTEGER,
        feedback_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabla: etapas (snapshots de progreso)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS etapas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,         -- "Etapa 01: Análisis"
        estado TEXT,                  -- 'activa', 'completada', 'pausada'
        tokens_totales INTEGER DEFAULT 0,
        costo_total REAL DEFAULT 0,
        fecha_inicio TIMESTAMP,
        fecha_fin TIMESTAMP,
        duracion_segundos INTEGER,
        motor_principal TEXT,
        discusiones_count INTEGER DEFAULT 0,
        planes_count INTEGER DEFAULT 0,
        success_rate REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabla: reportes (snapshots generados)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reportes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,                    -- 'etapa', 'proyecto', 'motor'
        titulo TEXT,
        etapa_id INTEGER,
        tokens_total INTEGER DEFAULT 0,
        costo_total REAL DEFAULT 0,
        contenido_json TEXT,          -- JSON con datos del reporte
        fecha_generado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        generado_por TEXT,            -- 'sistema', 'usuario'
        FOREIGN KEY(etapa_id) REFERENCES etapas(id)
    )
    ''')
    
    # Tabla: comandos ejecutados (auditoría)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comandos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comando TEXT NOT NULL,        -- 'gen_discusión', 'ejecutar_plan', etc
        parametros TEXT,              -- JSON con args
        estado TEXT,                  -- 'éxito', 'error', 'en_progreso'
        resultado TEXT,               -- JSON con resultado
        error_msg TEXT,
        fecha_ejecucion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        duracion_ms INTEGER,
        motor_usado TEXT
    )
    ''')
    
    # Tabla: estadísticas por motor
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS motor_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        motor TEXT UNIQUE,
        total_eventos INTEGER DEFAULT 0,
        total_tokens INTEGER DEFAULT 0,
        costo_total REAL DEFAULT 0,
        promedio_tokens_por_evento REAL DEFAULT 0,
        success_count INTEGER DEFAULT 0,
        error_count INTEGER DEFAULT 0,
        tiempo_promedio_seg REAL DEFAULT 0,
        ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Índices para queries rápidas
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_token_etapa ON token_events(etapa)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_token_motor ON token_events(motor)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_token_estado ON token_events(estado)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_etapa_estado ON etapas(estado)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reporte_etapa ON reportes(etapa_id)')
    
    conn.commit()
    conn.close()
    
    print(f"✅ Base de datos inicializada: {db_path}")
    print("   Tablas creadas:")
    print("   - token_events")
    print("   - etapas")
    print("   - reportes")
    print("   - comandos")
    print("   - motor_stats")

if __name__ == '__main__':
    init_database()