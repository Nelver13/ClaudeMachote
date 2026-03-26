#!/usr/bin/env python3
"""
Motor Detect — Detecta qué IDE/motor de IA está siendo usado
- Copilot en VS Code
- Claude en VS Code
- Cursor IDE
- Google Antigravity

Actualiza .motor/motor.json con el resultado.
"""

import os
import json
import sys
import subprocess
import platform
from pathlib import Path

def detect_vscode():
    """¿Estamos en VS Code?"""
    if os.getenv('TERM_PROGRAM') in ['vscode', 'Cursor']:
        return 'vscode'
    
    # Windows
    if os.getenv('VSCODE_PID'):
        return 'vscode'
    
    return None

def detect_cursor():
    """¿Estamos en Cursor IDE?"""
    if os.getenv('TERM_PROGRAM') == 'Cursor':
        return True
    
    # Windows
    if 'Cursor' in os.getenv('PATH', ''):
        return True
    
    return False

def detect_copilot():
    """¿GitHub Copilot activado en VS Code?"""
    # Buscar extensión Copilot
    ext_dir = Path.home() / '.vscode' / 'extensions'
    if ext_dir.exists():
        copilot_exts = [d for d in ext_dir.iterdir() 
                       if d.is_dir() and 'copilot' in d.name.lower()]
        return len(copilot_exts) > 0
    return False

def detect_claude_extension():
    """¿Claude Extension en VS Code?"""
    ext_dir = Path.home() / '.vscode' / 'extensions'
    if ext_dir.exists():
        claude_exts = [d for d in ext_dir.iterdir() 
                      if d.is_dir() and 'claude' in d.name.lower()]
        return len(claude_exts) > 0
    return False

def detect_antigravity():
    """¿Google Antigravity disponible?"""
    # Por ahora, check basic — requeriría Google API auth
    return False

def main():
    motor_file = Path(__file__).parent.parent.parent / '.motor'
    
    # Si .motor es un archivo (como en la plantilla), convertir a directorio
    if motor_file.is_file():
        motor_file.unlink()  # Eliminar el archivo
        motor_file.mkdir()   # Crear directorio
        motor_file = motor_file / 'motor.json'
    elif motor_file.is_dir():
        motor_file = motor_file / 'motor.json'
    else:
        motor_file.parent.mkdir(exist_ok=True)
        motor_file = motor_file / 'motor.json'
    
    detected = None
    details = {
        'vscode': detect_vscode(),
        'copilot': detect_copilot(),
        'claude_ext': detect_claude_extension(),
        'cursor': detect_cursor(),
        'antigravity': detect_antigravity()
    }
    
    print("🔍 Detectando motor...")
    print(f"  VS Code: {details['vscode']}")
    print(f"  Copilot: {details['copilot']}")
    print(f"  Claude Ext: {details['claude_ext']}")
    print(f"  Cursor IDE: {details['cursor']}")
    print(f"  Google Antigravity: {details['antigravity']}")
    
    # Lógica de detección
    if details['cursor']:
        detected = 'cursor'
    elif details['vscode']:
        if details['copilot']:
            detected = 'copilot'
        elif details['claude_ext']:
            detected = 'claude'
    elif details['antigravity']:
        detected = 'antigravity'
    else:
        detected = 'unknown'
    
    # Actualizar motor.json
    if motor_file.exists():
        with open(motor_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {}
    
    config['detected_motor'] = detected
    config['detection_details'] = details
    config['platform'] = platform.system()
    
    with open(motor_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Motor detectado: {detected}")
    print(f"📝 Actualizado: {motor_file}")

if __name__ == '__main__':
    main()