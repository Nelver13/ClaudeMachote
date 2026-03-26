# Skill: React + Vite
name: react-vite
description: Convenciones y patrones para proyectos React con Vite. Se activa al trabajar con componentes, hooks, rutas, estado frontend o vite.config.
allowed tools: Read, Grep, Glob, Edit, Write, Bash

---

## Convenciones

- Componentes en `PascalCase`
- Hooks personalizados en `/hooks/` con prefijo `use`
- Servicios API en `/services/`
- Estado global: Context API o Zustand (no Redux salvo que ya esté)
- Nunca hardcodear URLs → siempre `import.meta.env.VITE_API_URL`
- Estilos: módulos CSS o Tailwind según el proyecto

## Estructura del proyecto

```
src/
├── components/
│   └── NombreComponente/
│       ├── NombreComponente.jsx
│       └── NombreComponente.module.css
├── hooks/
│   └── useNombre.js
├── pages/
│   └── NombrePage.jsx
├── services/
│   └── nombre.service.js
├── context/
│   └── NombreContext.jsx
└── utils/
```

## Patrones

### Componente
```jsx
// ARCHIVO: NombreComponente.jsx
// QUÉ HACE: descripción
// CÓMO ENCAJA: conexión con el resto

const NombreComponente = ({ prop1, prop2 }) => {
  return <div>{prop1}</div>
}

export default NombreComponente
```

### Servicio API con JWT
```js
// ARCHIVO: nombre.service.js
const API = import.meta.env.VITE_API_URL

export const getNombres = async (token) => {
  const res = await fetch(`${API}/api/v1/nombres/`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  return res.json()
}
```

## Variables de entorno

```
VITE_API_URL=http://localhost:8000
```

## Git — reglas de seguridad

Antes de cualquier `git add`, verificar `.gitignore` incluye:
```
node_modules/
dist/
.vite/
.env
.env.local
.env.*.local
```

Si el proyecto se deploya vía Docker, verificar que el `Dockerfile` no copia `.env`.

## Comandos frecuentes

```bash
npm run dev
npm run build
npm run preview
npm run lint
```
