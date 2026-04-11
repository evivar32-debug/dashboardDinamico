
# 🚀 IoT Control Center - Monitoreo Industrial en Tiempo Real

Sistema integral de telemetría diseñado para la visualización y registro de variables críticas en entornos industriales. Este ecosistema permite la transición hacia la **Minería 4.0**, integrando datos de campo desde microcontroladores (ESP32/PLC) hacia una plataforma analítica robusta.


## 


🛠️ Arquitectura del Sistema (IT/OT Convergence)

El proyecto utiliza un modelo de comunicación desacoplado y escalable:



1. **Capa de Hardware:** Captura de datos mediante sensores analógicos/digitales y transmisión vía HTTP/REST.
2. **Capa de Servicio (Backend):** API REST construida con **Python/Django** y **DRF**, gestionando la persistencia en **PostgreSQL**.
3. **Capa de Presentación (Frontend):** Dashboard SPA (Single Page Application) dinámico con **Chart.js** y **Vanilla JS**.


## 


📋 Características Principales



* **Seguridad RBAC:** Control de acceso basado en roles (Administrador vs. Operador) con validación mediante **JWT**.
* **Visualización Predictiva:** Gráficos de series de tiempo con suavizado de curva (Bézier) y manejo de ruido estocástico.
* **KPIs Industriales:** Cálculo en tiempo real de valores máximos, mínimos y promedios por sesión.
* **Gestión de Activos:** Interfaz administrativa para el alta/baja de sensores y dispositivos de campo.
* **Contenerización:** Despliegue agnóstico al SO mediante **Docker Compose**, optimizado para entornos Linux (**CachyOS**).


## 

🔧 Instalación y Despliegue Rápido


### Requisitos Previos



* Docker & Docker Compose (Recomendado)
* Python 3.10+ (Para ejecución local del simulador)


### Pasos para el despliegue del Stack



1. **Clonar y configurar:** 
```Bash 
git clone https://github.com/evivar32-debug/dashboardDinamico.git  
cd dashboardDinamico 
# Configura tu .env basado en el .env.example 
```
2. **Levantar infraestructura:** 
```Bash 
docker compose up --build -d 
```
3. **Inicializar Base de Datos:** 
```Bash 
# Ejecutar migraciones 
docker compose exec api python manage.py migrate 
 ```
4. **Crear cuenta administrativa** 
```bash
docker compose exec api python manage.py createsuperuser 
```
5. **Simular Datos (Opcional):** 
Para probar el sistema sin hardware físico, ejecuta el simulador incluido: 
```Bash 
python tools/sensor_simulador.py
```



## 


🛡️ Prácticas de Ingeniería y Performance



* **Robustez de Datos:** Implementación de modelos personalizados en Django para el manejo de **RUT** e identificadores de hardware únicos (**Chip ID**).
* **Memory Management:** Optimización del ciclo de vida de los objetos en el Frontend para prevenir fugas de memoria en monitoreo 24/7.
* **Diseño Low-Fatigue:** Interfaz de usuario de alto contraste y baja fatiga visual, diseñada para centros de control operativos.


## 


🛠️ Stack Tecnológico


<table>
  <tr>
   <td><strong>Backend</strong>
   </td>
   <td><strong>Frontend</strong>
   </td>
   <td><strong>DevOps & Herramientas</strong>
   </td>
  </tr>
  <tr>
   <td>Python / Django
   </td>
   <td>JavaScript (ES6+)
   </td>
   <td>Docker / Docker Compose
   </td>
  </tr>
  <tr>
   <td>Django REST Framework
   </td>
   <td>Chart.js
   </td>
   <td>PostgreSQL
   </td>
  </tr>
  <tr>
   <td>JWT Authentication
   </td>
   <td>CSS3 (Custom Vars)
   </td>
   <td>Linux (CachyOS) / Fish Shell
   </td>
  </tr>
</table>



### 


👤 Autor

**Elvis Vivar** - *Ingeniero Electrónico*
