"""
Módulo de Simulación de Telemetría IoT para Validación de Backend.

Este script actúa como un gemelo digital (Digital Twin) de un microcontrolador 
Wemos D1/ESP32. Genera señales sintéticas basadas en una función senoidal 
con ruido gaussiano para simular comportamientos térmicos industriales reales, 
permitiendo estresar la API REST y validar la visualización en el Dashboard.

Librerías Necesarias (Dependencias):
----------------------------------
1. requests:  Manejo de protocolos HTTP (POST/GET).
              Instalación: `pip install requests`
2. python-dotenv: Gestión de variables de entorno (.env).
              Instalación: `pip install python-dotenv`
3. math:      Funciones trigonométricas para modelamiento de señales. (Nativa)
4. random:    Generación de ruido estocástico para realismo físico. (Nativa)
5. pathlib:   Manipulación de rutas de archivos de forma agnóstica al SO. (Nativa)

Uso:
----
Asegúrese de tener el contenedor de la API corriendo y un archivo .env en la 
raíz del proyecto con las claves API_URL y CHIP_ID configuradas.

Ejecución en Linux: `python tools/sensor_simulador.py`
"""

import os
import time
import math
import random
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Cargar configuración desde la raíz del proyecto
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- CONFIGURACIÓN TÉCNICA ---
API_URL = os.getenv('API_URL', "http://localhost:8000/api/sensores/lecturas/")
CHIP_ID = os.getenv('CHIP_ID', "16777215")
SENSOR_SLUG = "temperatura-pieza"  # Asegúrate que coincida con el Admin de Django

# Parámetros de la Señal (Simulación Física)
INTERVALO = 10       # segundos
BASE_TEMP = 25.0     # Temperatura media
AMPLITUD = 5.0       # Oscilación térmica
RUIDO_SIGMA = 0.2    # Desviación del ruido

def generar_lectura_realista(paso):
    """Simula una curva térmica con ruido de medición"""
    # Función seno para simular el ciclo del día/noche o clima
    oscilacion = AMPLITUD * math.sin(paso / 10) 
    ruido = random.normalvariate(0, RUIDO_SIGMA)
    return round(BASE_TEMP + oscilacion + ruido, 2)

def iniciar_simulador():
    print(f"🚀 Simulador Industrial Activo | Sensor: {SENSOR_SLUG}")
    print(f"📡 Enviando a: {API_URL}\n" + "-"*45)
    
    session = requests.Session()
    paso = 0

    try:
        while True:
            valor = generar_lectura_realista(paso)
            
            payload = {
                "chip_id": CHIP_ID,
                "sensor_slug": SENSOR_SLUG,
                "tipo": "Temperatura",
                "valor": valor
            }

            try:
                response = session.post(API_URL, json=payload, timeout=5)
                timestamp = datetime.now().strftime("%H:%M:%S")

                if response.status_code == 201:
                    print(f"[{timestamp}] Transmisión OK: {valor:>5}°C | Params: sin({paso/10:.1f})")
                else:
                    print(f"[{timestamp}] ⚠️ ERROR {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"❌ FALLO DE CONEXIÓN: Verifique que el contenedor Django esté corriendo.")

            paso += 1
            time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\n\n🔌 Simulador detenido por el usuario. Cerrando comunicación...")

if __name__ == "__main__":
    iniciar_simulador()
