from rest_framework import generics, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lectura, Sensor, Dispositivo
from .serializers import (
    LecturaSerializer, 
    SensorSerializer, 
    DispositivoConSensoresSerializer
)

class LecturaListCreateView(generics.ListCreateAPIView):
    """
    Gestiona la ingesta de telemetría y la consulta de series de tiempo.
    
    Optimizaciones:
    - Filtra por metadatos (slug, tipo) antes de truncar la serie.
    - select_related('sensor') para evitar el problema de consultas N+1.
    """
    serializer_class = LecturaSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    
    # Configuración de filtros dinámicos (django-filter)
    filterset_fields = {
        'sensor__slug': ['exact'],
        'tipo': ['exact'],
    }

    def get_queryset(self):
        """
        Retorna el flujo de lecturas ordenado cronológicamente de forma descendente.
        Se mantiene abierto (sin recortes) para permitir el filtrado posterior.
        """
        return Lectura.objects.select_related('sensor').all().order_by('-timestamp')

    def list(self, request, *args, **kwargs):
        """
        Sobrescribe la salida para el Dashboard.
        Aplica filtros sobre el histórico total y recorta a los últimos 50 registros
        para optimizar el ancho de banda y la renderización en Chart.js.
        """
        # Aplicamos la lógica de filtrado de la URL
        queryset = self.filter_queryset(self.get_queryset())
        
        # Slicing: Solo los 50 eventos más recientes del sensor filtrado
        last_50_readings = queryset[:50]

        serializer = self.get_serializer(last_50_readings, many=True)
        return Response(serializer.data)


class SensorListView(generics.ListAPIView):
    """
    Catálogo técnico de sensores.
    
    Uso: Provee metadatos como pines de conexión y tipos de sensores.
    Optimización: select_related('dispositivo') para traer el nombre del hardware dueño.
    """
    queryset = Sensor.objects.select_related('dispositivo').all()
    serializer_class = SensorSerializer
    permission_classes = [permissions.AllowAny]


class DispositivoListView(generics.ListAPIView):
    """
    Genera la estructura jerárquica para el menú de navegación (Dashboard).
    
    Uso: Retorna Dispositivos con sus Sensores anidados.
    Optimización: prefetch_related('sensores') para cargar todas las relaciones 
    inversas en una sola consulta adicional (Reverse Foreign Key).
    """
    queryset = Dispositivo.objects.prefetch_related('sensores').all()
    serializer_class = DispositivoConSensoresSerializer
    permission_classes = [permissions.AllowAny]