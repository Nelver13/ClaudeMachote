# Skill: Docker Producción
name: docker-prod
description: Configuración de Docker para deploy de producción. Se activa cuando el arquitecto dice "listo para producción", "hacer deploy" o "dockerizar".
allowed tools: Read, Grep, Glob, Edit, Write, Bash

---

## Cuándo se activa

- El arquitecto dice "está listo para producción"
- El arquitecto pide "dockerizar el proyecto"
- El arquitecto pide "preparar para deploy"

## Principios

- Una imagen por servicio (no meter todo en uno)
- Variables de entorno desde `.env` → nunca hardcodeadas
- Imagen mínima: Alpine o slim siempre que sea posible
- Multi-stage build para reducir tamaño final
- `docker-compose.yml` para orquestación local
- `docker-compose.prod.yml` para producción (override)

## Estructura típica — Django + React

```
docker/
├── django/
│   └── Dockerfile
├── react/
│   └── Dockerfile
└── nginx/
    ├── Dockerfile
    └── nginx.conf
docker-compose.yml
docker-compose.prod.yml
.env
.env.example
```

## Dockerfile Django (producción)

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Dockerfile React (multi-stage)

```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

## docker-compose.yml base

```yaml
version: '3.9'
services:
  db:
    image: postgres:16-alpine
    env_file: .env
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./docker/django
    env_file: .env
    depends_on: [db]
    volumes:
      - static_files:/app/staticfiles

  frontend:
    build: ./docker/react
    depends_on: [backend]

volumes:
  postgres_data:
  static_files:
```

## Checklist antes de deploy

- [ ] `.env` en `.gitignore`
- [ ] `.env.example` actualizado con todas las variables
- [ ] No hay secrets hardcodeados en `Dockerfile` ni `docker-compose`
- [ ] `DEBUG=False` en producción
- [ ] `ALLOWED_HOSTS` configurado
- [ ] `SECRET_KEY` generada con `python -c "import secrets; print(secrets.token_hex(50))"`
