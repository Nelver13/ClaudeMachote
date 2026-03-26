# Skill: Mobile — React Native + Flutter + Electron
name: mobile
description: Patrones para proyectos mobile y desktop cross-platform. Cubre React Native + Expo, Flutter, y Electron. Se activa al trabajar con app.json, pubspec.yaml, main.js de Electron, o archivos de plataforma móvil.
allowed tools: Read, Grep, Glob, Edit, Write, Bash

---

## Detección automática de sub-stack

| Archivo | Sub-stack activo |
|---|---|
| `app.json` + `expo` en package.json | React Native + Expo |
| `pubspec.yaml` | Flutter |
| `package.json` + `electron` | Electron |

Cuando hay múltiples → aplicar convenciones de todos los sub-stacks activos.

---

## React Native + Expo

### Convenciones
- Componentes en `PascalCase`
- Navegación con `expo-router` (file-based)
- Estado: Context API o Zustand
- Nunca acceder a APIs nativas sin verificar plataforma (`Platform.OS`)
- Estilos con `StyleSheet.create()`, no inline

### Estructura
```
app/
├── (tabs)/
│   ├── index.tsx
│   └── perfil.tsx
├── _layout.tsx
components/
hooks/
services/
constants/
```

### .gitignore adicional
```
.expo/
android/build/
ios/build/
*.ipa
*.apk
```

---

## Flutter

### Convenciones
- `snake_case` para archivos, `PascalCase` para clases
- BLoC o Provider para estado
- Separar UI de lógica: `screens/`, `widgets/`, `services/`, `models/`
- Nunca lógica en el widget directamente → siempre en BLoC/Provider

### Estructura
```
lib/
├── main.dart
├── screens/
├── widgets/
├── models/
├── services/
└── blocs/
```

### .gitignore adicional
```
build/
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
```

---

## Electron

### Convenciones
- `main.js` (proceso principal) separado de `renderer/` (UI React/HTML)
- IPC para comunicación entre procesos — nunca `remote` module
- Nunca exponer Node.js APIs directamente al renderer → usar `preload.js`
- Builds con `electron-builder`

### Estructura
```
src/
├── main/
│   ├── main.js          ← proceso principal
│   └── preload.js       ← puente seguro a renderer
└── renderer/
    ├── App.jsx
    └── index.html
```

### .gitignore adicional
```
out/
release/
dist/
```

---

## Variables de entorno — mobile

Nunca hardcodear en el código. Para Expo:
```
EXPO_PUBLIC_API_URL=https://api.tuapp.com
```

Para Electron: leer de `.env` con `dotenv` solo en proceso principal.
