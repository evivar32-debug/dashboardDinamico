from django.contrib import admin
from .models import Dispositivo, Sensor, Lectura

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    # Añadimos la ubicación para tener contexto físico del hardware
    list_display = ('nombre_placa', 'chip_id', 'ubicacion')
    search_fields = ('nombre_placa', 'chip_id', 'ubicacion')
    list_filter = ('ubicacion',)

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    # list_select_related evita 1 query extra por cada fila para traer el nombre del dispositivo
    list_select_related = ('dispositivo',)
    list_display = ('nombre', 'slug', 'dispositivo', 'pin_conexion', 'tipo')
    list_filter = ('dispositivo', 'tipo')
    search_fields = ('nombre', 'slug', 'dispositivo__nombre_placa')
    # El slug se puede autocompletar desde el nombre para ahorrar tipeo
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(Lectura)
class LecturaAdmin(admin.ModelAdmin):
    # Optimización crítica: traemos los datos del sensor y dispositivo en un solo JOIN
    list_select_related = ('sensor', 'sensor__dispositivo')
    
    list_display = ('get_dispositivo', 'sensor', 'tipo', 'valor', 'timestamp')
    list_filter = ('sensor__dispositivo', 'sensor', 'tipo', 'timestamp')
    search_fields = ('sensor__slug', 'sensor__nombre', 'tipo')
    
    # Hacemos que las lecturas sean de "solo lectura" en el admin para integridad de datos
    readonly_fields = ('sensor', 'tipo', 'valor', 'timestamp')

    # Método para mostrar el dispositivo dueño de la lectura en la lista
    @admin.display(description='Dispositivo', ordering='sensor__dispositivo')
    def get_dispositivo(self, obj):
        return obj.sensor.dispositivo.nombre_placa

# Configuración visual del Panel
admin.site.site_header = "Panel de Control IoT - Monitoreo Industrial"
admin.site.site_title = "IoT Admin"
admin.site.index_title = "Gestión de Telemetría y Hardware"