# 🚀 Sistema de Gestión y Monitoreo IoT Industrial

## **Introducción**


### Resumen del Proyecto y Aplicación Laboral

El presente proyecto consiste en el desarrollo de una plataforma **IoT (Internet of Things)** diseñada para el monitoreo y gestión de variables críticas en entornos industriales en tiempo real. El sistema integra nodos de adquisición de datos (Hardware), un motor de procesamiento y gestión de datos (Backend) y una interfaz de visualización dinámica (Frontend).

En el ámbito laboral actual, este sistema permite la transición hacia la **Minería e Industria 4.0**, proporcionando una solución escalable para la supervisión de salas eléctricas, centros de datos o procesos de instrumentación. Su aplicación directa permite reducir los tiempos de respuesta ante fallas, optimizar el mantenimiento preventivo mediante el análisis de tendencias térmicas y asegurar la continuidad operativa de activos críticos sin necesidad de supervisión humana constante en terreno.

### Motivación y Convergencia de Disciplinas

Mi principal motivación para el desarrollo de esta arquitectura es la **convergencia técnica**. He buscado plasmar de manera tangible el conocimiento adquirido durante el programa de **Desarrollo de Aplicaciones Fullstack Python Trainee**, integrándolo sinérgicamente con mi trayectoria previa como **Ingeniero Electrónico** especializado en electricidad y automatización industrial.

Este proyecto representa el puente entre el mundo del control físico (PLC, DCS, Instrumentación) y el mundo del desarrollo de software moderno. La capacidad de entender cómo fluye un electrón desde un sensor en una planta industrial hasta convertirse en un dato procesado en una API de Python es el pilar de mi perfil profesional.

### Enfoque Profesional y Arquitectura Moderna

Para garantizar la robustez y escalabilidad de la solución, se ha aplicado un enfoque de ingeniería moderno, alejándose de los sistemas monolíticos tradicionales y adoptando estándares de la industria de software actual:

- **Arquitectura Desacoplada (Microservicios):** El sistema se ha diseñado separando estrictamente el **Backend** (Django REST Framework) del **Frontend** y, próximamente, del **Hardware** (Edge Computing). Esto permite que cada capa evolucione y se mantenga de forma independiente.
    
- **Seguridad y Control de Acceso:** Se ha implementado un sistema de autenticación basado en **JWT (JSON Web Tokens)** para asegurar las comunicaciones entre servicios. Además, la plataforma cuenta con una **gestión de privilegios por niveles**, diferenciando roles de administración de hardware frente a roles de visualización de datos, asegurando que solo personal autorizado pueda modificar la infraestructura.
    
- **Integridad de Datos y Estándares:** Haciendo uso de contenedores con **Docker**, bases de datos relacionales robustas y validaciones personalizadas (como el manejo de RUT y correos corporativos), el proyecto cumple con las recomendaciones técnicas de desarrollo profesional de clase mundial. Se seleccionó **PostgreSQL** como motor de base de datos relacional debido a su robustez en el manejo de tipos de datos complejos y su excelente rendimiento en consultas de series temporales (lecturas de sensores). Además, su estricto cumplimiento de ACID garantiza la integridad de los registros de auditoría y de usuarios (RUT/Email).
### Proyección de Escalabilidad e Integración Minera

Un pilar fundamental de este diseño es su capacidad de **escalabilidad horizontal y vertical**. A diferencia de los sistemas de monitoreo cerrados, esta arquitectura permite el crecimiento orgánico desde un único nodo de control hasta una red de cientos de sensores distribuidos en una planta minera. Gracias al uso de **Docker**, el backend puede ser desplegado en clústeres que soporten un alto volumen de peticiones concurrentes, mientras que la base de datos está optimizada mediante relaciones de integridad para manejar históricos masivos de telemetría.

En términos de integración, el enfoque de **API REST** permite que estos datos no solo alimenten el Dashboard propio, sino que puedan ser consumidos por sistemas de nivel superior como **ERP (SAP)** o **MES (Manufacturing Execution Systems)**. Esta visión prepara al proyecto para enfrentar los desafíos de la **Minería 4.0**, donde la interoperabilidad entre el hardware de campo y las capas de decisión empresarial es el factor crítico para la eficiencia operativa.


## **Instalación y Configuración del Entorno**

---


Para asegurar la replicabilidad del sistema en cualquier entorno (Windows, Linux o macOS), se ha contenedorizado la aplicación completa.

**Requisitos previos:**

- Python 3.10+ (para ejecución local/scripts de hardware).
    
- **Docker & Docker Compose** (obligatorio para el despliegue del stack).
    

#### 1. Clonar el Repositorio

Se recomienda el uso de Git para mantener la integridad de las ramas de desarrollo:
```bash
git clone https://github.com/evivar32-debug/dashboardDinamico.git 
cd dashboardDinamico
```

#### 2. Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto. Este archivo es crítico para la seguridad, ya que separa las credenciales del código fuente. Puedes usar como base el archivo `.env.example`:
```python
# === Django Core ===
DEBUG=True
SECRET_KEY=cambiame_por_una_llave_segura
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# === Base de Datos ===
DB_NAME=iot_db
DB_USER=admin
DB_PASSWORD=tu_password_seguro
DB_HOST=db
DB_PORT=5432 

# === Seguridad CORS ===
CORS_ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500

# === Configuración Simulación Hardware ===
API_URL=http://localhost:8000/api/sensores/lecturas/
```
#### 3. Despliegue con Docker

Construye y levanta los servicios (API + Base de Datos). El flag `--build` garantiza que se instalen todas las dependencias de Python listadas en `requirements.txt`:
```bash
docker compose up --build -d
```
#### 4. Inicialización de Base de Datos y Accesos

Una vez que los contenedores estén en ejecución, prepara el esquema de datos y crea la cuenta de administración:
```bash
# Ejecutar migraciones
docker compose exec api python manage.py migrate
```

## **Funcionamiento del proyecto**

Para demostrar el funcionamiento del proyecto se realizara una demostración de una lectura simulada de temperatura, el enfoque sera de tipo industrial.

> [!NOTA]
> En caso de presentar problemas al hacer los siguientes pasos, se recomienda realizar un reset del contenedor de Docker con: `docker compose down` y `docker compose up`

### 1. Crear SuperUsuario
El primer paso es crear un SuperUsuario (SuperUser) el cual sera un Administrador que tendrá privilegios para agregar y/o eliminar sensores, dispositivos (microcontroladores ESP32, PLC etc.) y agregar otros usuarios de tipo Operador el cual solo podrá realizar lecturas de los valores de los sensores.
Para crear un SuperUser se debe realizar el comando:
```bash
docker compose exec api python manage.py createsuperuser 
```
Se preguntara por los siguientes datos:
- Correo electrónico 
- Nombre completo
- RUT
- Password (pide escribir 2 veces)
Una vez realizado se mostrara en la terminal : `Superuser created successfully.`


> [!NOTA] 
> La primera vez se debe realizar de esta manera, mas adelante si se desea crear otro usuario o SuperUsuario, se puede realizar directamente desde el administrador de Django.


### 2. Crear dispositivo y sensor
Una vez realizado nuestro SuperUsuario, debemos dirigirnos a nuestro navegador con la dirección [http://localhost:8000/admin](http://localhost:8000/admin).

![login_django](/Docs/img/login_django.png)

Una vez dentro, debemos ingresar con los datos de Correo electrónico y Contraseña escritas anteriormente. Al loguearnos nos encontraremos con el panel principal.

![menu_django](/Docs/img/menu_django.png)

Creamos un nuevo Dispositivo haciendo click en Añadir, se creara un dispositivo con las siguientes denominaciones:

![add_disp](/Docs/img/add_disp.png)

Nos dirigimos a Añadir Sensor desde el menú lateral, al crear un sensor elegimos un dispositivo desde el menú despegable (estará listado nuestro dispositivo recién hecho)
y completar los campos restantes según nuestros requisitos.

![add_sensor](/Docs/img/add_sensor.png)

Habiendo realizado esto, ya tendremos incorporado un sensor a nuestro proyecto el cual se podrá visualizar en nuestra pagina Web.

### 3. Simulación y visualización de datos
Para visualizar nuestro proyecto en el navegador, se debe levantar nuestro Frontend, se utilizara la extensión de [Live Server](https://github.com/ritwickdey/vscode-live-server-plus-plus) de Visual Studio Code para esta demostracion, una vez levantado el Frontend, nos dirigiremos a [http://127.0.0.1:5500/web/index.html](http://127.0.0.1:5500/web/index.html).

![login_web](/Docs/img/login_web.png)

Ingresaremos con la cuenta hecha previamente, al ingresar podremos ver nuestro sensor creado:

![menu_web](/Docs/img/menu_web.png)

Como esta recién creado y no esta conectado a nada todavía, tendremos una lista vacía, por lo que simularemos valores gracias al programa incorporado en el proyecto en la carpeta **tools**, para usarlo se debe configurar los valores de `CHIP_ID` y `SENSOR_SLUG` segun lo que definimos anteriormente, en nuestro caso quedara:
```python
# --- CONFIGURACIÓN TÉCNICA ---
# El SENSOR_SLUG debe coincidir con el campo 'slug' creado en el Admin de Django
API_URL = os.getenv('API_URL', "http://localhost:8000/api/sensores/lecturas/")
CHIP_ID = "16777215" # ID único del hardware (ej. Dirección MAC)
SENSOR_SLUG = "temperatura-sala"
```

> [!Instalar dependencias de ser necesario:]
> 1. requests:  Manejo de protocolos HTTP (POST/GET).
>               Instalación: `pip install requests`
> 2. python-dotenv: Gestión de variables de entorno (.env).
>               Instalación: `pip install python-dotenv`
> 3. math:      Funciones trigonométricas para modelamiento de señales. (Nativa)
> 4. random:    Generación de ruido estocástico para realismo físico. (Nativa)
> 5. pathlib:   Manipulación de rutas de archivos de forma agnóstica al SO. (Nativa)

Arrancamos nuestro programa usando el comando:
```bash
python tools/sensor_simulador.py 
```
El programa nos comenzara a crear lecturas del sensor creado, se debe visualizar lo siguiente:
```
🚀 Simulador Industrial Activo | Sensor: temperatura-sala
📡 Enviando a: http://localhost:8000/api/sensores/lecturas/
---------------------------------------------
[19:46:52] Transmisión OK: 24.99°C | Params: sin(0.0)
[19:47:02] Transmisión OK: 25.05°C | Params: sin(0.1)
```
Al ir a nuestra pagina web, veremos que los datos se empiezan a visualizar:

![menu_datos](/Docs/img/menu_datos.png)

> [!TIP] **Sobre el Simulador:** 
El script en Python utiliza una función seno combinada con ruido aleatorio (`random`) para emular el comportamiento térmico real de una sala eléctrica, donde la temperatura oscila suavemente pero presenta pequeñas variaciones por interferencias o flujo de aire.


## **Gestión de Usuarios y Control de Acceso (RBAC)**

El sistema implementa un modelo de **Control de Acceso Basado en Roles (RBAC)**, lo que permite segregar funciones y minimizar riesgos operativos mediante la jerarquía de privilegios:

- **Perfil Operador:** Diseñado para personal de planta o monitoreo. Su alcance se limita a la **visualización de datos en tiempo real** y consulta de históricos. No posee acceso a la API de configuración ni al panel administrativo, garantizando que la configuración del hardware permanezca inalterada.
    
- **Perfil Administrador:** Orientado a ingenieros de soporte o jefes de área. Cuenta con privilegios extendidos para la gestión de activos (CRUD de sensores y dispositivos), auditoría de lecturas y administración de cuentas de usuario.
    

### Crear nueva cuenta
Para crear una nueva cuenta, se debe dirigir al login de [Admin](http://localhost:8000/admin/) de Django, iniciar sesión con una cuenta de administrador (debe ser un SuperUsuario o con privilegios de Staff) y hacer click en añadir Usuario:

![add_usuario](/Docs/img/add_usuario.png)

Completamos con los datos solicitados y damos los privilegios que tendrá el nuevo usuario, el campo '**Es staff**' es necesario si se quiere que la cuenta nueva tenga acceso al administrador de Django.
Una vez registrado ya se puede usar esta cuenta en la pagina web, para diferenciar entre un Operador y un Administrador, en la pagina web se mostrara una insignia con el nivel de privilegios correspondiente.

Ejemplo usuario nivel Operador:
![badge_operador](/Docs/img/badge_operador.png)

Ejemplo usuario nivel Administrador:
![badge_admin](/Docs/img/badge_admin.png)

> [!IMPORTANT] **Integridad del Sistema:** En la interfaz web, el sistema valida el token de autenticación y renderiza dinámicamente una **insignia de rango**. Esto no es solo un cambio estético; el Backend rechaza cualquier petición de modificación de datos (POST/PUT/DELETE) si el token no pertenece a un perfil con los permisos adecuados.

## **🛠️ Solución de Problemas Comunes (Troubleshooting)**


#### 1. Errores de Permisos en Docker (Linux)

Si al ejecutar `docker compose up` recibes un error de "Permission Denied", generalmente se debe a que tu usuario no pertenece al grupo `docker`.
**Solución:**
```bash
sudo usermod -aG docker $USER
# Luego cierra sesión y vuelve a entrar para aplicar los cambios.
```

#### 2. Conflicto de Puertos

Si recibes un error indicando que el puerto `8000` o `5432` ya está en uso, es probable que tengas una instancia local de Django o PostgresSQL corriendo fuera de Docker. **Solución:** Puedes cambiar los puertos externos en el archivo `docker-compose.yml`:
```yaml
ports:
  - "8080:8000" # Cambia el puerto de la API al 8080
```

#### 3. Error de Conexión a la Base de Datos

Si los logs de la API muestran `django.db.utils.OperationalError: (2002, "Can't connect to server")`, significa que la API intentó conectar antes de que la base de datos terminara de inicializarse. **Solución:** Reinicia el contenedor de la API para forzar un nuevo intento de conexión:
```bash
docker compose restart api
```

#### 4. Limpieza Total (Reset)

Si necesitas borrar todo y empezar desde cero (incluyendo los datos de la base de datos):
```bash
docker compose down -v
docker compose up --build
```
(El flag `-v` elimina los volúmenes de datos, permitiendo una instalación limpia).

## **Conclusiones y Proyección Técnica**

El desarrollo de este ecosistema de monitoreo industrial ha permitido validar la viabilidad de integrar tecnologías de **Desarrollo Fullstack** con la **Automatización Industrial**. El uso de un Backend robusto en **Django** y **PostgreSQL**, comunicado con un Frontend dinámico, ofrece una solución superior a los SCADAs tradicionales en términos de flexibilidad, seguridad y costos de licenciamiento.

### Logros Técnicos Destacados:

- **Convergencia IT/OT:** Se logró traducir señales de campo (simuladas con lógica física) en datos procesables mediante una API REST protegida por JWT.
    
- **Seguridad de Datos:** La implementación de roles (RBAC) asegura que la operación y la administración del sistema mantengan la integridad necesaria para entornos críticos como salas eléctricas.
    
- **Escalabilidad:** Gracias a la arquitectura de microservicios y la contenedorización con **Docker**, el sistema está preparado para transicionar de un entorno de pruebas a un despliegue en la nube o servidores locales de planta.
    

### Futuras Mejoras (Roadmap):

1. **Integración de Hardware Real:** Sustituir el simulador por nodos ESP32 físicos conectados vía RS485/Modbus.
    
2. **Notificaciones Críticas:** Implementar un servicio de alertas (vía Email o Telegram) cuando las lecturas superen umbrales críticos de temperatura u otra magnitud de medida.
    
3. **Análisis Predictivo:** Utilizar los datos históricos almacenados en Postgres para predecir fallas mediante algoritmos de Machine Learning.