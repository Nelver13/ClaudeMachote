# Skill: Django + DRF
name: django-drf
description: Convenciones y patrones para proyectos Django + Django REST Framework. Se activa automáticamente al trabajar con modelos, serializers, vistas, URLs, migrations o manage.py.
allowed tools: Read, Grep, Glob, Edit, Write, Bash

---

## Convenciones

- `snake_case` en todo (modelos, campos, funciones, URLs)
- Serializers en `serializers.py` por app
- Validaciones en el serializer, nunca en la vista
- Modelos siempre con `__str__` definido
- Lógica de negocio en `services.py`, no en la vista
- URLs versionadas: `/api/v1/`
- Autenticación: JWT con SimpleJWT

## Estructura de app

```
apps/
└── [nombre_app]/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── services.py       ← lógica de negocio
    ├── tests/
    │   ├── test_models.py
    │   └── test_views.py
    └── migrations/
```

## Bloque de encabezado (cada archivo nuevo)

```python
# ARCHIVO: nombre
# QUÉ HACE: descripción simple
# CÓMO ENCAJA: conexión con el resto
# PARA EDITAR: qué saber antes de tocarlo
# DEPENDENCIAS: qué necesita
```

## Patrones

### Model
```python
class NombreModel(models.Model):
    nombre = models.CharField(max_length=100)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return self.nombre
```

### Serializer con validación
```python
class NombreSerializer(serializers.ModelSerializer):
    class Meta:
        model = NombreModel
        fields = '__all__'

    def validate_campo(self, value):
        # validación aquí
        return value
```

### ViewSet
```python
class NombreViewSet(viewsets.ModelViewSet):
    queryset = NombreModel.objects.all()
    serializer_class = NombreSerializer
    permission_classes = [IsAuthenticated]
```

## Comandos frecuentes

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py test apps.[nombre]
python manage.py createsuperuser
```

## Variables de entorno requeridas

```
SECRET_KEY=
DEBUG=
DATABASE_URL=
ALLOWED_HOSTS=
```
