from django.db import models

class Dispositivo(models.Model):
    # El ID único de la placa Wemos (ChipID)
    chip_id = models.SlugField(max_length=50, unique=True, help_text="ID único del hardware (ej: 16777215)")
    nombre_placa = models.CharField(max_length=100, help_text="Ej: Nodo Central Tablero")
    
    def __str__(self):
        return f"{self.nombre_placa} [{self.chip_id}]"

class Sensor(models.Model):
    # Un dispositivo puede tener muchos sensores
    dispositivo = models.ForeignKey(Dispositivo, default=None, on_delete=models.CASCADE, related_name='sensores')
    
    nombre = models.CharField(max_length=100, help_text="Ej: Temp Motor, Humedad Ambiente")
    pin_conexion = models.IntegerField(default=0, help_text="Pin GPIO usado en la Wemos")
    tipo = models.CharField(max_length=50, default="DHT11")

    def __str__(self):
        return f"{self.nombre} (en {self.dispositivo.nombre_placa})"

class Lectura(models.Model):
    # Relación: Si se borra el sensor, se borran sus lecturas (CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='lecturas')
    
    tipo = models.CharField(max_length=30, default="Temperatura") # Temperatura, Humedad, presion, etc. 
    valor = models.FloatField()
    
    # auto_now_add es clave para filtrar por días/semanas/meses después
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ordenamos por defecto de la más reciente a la más antigua
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sensor.nombre} - {self.tipo}: {self.valor} | {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
    