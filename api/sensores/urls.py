from django.urls import path
from .views import (
    LecturaListCreateView, 
    SensorListView, 
    DispositivoListView
)

# Definimos el namespace para que, si tu proyecto crece, 
# puedas referenciar rutas como 'sensores:lectura-list-create'
app_name = 'sensores'

urlpatterns = [
    # Ingesta de datos y consulta de historial (Endpoint principal para Wemos y Dashboard)
    # GET/POST: http://localhost:8000/api/sensores/lecturas/
    path('lecturas/', LecturaListCreateView.as_view(), name='lectura-list-create'),

    # Catálogo técnico de sensores registrados
    # GET: http://localhost:8000/api/sensores/lista/
    path('lista/', SensorListView.as_view(), name='sensor-list'),

    # Estructura jerárquica para construir el menú lateral del Dashboard
    # GET: http://localhost:8000/api/sensores/menu/',
    path('menu/', DispositivoListView.as_view(), name='dispositivos-menu'),
    
    # Nueva ruta para el POST (Creación) y GET (Listado simple)
    path('', SensorListView.as_view(), name='sensor-list-create'),
]