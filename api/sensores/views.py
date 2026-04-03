from rest_framework import generics
from .models import Lectura
from .serializers import LecturaSerializer

from rest_framework import generics, permissions # <--- Importa permissions

class LecturaListCreateView(generics.ListCreateAPIView):
    """
    Vista para:
    - POST: Recibir lecturas de la Wemos D1.
    - GET: Listar las últimas lecturas para el Dashboard.
    """
    queryset = Lectura.objects.all()
    serializer_class = LecturaSerializer
    
    # Esto permite que la Wemos y el CURL funcionen sin contraseña
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Optimizamos para mostrar solo las últimas 50 lecturas
        # Esto evita que el navegador se pegue si tienes miles de datos
        return Lectura.objects.all().order_by('-timestamp')[:50]