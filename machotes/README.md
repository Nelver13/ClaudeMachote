# Machotes

Plantillas listas para copiar a nuevos proyectos.

---

## kimi+claude

**Dos terminales. Opus discute y planea, Sonnet ejecuta.**

```
Terminal 1: claude (Opus)   → Modo KIMI — discute y genera planes
Terminal 2: claude (Sonnet) → Modo CLAUDE — ejecuta el plan
```

Flujo:
1. Opus abre → anuncia "Modo: KIMI"
2. Discutis la idea → `0` → Kimi crea plan_XXX.md → avisa
3. Sonnet abre → anuncia "Modo: CLAUDE" → `sigue` → ejecuta
4. Al terminar → marca "En revision" → avisa
5. Vas a Kimi → `ok` → aprobado

**Cuando usarlo:** proyectos con planificacion previa, modulos grandes, cuando queres que el arquitecto piense antes de que Claude toque codigo.

---

## solo-claude

**Una terminal. Claude discute, planea Y ejecuta.**

```
Terminal: claude (Sonnet) → Modo CLAUDE AUTONOMO
```

Flujo:
1. Contale la idea → Claude crea disc_*.md → avisa
2. Refinan → `0` → Claude crea plan_XXX.md → avisa
3. `sigue` → Claude ejecuta tarea por tarea → avisa
4. Al terminar → marca "Completado" → avisa

**Cuando usarlo:** proyectos chicos, prototipado rapido, cuando no necesitas un ciclo de revision separado.

---

## Como usar un machote

```bash
# Copiar al proyecto nuevo
cp -r machotes/kimi+claude/ ../mi-proyecto/
# o
cp -r machotes/solo-claude/ ../mi-proyecto/

# Configurar credenciales Discord
nano mi-proyecto/claude/acciones/credenciales.md

# Probar avisos
python mi-proyecto/claude/acciones/avisar.py --test
```
