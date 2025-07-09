# Proyecto saludmujer.cl

## Descripción técnica
Este proyecto utiliza **Python 3.10**, **Djongo 1.3.7** y **Django REST Framework 3.12.4** para permitir una integración directa entre Django y MongoDB usando la capa de modelos (`models.py`).

Se eligió **Djongo** en lugar de **mongoengine** porque Djongo permite definir modelos de datos usando la sintaxis estándar de Django (`models.Model`), lo que facilita el uso de migraciones, validaciones y la integración con el admin de Django. En cambio, mongoengine solo permite definir documentos (`Document`), lo que limita la compatibilidad con muchas herramientas y librerías del ecosistema Django.

De esta forma, el proyecto mantiene la estructura y ventajas de un proyecto Django tradicional, pero usando MongoDB como base de datos.

## Requisitos
- Python 3.10
- MongoDB

## Instalación de dependencias

Instala las dependencias usando el entorno virtual y pip:

```
python -m venv venv
venv\Scripts\activate  # En Windows
```

### Dependencias principales (versiones usadas)
- Django==3.1.12
- djangorestframework==3.12.4
- djongo==1.3.7
- pymongo==3.11.4
- djangorestframework-authtoken (incluido en DRF)
- pytz==2025.2

## Configuración de la base de datos

Asegúrate de tener MongoDB corriendo y la configuración correcta en `settings.py`.

## Migraciones

```
python manage.py makemigrations
python manage.py migrate
```

## Cómo iniciar el servidor

```
python manage.py runserver
```

## Cómo crear un usuario para autenticación por token

Puedes crear un usuario normal o un superusuario:

### Opción 1: Superusuario
```
python manage.py createsuperuser
```
Sigue las instrucciones para ingresar usuario y contraseña.

### Opción 2: Usuario normal
```
python manage.py shell
```
Luego en el shell de Python:
```python
from django.contrib.auth.models import User
User.objects.create_user('admin', password='admin')
exit()
```

## Cómo obtener un token de autenticación

Haz un POST a:
```
http://localhost:8000/api-token-auth/
```
Con el body:
```json
{
  "username": "admin",
  "password": "admin"
}
```
La respuesta será:
```json
{
  "token": "<tu_token>"
}
```

## Cómo usar el token para endpoints protegidos

Agrega el siguiente header en tus peticiones:
```
Authorization: Token <tu_token>
```

## Endpoints principales
- `POST /patient/` — Crear paciente (mixin)
- `GET /patients/` — Listar pacientes (generic)
- `GET /patient/<object_id>/` — Obtener paciente por id (viewset)
- `PUT /patient/<object_id>/` — Actualizar paciente (APIView, requiere token)
- `DELETE /patient/<object_id>/` — Eliminar paciente (APIView, requiere token) 