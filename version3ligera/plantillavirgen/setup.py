#!/usr/bin/env python3
"""
Setup Automatico - Version3Ligera
Ejecuta: python setup.py
Hace todo el proceso de instalacion automatica
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Ejecuta comando y muestra resultado"""
    print(f"\n[INFO] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print(f"[OK] {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error en {description}: {e}")
        print(f"Salida: {e.output}")
        return False

def check_python_version():
    """Verifica version de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"[ERROR] Python {version.major}.{version.minor} no soportado. Necesitas Python 3.8+")
        return False
    print(f"[OK] Python {version.major}.{version.minor}.{version.micro} OK")
    return True

def install_flask():
    """Instala Flask si no esta"""
    try:
        import flask
        print("[OK] Flask ya instalado")
        return True
    except ImportError:
        print("[INFO] Instalando Flask...")
        return run_command("pip install flask", "Instalacion de Flask")

def ensure_ia_folder():
    """Crea/usa carpeta ia y copia plantilla si se ejecuta desde otro folder."""
    project_root = Path.cwd()
    target_dir = project_root

    if project_root.name != 'ia':
        target_dir = project_root / 'ia'

    # Si no existe, crea y copia plantilla base:
    if not target_dir.exists():
        print(f"[INFO] Creando carpeta de proyecto: {target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)

    # Si setup se ejecuta desde plantilla, copiar contenido en ia
    source_dir = Path(__file__).resolve().parent
    if source_dir != target_dir:
        for item in source_dir.iterdir():
            if item.name == 'venv':
                continue
            dest = target_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)

    print(f"[OK] Entorno de trabajo: {target_dir}")
    os.chdir(target_dir)
    return target_dir


def init_database():
    """Inicializa base de datos"""
    script = Path("claude/acciones/init_db.py")
    if script.exists():
        return run_command("python claude/acciones/init_db.py", "Inicializacion de base de datos")
    else:
        print("[ERROR] init_db.py no encontrado")
        return False

def create_venv():
    """Crea un entorno virtual y devuelve ruta de pip"""
    venv_dir = Path("venv")
    if not venv_dir.exists():
        print("[INFO] Creando entorno virtual en ./venv ...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] No se pudo crear venv: {e}")
            return None
    else:
        print("[INFO] Entorno virtual ya existe: ./venv")
    # Selecciona pip del venv
    if platform.system() == "Windows":
        pip_path = venv_dir / "Scripts" / "pip.exe"
    else:
        pip_path = venv_dir / "bin" / "pip"
    if not pip_path.exists():
        print(f"[ERROR] pip no encontrado en entorno virtual: {pip_path}")
        return None
    print(f"[OK] pip de venv: {pip_path}")
    return str(pip_path)

def install_requirements_from_venv(pip_exe):
    """Instala requirements usando pip del venv"""
    req_file = Path("claude/dashboard/requirements.txt")
    if not req_file.exists():
        print("[ERROR] requirements.txt no encontrado en claude/dashboard")
        return False
    cmd = f'"{pip_exe}" install -r "{req_file}"'
    return run_command(cmd, "Instalacion de requirements en venv")

def detect_motor():
    """Detecta motor de IA"""
    script = Path("claude/acciones/motor_detect.py")
    if script.exists():
        return run_command("python claude/acciones/motor_detect.py", "Deteccion de motor IA")
    else:
        print("[ERROR] motor_detect.py no encontrado")
        return False

def test_dashboard():
    """Test basico del dashboard"""
    script = Path("claude/dashboard/app.py")
    if script.exists():
        print("\n[TEST] Probando sintaxis del dashboard...")
        try:
            subprocess.run([sys.executable, "-m", "py_compile", "claude/dashboard/app.py"],
                         capture_output=True, check=True)
            print("[OK] Sintaxis del dashboard OK")
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] Error de sintaxis en dashboard")
            return False
    else:
        print("[ERROR] app.py no encontrado")
        return False

def main():
    """Setup automatico completo"""
    print("Setup Automatico - Version3Ligera")
    print("=" * 50)

    # Asegurarse de estar dentro de ia/ y copiar plantilla si es necesario
    project_dir = ensure_ia_folder()

    # Verificar que estamos en el directorio correcto
    if not Path("claude").exists():
        print("[ERROR] Error: no encontró carpeta claude/ en el directorio actual")
        sys.exit(1)

    success = True

    # 1. Verificar Python
    if not check_python_version():
        success = False

    # 2. Crear entorno virtual e instalar requirements
    pip_venv = create_venv()
    if pip_venv is None or not install_requirements_from_venv(pip_venv):
        success = False

    # 3. Inicializar DB
    if not init_database():
        success = False

    # 4. Detectar motor
    if not detect_motor():
        success = False

    # 5. Verificar dashboard
    if not test_dashboard():
        success = False

    print("\n" + "=" * 50)
    if success:
        print("Setup completado exitosamente!")
        print("\nProximos pasos:")
        print("1. Ejecuta: python claude/acciones/iniciar_dashboard.py")
        print("2. Abre: http://localhost:5000")
        print("3. Disfruta tu sistema de gestion con IA!")
    else:
        print("Setup fallo. Revisa los errores arriba.")
        print("\nSoluciones:")
        print("- Verifica que tienes Python 3.8+")
        print("- Instala manualmente: pip install flask")
        print("- Ejecuta scripts individualmente para debug")

    return success

if __name__ == "__main__":
    main()