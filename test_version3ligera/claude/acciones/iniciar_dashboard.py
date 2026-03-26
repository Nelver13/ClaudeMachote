#!/usr/bin/env python3
"""
Iniciar Dashboard — Launcher para Version3Ligera
Ejecuta: python iniciar_dashboard.py

Inicia el servidor Flask y abre el navegador automáticamente.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    """Inicia el dashboard"""
    base_dir = Path(__file__).parent.parent.parent
    
    print("🚀 Iniciando Version3Ligera Dashboard...")
    
    # Verificar que existe app.py
    app_path = base_dir / 'claude' / 'dashboard' / 'app.py'
    if not app_path.exists():
        print(f"❌ No se encuentra app.py en {app_path}")
        return
    
    # Verificar requirements
    req_path = base_dir / 'claude' / 'dashboard' / 'requirements.txt'
    if req_path.exists():
        print("📦 Verificando dependencias...")
        # Aquí podríamos verificar si están instaladas
    
    # Iniciar servidor Flask
    try:
        print("🌐 Iniciando servidor...")
        os.chdir(app_path.parent)
        
        # Ejecutar Flask app
        cmd = [sys.executable, 'app.py']
        process = subprocess.Popen(cmd, cwd=app_path.parent)
        
        # Esperar un poco para que inicie
        time.sleep(2)
        
        # Abrir navegador
        url = "http://localhost:5000"
        print(f"📱 Abriendo navegador: {url}")
        webbrowser.open(url)
        
        print("✅ Dashboard iniciado exitosamente")
        print("   Presiona Ctrl+C para detener")
        
        # Mantener vivo
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...")
        process.terminate()
    except Exception as e:
        print(f"❌ Error iniciando dashboard: {e}")

if __name__ == '__main__':
    main()