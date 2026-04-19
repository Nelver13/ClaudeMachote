# NOVEDADES — Instrucciones de actualización para la IA
> Este archivo lo lee auto_setup.py al detectar version nueva.
> La IA ejecuta las instrucciones de la version que acaba de instalarse.
> Formato: una seccion por version. La IA ejecuta solo la mas reciente.

---

## v2.5

### Que cambio
- auto_setup.py ahora hace git pull automatico y lee este archivo
- La IA ejecuta las instrucciones de actualizacion sola al arrancar

### Ejecutar ahora (la IA lo hace):

1. Verificar que AGENTS.md tiene la seccion de ahorro de tokens (no "MODO CAVEMAN"):
   - Abre AGENTS.md
   - Si la primera seccion dice "MODO CAVEMAN (siempre activo)" -> reemplazala por el contenido de sistema-ia/machote/AGENTS.md seccion "AHORRO DE TOKENS"
   - Si ya dice "AHORRO DE TOKENS" -> OK, no hacer nada

2. Verificar que INICIO.md existe en la raiz del proyecto:
   - Si no existe -> copia sistema-ia/machote/INICIO.md -> INICIO.md
   - Si existe -> OK

3. Avisar cuando termines:
   python sistema-ia/acciones/avisar.py "Proyecto actualizado a v2.5" normal

### No tocar:
- ESTADO.md
- Nombre del proyecto, stack, roles
- planes/ discusiones/ memoria/
