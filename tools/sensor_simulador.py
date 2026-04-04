import requests
import random
import time
from datetime import datetime

# Configuración
API_URL = "http://localhost:8000/api/sensores/lecturas/"
CHIP_ID = "16777215"  

# --- CAMBIO IMPORTANTE AQUÍ ---
# Usamos el SLUG que creaste en el Admin de Django
SENSOR_SLUG = "temperatura-pieza" 

INTERVALO_SEGUNDOS = 10 
TEMP_MIN = 15.0
TEMP_MAX = 35.0

def simular_envio():
    print(f"--- Simulador IoT (ID: {SENSOR_SLUG}) | Intervalo: {INTERVALO_SEGUNDOS}s ---")
    
    while True:
        temp_random = round(random.uniform(TEMP_MIN, TEMP_MAX), 2)
        
        # Estructura del JSON actualizada
        payload = {
            "chip_id": CHIP_ID,
            "sensor_slug": SENSOR_SLUG, # <--- Cambiado de 'sensor_nombre' a 'sensor_slug'
            "tipo": "Temperatura",
            "valor": temp_random
        }

        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 201:
                ahora = datetime.now().strftime("%H:%M:%S")
                print(f"[{ahora}] Transmisión Exitosa: {temp_random}°C")
            else:
                # Si te da error aquí, revisa que el SLUG exista en el Admin
                print(f"Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("CRÍTICO: No hay conexión con el servidor. ¿Docker está UP?")

        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    simular_envio()