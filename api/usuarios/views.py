from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadimos datos al Payload del JWT (Carga útil)
        token['nombre'] = user.nombre_completo
        token['es_admin'] = user.es_admin
        token['cargo'] = user.cargo
        return token

    def validate(self, attrs):
        # Esta parte define qué devuelve la API en el cuerpo de la respuesta JSON
        data = super().validate(attrs)
        data['user'] = {
            'nombre': self.user.nombre_completo,
            'email': self.user.email,
            'es_admin': self.user.es_admin
        }
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer