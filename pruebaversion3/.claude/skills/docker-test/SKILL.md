# Skill: Docker Test/Demo
name: docker-test
description: Deploy rápido a servidor de prueba para probar o mostrar algo. Se activa cuando el arquitecto dice "quiero mostrar algo", "subí a pruebas", "deploy rápido" o "server de test".
allowed tools: Read, Grep, Glob, Edit, Write, Bash

---

## Cuándo se activa

- El arquitecto dice "quiero mostrar algo"
- El arquitecto dice "subí a un servidor de prueba"
- El arquitecto dice "deploy rápido"
- El arquitecto dice "quiero ver cómo queda en el servidor"

## Objetivo

Levantar el proyecto en un servidor en minutos para probar o mostrar. No es producción — es una instancia rápida con las mismas condiciones del servidor real.

## Diferencias con docker-prod

| | docker-test | docker-prod |
|---|---|---|
| Debug | Puede estar activo | Siempre False |
| SSL | Opcional | Obligatorio |
| Datos | De prueba o copia anon | Reales |
| Performance | No optimizado | Optimizado |
| Objetivo | Ver / probar | Servir |

## docker-compose.test.yml

```yaml
version: '3.9'
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: testdb
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test123
    volumes:
      - test_db:/var/lib/postgresql/data

  backend:
    build: .
    environment:
      DEBUG: "True"
      SECRET_KEY: "test-key-no-produccion"
      DATABASE_URL: "postgresql://test:test123@db:5432/testdb"
    ports:
      - "8000:8000"
    depends_on: [db]
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"

  frontend:
    build: ./frontend
    ports:
      - "3000:80"

volumes:
  test_db:
```

## Comandos rápidos

```bash
# Levantar entorno de prueba
docker compose -f docker-compose.test.yml up --build -d

# Ver logs
docker compose -f docker-compose.test.yml logs -f

# Parar y limpiar
docker compose -f docker-compose.test.yml down -v
```

## Checklist antes de deploy de prueba

- [ ] `docker-compose.test.yml` existe o se crea
- [ ] Credenciales de prueba (no las reales de producción)
- [ ] Puerto disponible en el servidor
- [ ] `docker-compose.test.yml` en `.gitignore` si tiene credenciales fijas
