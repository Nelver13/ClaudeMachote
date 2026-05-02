# actualizar_checklist.py
# Actualiza checklist automáticamente durante ejecución
# Mantiene memoria de continuidad entre sesiones

import os
import re
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CLAUDE_DIR = SCRIPT_DIR.parent
PLANES_DIR = CLAUDE_DIR / 'planes'

def marcar_tarea_completada(plan_path, tarea_descripcion):
    """Marca una tarea como completada en el checklist"""
    try:
        plan_filepath = Path(plan_path)
        if not plan_filepath.exists():
            print(f'Error: Plan no encontrado: {plan_filepath}')
            return False

        with open(plan_filepath, 'r', encoding='utf-8') as f:
            contenido = f.read()

        # Buscar la tarea y marcarla como completada
        patron = r'(\s*)- \[ \] ' + re.escape(tarea_descripcion)
        reemplazo = r'\1- [x] ' + tarea_descripcion

        if re.search(patron, contenido):
            contenido_actualizado = re.sub(patron, reemplazo, contenido)

            # Actualizar memoria de continuidad
            contenido_actualizado = actualizar_memoria_continuidad(
                contenido_actualizado, tarea_descripcion
            )

            with open(plan_filepath, 'w', encoding='utf-8') as f:
                f.write(contenido_actualizado)

            print(f"✓ Tarea completada: {tarea_descripcion}")
            return True
        else:
            print(f"⚠ No se encontró la tarea: {tarea_descripcion}")
            return False

    except Exception as e:
        print(f"Error al actualizar checklist: {e}")
        return False

def actualizar_memoria_continuidad(contenido, tarea_completada):
    """Actualiza la sección de memoria de continuidad"""
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Buscar sección de memoria
    patron_memoria = r'(## Memoria de continuidad\n)(.*?)(?=##|\Z)'
    match = re.search(patron_memoria, contenido, re.DOTALL)

    if match:
        memoria_actual = match.group(2).strip()

        # Actualizar última tarea completada
        memoria_actual = re.sub(
            r'- \*\*Última tarea completada:\*\* .*',
            f'- **Última tarea completada:** {tarea_completada} ({ahora})',
            memoria_actual
        )

        # Calcular próxima tarea
        proxima = obtener_proxima_tarea(contenido)
        if proxima:
            memoria_actual = re.sub(
                r'- \*\*Próxima tarea:\*\* .*',
                f'- **Próxima tarea:** {proxima}',
                memoria_actual
            )

        # Calcular progreso
        progreso = calcular_progreso(contenido)
        memoria_actual = re.sub(
            r'- \*\*Estado general:\*\* .*',
            f'- **Estado general:** {progreso}%',
            memoria_actual
        )

        contenido = contenido.replace(match.group(2), memoria_actual + '\n')

    return contenido

def obtener_proxima_tarea(contenido):
    """Obtiene la próxima tarea pendiente"""
    lineas = contenido.split('\n')
    for linea in lineas:
        if '- [ ] ' in linea and not linea.strip().startswith('  '):
            # Es una tarea principal pendiente
            tarea = linea.replace('- [ ] ', '').strip()
            return tarea
    return "Ninguna tarea pendiente"

def calcular_progreso(contenido):
    """Calcula el porcentaje de progreso"""
    total_tareas = len(re.findall(r'- \[.\] ', contenido))
    tareas_completadas = len(re.findall(r'- \[x\] ', contenido))

    if total_tareas == 0:
        return 100

    return int((tareas_completadas / total_tareas) * 100)

def obtener_estado_plan(plan_path):
    """Obtiene el estado actual del plan"""
    try:
        plan_filepath = Path(plan_path)
        if not plan_filepath.exists():
            return None

        with open(plan_filepath, 'r', encoding='utf-8') as f:
            contenido = f.read()

        progreso = calcular_progreso(contenido)
        proxima = obtener_proxima_tarea(contenido)

        return {
            'progreso': progreso,
            'proxima_tarea': proxima,
            'completado': progreso == 100
        }

    except Exception as e:
        print(f"Error al leer estado del plan: {e}")
        return None

def main():
    if len(sys.argv) < 3:
        print("Uso: python actualizar_checklist.py <plan_path> <tarea_descripcion>")
        print("O: python actualizar_checklist.py <plan_path> --estado")
        sys.exit(1)

    plan_path = sys.argv[1]

    if not os.path.exists(plan_path):
        print(f"Error: No existe el archivo {plan_path}")
        sys.exit(1)

    if len(sys.argv) == 3 and sys.argv[2] == '--estado':
        # Mostrar estado del plan
        estado = obtener_estado_plan(plan_path)
        if estado:
            print(f"Progreso: {estado['progreso']}%")
            print(f"Próxima tarea: {estado['proxima_tarea']}")
            print(f"Completado: {'Sí' if estado['completado'] else 'No'}")
    else:
        # Marcar tarea como completada
        tarea_descripcion = ' '.join(sys.argv[2:])
        if marcar_tarea_completada(plan_path, tarea_descripcion):
            # Notificar si está configurado
            try:
                import subprocess
                subprocess.run([
                    'python', 'avisar.py',
                    f"Tarea completada: {tarea_descripcion[:50]}...",
                    'suave'
                ], cwd=str(SCRIPT_DIR))
            except:
                pass  # Avisar es opcional

if __name__ == "__main__":
    main()