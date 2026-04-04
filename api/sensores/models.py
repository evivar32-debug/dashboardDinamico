from django.db import models

class Dispositivo(models.Model):
    """Representa la unidad física (Wemos D1, ESP32, etc.)"""
    chip_id = models.SlugField(
        max_length=50, 
        unique=True, 
        db_index=True,
        help_text="ID único del hardware (ej: 16777215)"
    )
    nombre_placa = models.CharField(max_length=100, help_text="Ej: Tablero Control Norte")
    ubicacion = models.CharField(max_length=100, blank=True, help_text="Ej: Sala de Máquinas")

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "1. Dispositivos"

    def __str__(self):
        return f"{self.nombre_placa} [{self.chip_id}]"


class Sensor(models.Model):
    """Representa un componente conectado a un pin específico del dispositivo"""
    dispositivo = models.ForeignKey(
        Dispositivo, 
        on_delete=models.CASCADE, 
        related_name='sensores'
    )
    nombre = models.CharField(max_length=100, help_text="Ej: Temperatura Motor")
    slug = models.SlugField(
        max_length=100, 
        unique=True, 
        db_index=True,
        help_text="Identificador técnico (ej: temp_motor)"
    )
    pin_conexion = models.IntegerField(help_text="Pin GPIO (ej: 5 para D1)")
    tipo = models.CharField(max_length=50, default="DHT11", help_text="Ej: DHT22, PT100, NTC")

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "2. Sensores"
        # Regla de Oro: Un pin solo puede tener un sensor EN ESA PLACA específica
        constraints = [
            models.UniqueConstraint(fields=['dispositivo', 'pin_conexion'], name='unique_pin_per_device')
        ]

    def __str__(self):
        return f"{self.nombre} ({self.slug}) en {self.dispositivo.nombre_placa}"


class Lectura(models.Model):
    """Registro histórico de telemetría"""
    sensor = models.ForeignKey(
        Sensor, 
        on_delete=models.CASCADE, 
        related_name='lecturas'
    )
    tipo = models.CharField(max_length=30, default="Temperatura")
    valor = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Lectura"
        verbose_name_plural = "3. Lecturas"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sensor.slug} | {self.valor} | {self.timestamp.strftime('%d/%m %H:%M')}"