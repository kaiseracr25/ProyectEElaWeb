Plataforma de Crowdfunding con Django
1. Descripción del Proyecto
Desarrollo de una aplicación web tipo "Kickstarter" que permite gestionar campañas de recaudación de fondos. El sistema cuenta con dos roles: Administrador (gestiona campañas y categorías) y Funder (dona y visualiza su historial) .
Tecnologías: Python, Django, SQLite, Bootstrap 5, HTML/CSS/JS .
________________________________________
2. Configuración del Entorno (Paso a Paso)
2.1. Creación del Entorno Virtual
Para aislar las dependencias del proyecto .
1.	Crear carpeta del proyecto y abrirla en Visual Studio Code.
2.	Abrir terminal y ejecutar:
Bash
python -m venv venv
3.	Activar el entorno:
o	Windows: .\venv\Scripts\activate
o	Mac/Linux: source venv/bin/activate
2.2. Instalación de Dependencias
Instalamos Django y Pillow (para manejo de imágenes).
Bash
pip install django Pillow
2.3. Estructura del Proyecto
Creamos el proyecto principal y la aplicación crowdfunding .
Bash
django-admin startproject sitio_web .
python manage.py startapp crowdfunding
2.4. Configuración Inicial (settings.py)
En sitio_web/settings.py:
1.	Agregar 'crowdfunding' a INSTALLED_APPS.
2.	Configurar rutas de medios (imágenes) al final del archivo:
Python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
________________________________________
3. Base de Datos y Modelos
Definición de las tablas en crowdfunding/models.py siguiendo el diseño sugerido .
•	Category: Nombre y descripción.
•	Campaign: Título, meta, fechas, imagen y relación con Categoría.
•	Donation: Relación con Usuario y Campaña, monto y comentario.
Comandos de Migración: Para crear las tablas en SQLite:
Bash
python manage.py makemigrations
python manage.py migrate
________________________________________
4. Panel de Administración (Backend)
4.1. Configuración (admin.py)
Registramos los modelos para que el superusuario pueda gestionarlos desde /admin/ .
4.2. Crear Superusuario
Bash
python manage.py createsuperuser
________________________________________
5. Desarrollo del Frontend (Vistas y Templates)
5.1. URLs y Rutas
Configuración en crowdfunding/urls.py para conectar las vistas con las direcciones web .
•	/: Inicio (Lista de campañas).
•	/campana/<id>: Detalle y donación.
•	/accounts/: Autenticación.
•	/mis-donaciones/: Historial del usuario.
5.2. Vistas Principales (views.py)
•	index: Lista campañas con activa=True.
•	detalle_campana: Muestra progreso, lista donantes y procesa el formulario de donación.
•	mis_donaciones: Filtra donaciones por request.user.
•	Funciones Admin: crear_campana, editar_campana, eliminar_campana protegidas con decorador @user_passes_test .
5.3. Templates Clave (HTML + Bootstrap)
•	index.html: Muestra tarjetas de campañas y menú de navegación dinámico (cambia si eres admin o usuario).
•	detalle.html:
o	Barra de progreso visual.
o	Formulario de Donación: Incluye validación de números negativos.
o	Modal de Pago: Simulación con JavaScript de ingreso de tarjeta de crédito.
•	mis_donaciones.html: Tabla resumen del historial de aportes del usuario.
________________________________________
6. Funcionalidades Avanzadas Implementadas
6.1. Validación de Seguridad
En forms.py, se implementó el método clean_monto para evitar donaciones con valores negativos o cero.
6.2. Simulación de Pasarela de Pago
Se desarrolló un flujo donde al hacer clic en "Donar", se abre un Modal (Pop-up) solicitando datos de tarjeta. Estos datos son visuales y no se guardan, cumpliendo el requisito de "simular" el pago sin una pasarela real.
6.3. CRUD Propio para el Administrador
Además del admin de Django, se crearon formularios web para que el administrador pueda:
•	Crear nuevas campañas desde la web (crear_campana.html).
•	Editar y Eliminar campañas y categorías desde botones específicos en la interfaz.
________________________________________
7. Instrucciones de Ejecución
Para levantar el proyecto en cualquier máquina:
1.	Asegurarse de tener el entorno virtual activo.
2.	Ejecutar el servidor:
Bash
python manage.py runserver
3.	Abrir el navegador en: http://127.0.0.1:8000/
Credenciales de Prueba:
•	Admin: (El usuario creado con createsuperuser).
•	Funder: Registrarse desde el botón "Registrarse" en la web.
