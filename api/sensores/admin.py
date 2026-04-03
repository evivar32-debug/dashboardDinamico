from django.contrib import admin
from .models import Dispositivo, Sensor, Lectura

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    # Campos que existen en tu modelo Dispositivo
    list_display = ('nombre_placa', 'chip_id')
    search_fields = ('nombre_placa', 'chip_id')

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    # Eliminamos 'ubicacion' y 'fecha_instalacion' porque ya no están en tu modelo Sensor
    list_display = ('nombre', 'dispositivo', 'pin_conexion', 'tipo')
    list_filter = ('dispositivo', 'tipo')
    search_fields = ('nombre',)

@admin.register(Lectura)
class LecturaAdmin(admin.ModelAdmin):
    # Reemplazamos 'temperatura' y 'humedad' por 'tipo' y 'valor'
    list_display = ('sensor', 'tipo', 'valor', 'timestamp')
    list_filter = ('sensor', 'tipo', 'timestamp')
    # Esto te permitirá buscar lecturas por el nombre del sensor o el chip_id
    search_fields = ('sensor__nombre', 'tipo')