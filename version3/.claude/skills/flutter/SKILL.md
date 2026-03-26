# Skill: Flutter
name: flutter
description: Convenciones y patrones para proyectos Flutter. Se activa automáticamente al trabajar con pubspec.yaml, widgets, providers, screens o archivos .dart.
allowed tools: Read, Grep, Glob, Edit, Write, Bash

---

## Convenciones

- `snake_case` para archivos y carpetas
- `PascalCase` para clases y widgets
- `camelCase` para variables y funciones
- Widgets sin lógica de negocio — lógica en providers o services
- Estado: Provider o Riverpod (verificar el que ya usa el proyecto)
- Nunca hardcodear strings de UI — usar constantes en `lib/core/constants/`

## Estructura del proyecto

```
lib/
├── main.dart
├── core/
│   ├── constants/
│   ├── theme/
│   └── utils/
├── data/
│   ├── models/
│   ├── repositories/
│   └── services/          ← llamadas a API
├── presentation/
│   ├── screens/
│   │   └── nombre/
│   │       ├── nombre_screen.dart
│   │       └── widgets/
│   └── providers/         ← estado
└── routes/
    └── app_router.dart
```

## Bloque de encabezado (cada archivo nuevo)

```dart
// ARCHIVO: nombre.dart
// QUÉ HACE: descripción simple
// CÓMO ENCAJA: conexión con el resto
// DEPENDENCIAS: qué importa
```

## Patrones

### Widget stateless
```dart
class NombreWidget extends StatelessWidget {
  const NombreWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
```

### Llamada a API
```dart
// data/services/nombre_service.dart
class NombreService {
  final String _base = const String.fromEnvironment('API_URL');

  Future<List<NombreModel>> getAll(String token) async {
    final res = await http.get(
      Uri.parse('$_base/api/v1/nombres/'),
      headers: {'Authorization': 'Bearer $token'},
    );
    // parsear respuesta
  }
}
```

### Model con fromJson
```dart
class NombreModel {
  final int id;
  final String nombre;

  NombreModel({required this.id, required this.nombre});

  factory NombreModel.fromJson(Map<String, dynamic> json) =>
      NombreModel(id: json['id'], nombre: json['nombre']);
}
```

## Comandos frecuentes

```bash
flutter pub get
flutter run
flutter build apk
flutter build ios
flutter test
flutter analyze
```

## Variables de entorno

Flutter no usa `.env` nativo. Opciones:
- `--dart-define=API_URL=http://...` al correr/build
- Paquete `flutter_dotenv` si ya está en el proyecto
