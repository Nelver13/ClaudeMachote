# Skill: React Native + Expo
name: react-native
description: Convenciones y patrones para proyectos React Native con Expo. Se activa automáticamente al trabajar con app.json, expo, componentes nativos o archivos de navegación.
allowed tools: Read, Grep, Glob, Edit, Write, Bash

---

## Convenciones

- Componentes en `PascalCase`
- Hooks personalizados en `/hooks/` con prefijo `use`
- Servicios API en `/services/`
- Navegación: Expo Router (si hay `/app/`) o React Navigation
- Estado global: Zustand o Context API
- Nunca hardcodear URLs → siempre `process.env.EXPO_PUBLIC_API_URL`
- Estilos: StyleSheet.create() o NativeWind si ya está

## Estructura del proyecto

```
app/                        ← si usa Expo Router
├── (tabs)/
│   ├── index.tsx
│   └── _layout.tsx
└── _layout.tsx

src/                        ← si usa React Navigation
├── screens/
│   └── NombreScreen.tsx
├── components/
│   └── NombreComponente.tsx
├── hooks/
│   └── useNombre.ts
├── services/
│   └── nombre.service.ts
├── store/
│   └── nombreStore.ts
└── navigation/
    └── AppNavigator.tsx
```

## Bloque de encabezado (cada archivo nuevo)

```tsx
// ARCHIVO: NombreComponente.tsx
// QUÉ HACE: descripción
// CÓMO ENCAJA: conexión con el resto
```

## Patrones

### Componente nativo
```tsx
import { View, Text, StyleSheet } from 'react-native'

const NombreComponente = ({ texto }: { texto: string }) => {
  return (
    <View style={styles.container}>
      <Text>{texto}</Text>
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 }
})

export default NombreComponente
```

### Servicio API con JWT
```ts
// services/nombre.service.ts
const API = process.env.EXPO_PUBLIC_API_URL

export const getNombres = async (token: string) => {
  const res = await fetch(`${API}/api/v1/nombres/`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  return res.json()
}
```

### Hook con AsyncStorage
```ts
import AsyncStorage from '@react-native-async-storage/async-storage'

const useToken = () => {
  const getToken = async () => AsyncStorage.getItem('token')
  const setToken = async (t: string) => AsyncStorage.setItem('token', t)
  return { getToken, setToken }
}
```

## Variables de entorno

```
EXPO_PUBLIC_API_URL=http://192.168.x.x:8000
```
> Usar IP local (no localhost) para conectar al backend desde el dispositivo físico.

## Comandos frecuentes

```bash
npx expo start
npx expo start --tunnel     ← para dispositivo físico fuera de red local
npx expo build:android
npx expo build:ios
npx expo install            ← instalar deps compatibles con Expo SDK
```
