from django.db import models

class Dispositivo(models.Model):
    """
    Entidad de Hardware (Nodo de Control).
    
    Representa la unidad física de cómputo (Wemos D1, ESP32, Raspberry Pi) 
    desplegada en terreno. Utiliza el chip_id como identificador primario 
    para el handshake con la API.
    """
    chip_id = models.SlugField(
        max_length=50, 
        unique=True, 
        db_index=True,
        help_text="ID único del hardware (ej: MAC address o chip ID del fabricante)"
    )
    nombre_placa = models.CharField(
        max_length=100, 
        help_text="Nombre descriptivo para humanos (ej: Nodo Tanque Ácido)"
    )
    ubicacion = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Ubicación física en planta (ej: Sector Lixiviación)"
    )

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "1. Dispositivos"

    def __str__(self):
        return f"{self.nombre_placa} [{self.chip_id}]"


class Sensor(models.Model):
    """
    Entidad de Instrumentación (Punto de Medición).
    
    Define un transductor específico conectado a un puerto GPIO del dispositivo.
    Cada sensor debe tener un 'slug' único que se utiliza en las rutas URL 
    del Dashboard para el filtrado de series de tiempo.
    """
    dispositivo = models.ForeignKey(
        Dispositivo, 
        on_delete=models.CASCADE, 
        related_name='sensores'
    )
    nombre = models.CharField(
        max_length=100, 
        help_text="Nombre del punto de medida (ej: Flujo Entrada)"
    )
    slug = models.SlugField(
        max_length=100, 
        unique=True, 
        db_index=True,
        help_text="ID técnico usado por el Dashboard (ej: flujo_ent)"
    )
    pin_conexion = models.IntegerField(
        help_text="GPIO físico utilizado en el microcontrolador"
    )
    tipo = models.CharField(
        max_length=50, 
        default="DHT11", 
        help_text="Modelo del sensor (ej: DHT22, DS18B20, PT100)"
    )

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "2. Sensores"
        # Restricción técnica: Evita que dos sensores se mapeen al mismo pin físico en una placa
        constraints = [
            models.UniqueConstraint(
                fields=['dispositivo', 'pin_conexion'], 
                name='unique_pin_per_device'
            )
        ]

    def __str__(self):
        return f"{self.nombre} ({self.slug}) en {self.dispositivo.nombre_placa}"


class Lectura(models.Model):
    """
    Entidad de Telemetría (Serie Temporal).
    
    Almacena el registro histórico de las magnitudes medidas. Incluye 
    indexación en el timestamp para optimizar las consultas de series 
    de tiempo requeridas por Chart.js.
    """
    sensor = models.ForeignKey(
        Sensor, 
        on_delete=models.CASCADE, 
        related_name='lecturas'
    )
    tipo = models.CharField(
        max_length=30, 
        default="Temperatura",
        help_text="Unidad de medida (ej: Presión, Voltaje, Corriente)"
    )
    valor = models.FloatField(
        help_text="Valor numérico de la medición"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, 
        db_index=True,
        help_text="Fecha y hora de recepción del dato (UTC-4 para Chile)"
    )

    class Meta:
        verbose_name = "Lectura"
        verbose_name_plural = "3. Lecturas"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sensor.slug} | {self.valor} | {self.timestamp.strftime('%d/%m %H:%M')}"