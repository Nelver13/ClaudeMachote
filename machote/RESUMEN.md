# Sistema Multi-IA — Arranque rápido

## Clonar e instalar

```bash
git clone https://github.com/TU_USER/machote-ia sistema-ia
```

Abre el proyecto en Claude Code → el sistema arranca solo.

---

## Qué hace al abrir

**Primera vez (proyecto nuevo):**
- Detecta que no está configurado
- Te pregunta una por una: nombre, stack, IAs, roles
- Configura ESTADO.md automáticamente

**Sesiones siguientes:**
- Carga el último checkpoint
- Te dice en qué módulo estás, qué falta, próxima tarea
- Listo para trabajar en segundos

---

## El ciclo completo

```
TÚ: idea
  ↓
Arquitecto debate (preguntas en archivo, no en chat)
  ↓
TÚ: "0" → plan listo → PROMPT_DEV generado
  ↓
Dev cambia rol solo → ejecuta todo → avisa
  ↓
TÚ revisas → "ok"
```

---

## Archivos que editas tú

| Archivo | Para qué |
|---------|----------|
| `ESTADO.md` | Cambiar roles de IAs |
| `sistema-ia/discusiones/` | Escribir feedback con `r/` |

Todo lo demás lo hace la IA.

---

## Comandos en el chat

| Comando | Acción |
|---------|--------|
| `1` | IA procesa tu feedback del archivo |
| `0` | Aprueba → genera plan |
| `ok` | Aprueba plan ejecutado |
