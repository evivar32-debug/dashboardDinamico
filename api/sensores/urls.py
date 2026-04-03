from django.urls import path
from .views import LecturaListCreateView

urlpatterns = [
    # La ruta será: http://localhost:8000/api/sensores/lecturas/
    path('lecturas/', LecturaListCreateView.as_view(), name='lectura-list-create'),
]