from rest_framework import generics, permissions
from .models import Lectura, Sensor, Dispositivo
from .serializers import (
    LecturaSerializer, 
    SensorSerializer, 
    DispositivoSerializer, 
    DispositivoConSensoresSerializer
)

class LecturaListCreateView(generics.ListCreateAPIView):
    """
    Vista para recibir telemetría (POST) y listar historial filtrado (GET).
    Optimizado para minimizar latencia en el Dashboard.
    """
    serializer_class = LecturaSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Optimizamos trayendo Sensor y Dispositivo en una sola consulta SQL
        queryset = Lectura.objects.select_related('sensor', 'sensor__dispositivo').all()
        
        # Filtro por slug enviado desde el Dashboard (ej: ?sensor_nombre=temp_motor)
        sensor_slug = self.request.query_params.get('sensor_nombre')
    
        if sensor_slug:
            queryset = queryset.filter(sensor__slug=sensor_slug)
            
        # Retornamos las últimas 50 lecturas para el gráfico en tiempo real
        return queryset.order_by('-timestamp')[:50]

class SensorListView(generics.ListAPIView):
    """Lista todos los sensores registrados y sus metadatos"""
    queryset = Sensor.objects.select_related('dispositivo').all()
    serializer_class = SensorSerializer
    permission_classes = [permissions.AllowAny]
    
class DispositivoListView(generics.ListAPIView):
    """
    Vista jerárquica para construir el menú lateral:
    Dispositivo -> [Lista de Sensores]
    """
    # prefetch_related es ideal para relaciones 'muchos a uno' (Reverse FK)
    queryset = Dispositivo.objects.prefetch_related('sensores').all()
    serializer_class = DispositivoConSensoresSerializer
    permission_classes = [permissions.AllowAny]