# Registro de Vacaciones de Empleados

Proyecto final de Programación 1 - Django.

## Requisitos
- Python 3.13+
- Django 6.1.2

## Cómo correr el proyecto

1. Clonar el repositorio:
   git clone https://github.com/MariiRo/registro-vacaciones.git
   cd registro-vacaciones

2. Crear y activar el entorno virtual:
   python -m venv venv
   venv\Scripts\activate

3. Instalar dependencias:
   pip install -r requirements.txt

4. Aplicar migraciones:
   python manage.py migrate

5. Correr el servidor:
   python manage.py runserver

6. Abrir http://127.0.0.1:8000/ en el navegador.

7. Cargar datos iniciales desde /admin/:
   - Departamentos: Administración, Ventas, Depósito
   - Tipos de licencia: Vacaciones (14 días), Licencia por enfermedad (30 días), Licencia por estudio (10 días)

## Funcionalidades
- Registro, login y logout de usuarios.
- CRUD de solicitudes de vacaciones.
- Comentarios en cada solicitud.
- Búsqueda por nombre de empleado.
- Validación personalizada de fechas.
- Panel de administración para gestionar departamentos y tipos de licencia.