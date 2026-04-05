# 🚀 IoT Control Center - Monitoreo Industrial en Tiempo Real

Sistema integral de telemetría diseñado para la visualización y registro de variables críticas de sensores conectados a microcontroladores (ESP32/Wemos D1). El proyecto combina la potencia de **Django** en el backend con una interfaz dinámica en **JavaScript** y **Chart.js**.


## 🛠️ Arquitectura del Sistema

El sistema sigue un modelo de comunicación desacoplado:



1. **Capa de Hardware:** Sensores conectados a microcontroladores que envían datos vía HTTP/REST o Modbus.
2. **Capa de Datos (API):** Backend en **Python/Django** con **Django REST Framework (DRF)** y base de datos SQL (**PostgreSQL**).
3. **Capa de Presentación:** Dashboard interactivo construido con HTML5 semántico, CSS3 (Flexbox) y JS Vanilla.


## 📋 Características Principales



* **Dashboard Dinámico:** Visualización de series de tiempo mediante **Chart.js** con suavizado de curva (Bézier).
* **KPIs en Tiempo Real:** Cálculo instantáneo de valores máximos y última lectura por sesión.
* **Gestión de Dispositivos:** Navegación jerárquica por Placas y Sensores vinculados.
* **Log de Eventos:** Historial de las últimas 10 lecturas con estados de recepción.
* **Diseño Industrial:** Interfaz optimizada para centros de control (Low-fatigue UI) con scroll independiente.
* **Contenerización:** Preparado para despliegue con **Docker** y **Docker Compose**.


## 🚀 Tecnologías Utilizadas



* **Backend:** Python 3.x, Django 5.x, Django REST Framework.
* **Frontend:** JavaScript (ES6+), CSS3 (Custom Properties & Flexbox), HTML5.
* **Base de Datos:** PostgreSQL.
* **DevOps:** Docker, CachyOS (Linux), Fish Shell.
* **Herramientas de Desarrollo:** Micro Editor, Visual Studio Code, Git.


## 🔧 Instalación y Configuración


### Requisitos Previos



* Python 3.10+
* Docker & Docker Compose (opcional para contenedores)


### Pasos de Instalación



1. **Clonar el repositorio:** \
git clone https://github.com/evivar32-debug/dashboardDinamico.git \
cd dashboardDinamico \

2. **Configurar el entorno virtual:** \
docker compose up -–build \

3. **Ejecutar Migraciones:** \
docker compose python manage.py makemigration \
docker compose python manage.py migrate \

4. **Levantar Frontend: \
**-Usar extensión ‘live server’ de Visual Studio Code (ya configurado) o usar otra herramienta de preferencia (se debe configurar archivos de Django correspondientes de puertos a usar) \



## 🛡️ Prácticas de Ingeniería Aplicadas



* **Zero-Footprint Styling:** Uso de flex-shrink: 0 para prevenir colapso de componentes en visualizaciones críticas.
* **Async/Await Flow:** Manejo asíncrono de peticiones para evitar bloqueos en el hilo principal del navegador.
* **Memory Management:** Optimización del ciclo de vida del gráfico para prevenir fugas de memoria en monitoreo 24/7.



---
**Desarrollado por:** Elvis Vivar - *Ingeniero Electrónico* 🇨🇱
