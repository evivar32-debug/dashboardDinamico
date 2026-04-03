import requests
import random
import time
from datetime import datetime

# Configuración
API_URL = "http://localhost:8000/api/sensores/lecturas/"
CHIP_ID = "16777215"  # Nombre del dispositivo a emular (serial), asegurarse que este creada en la base de datos  
SENSOR_NOMBRE = "Temperatura Pieza" # Nombre del sensor a emular, asegurarse que este creado en la base de datos
INTERVALO_SEGUNDOS = 10 # Intervalo de envíos en segundos
TEMP_MIN = 15.0
TEMP_MAX = 35.0
HUM_MIN = 40.0
HUM_MAX = 80.0

def simular_envio():
    print(f"--- Iniciando Simulador de Sensor (Intervalo: {INTERVALO_SEGUNDOS}s) ---")
    
    while True:
        # Generar datos aleatorios según el rango
        temp_random = round(random.uniform(TEMP_MIN, TEMP_MAX), 2)
        hum_random = round(random.uniform(HUM_MIN, HUM_MAX), 2) # Humedad (a implementar en el futuro)
        
        # Estructura del JSON que definimos en el Serializer
        payload = {
            "chip_id": CHIP_ID,
            "sensor_nombre": SENSOR_NOMBRE,
            "tipo": "Temperatura",
            "valor": temp_random
        }

        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 201:
                ahora = datetime.now().strftime("%H:%M:%S")
                print(f"[{ahora}] Éxito: {temp_random}°C enviado correctamente.")
            else:
                print(f"Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("Error: No se pudo conectar con el servidor Django. ¿Está Docker corriendo?")

        # Esperar el intervalo de tiempo
        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    simular_envio()