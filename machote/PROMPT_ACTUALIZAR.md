# PROMTO DE ACTUALIZACIÓN — Sistema Multi-IA v2.7
> Pega esto a cualquier IA para actualizar el sistema a la última versión.
> Ya no hay pasos manuales — el script lo hace todo.

---

```
Actualiza el sistema IA de este proyecto.

PASO 1 — Clona y ejecuta:
git clone https://github.com/Nelver13/ClaudeMachote.git sistema-ia-temp
python sistema-ia-temp/acciones/actualizar.py

El script detecta tu proyecto automáticamente y hace TODO:
- Sincroniza scripts, skills, docs y VERSION
- Crea backup completo antes de tocar nada
- Crea carpetas/archivos que falten (bugs, run scripts, etc.)
- Instala/verifica dependencias (Pillow, pynput, etc.)
- Actualiza .gitignore
- Muestra guía de novedades

PASO 2 — Borra el clon temporal:
rmdir /s /q sistema-ia-temp   (Windows)
rm -rf sistema-ia-temp        (Mac/Linux)

Listo.

Reglas:
- NO tocar: ESTADO.md, discusiones/, planes/, memoria/, código de producción
- git commit/push/add — NUNCA.
```
