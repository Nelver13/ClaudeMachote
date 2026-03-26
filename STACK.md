# STACK.md — Stack Personal del Arquitecto
> Este archivo lo mantenés vos. Actualizarlo cuando cambie el stack.
> Claude lo lee al iniciar cada sesión.

---

## 🌐 Web Fullstack
- **Backend:** Django + Django REST Framework (DRF)
- **Frontend:** React + Vite
- **Base de datos:** PostgreSQL
- **Autenticación:** JWT (SimpleJWT)
- **API:** RESTful, versionada con `/aspni/vw1w/`

## 📱 Mobile
- **Opción A:** React Native + Expo
- **Opción B:** Flutter

## 🖥️ Desktop
- **Stack:** WinForms — Visual Basic o C#

## ⚙️ Automatizaciones
- **n8n** — flujos y webhooks

---

## 📐 Convenciones

### Django
- `snake_case` en todo
- Serializers en `serializers.py`
- Validaciones en el serializer
- Modelos con `__str__` siempre definido

### React
- Componentes en `PascalCase`
- Hooks personalizados en `/hooks/`

### API
- Siempre JWT
- Endpoints RESTful — `/api/v1/`
- Nunca hardcodear secrets

### WinForms
- Lógica de negocio separada de la UI
- Conexión a DB encapsulada en capa de datos

---

## 🔧 Entorno
- **Control de versiones:** Git — el arquitecto administra commits y push
- **Variables de entorno:** siempre `.env` + `.env.example`

_Última actualización: [FECHA]_
