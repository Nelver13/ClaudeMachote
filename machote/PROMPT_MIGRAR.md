# PROMPT DE MIGRACIÓN — Sistema viejo → nuevo
> Pega esto a cualquier IA si el proyecto ya tiene un sistema IA viejo.

---

```
Este proyecto tiene un sistema IA viejo que hay que actualizar.

PASO 1 — Clona la versión nueva del sistema:
```bash
git clone git@github.com:Nelver13/ClaudeMachote.git sistema-ia-nuevo
```

PASO 2 — Ejecuta el migrador (hace backup de lo viejo, instala lo nuevo):
```bash
python sistema-ia-nuevo/sistema-ia/acciones/migrar.py
```

El script hace esto solo:
- Mueve archivos viejos (AGENT.md, MAPA.md, acciones/, estado.log, etc.) a sistema-ia/_backup_migracion/
- Copia la nueva estructura limpia
- Protege .gitignore

PASO 3 — Renombra la carpeta nueva:
```bash
mv sistema-ia-nuevo sistema-ia
```

PASO 4 — Ahora configúrame. Pregúntame UNA por UNA:
1. ¿Nombre del proyecto?
2. ¿Stack?
3. ¿IAs que trabajan aquí?
4. ¿Rol de cada IA hoy?
5. ¿Hay módulos ya completados que deba conocer?
6. ¿Hay un plan activo ahora?

PASO 5 — Actualiza sistema-ia/ESTADO.md con las respuestas.

PASO 6 — Avisa: "Listo — [proyecto] migrado a v2.0 — revisa."

Reglas desde ya:
- Sin saludos ni relleno. Una pregunta a la vez.
- git commit/push/pull/add — NUNCA.
```
