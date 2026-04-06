from rest_framework import serializers
from .models import Dispositivo, Sensor, Lectura
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class DispositivoSerializer(serializers.ModelSerializer):
    """
    Serializer básico para operaciones CRUD de Dispositivos.
    
    Uso: Registro de nuevo hardware (Wemos D1/ESP32) en el sistema.
    """
    class Meta:
        model = Dispositivo
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    """
    Serializer de Instrumentación.
    
    Permite la creación de sensores vinculándolos a un dispositivo mediante su ID,
    y provee metadatos adicionales de solo lectura para el Dashboard.
    """
    # Estos campos son para lectura (GET), no afectan la creación (POST)
    dispositivo_nombre = serializers.ReadOnlyField(source='dispositivo.nombre_placa')
    dispositivo_chip = serializers.ReadOnlyField(source='dispositivo.chip_id')

    class Meta:
        model = Sensor
        fields = [
            'id', 
            'dispositivo',       # <--- CRÍTICO: Debe estar aquí para poder hacer el POST
            'nombre', 
            'slug', 
            'tipo', 
            'pin_conexion', 
            'dispositivo_nombre', 
            'dispositivo_chip'
        ]
        # Opcional: Puedes marcar los campos de solo lectura explícitamente si prefieres
        extra_kwargs = {
            'dispositivo_nombre': {'read_only': True},
            'dispositivo_chip': {'read_only': True}
        }


class LecturaSerializer(serializers.ModelSerializer):
    """
    Motor de Ingesta de Telemetría con Validación de Integridad.
    
    Este serializador procesa los POST de los microcontroladores. 
    Incluye lógica de validación para asegurar que el hardware que reporta 
    sea efectivamente el dueño del sensor en la base de datos.
    """
    chip_id = serializers.CharField(write_only=True)
    
    # Vinculación por SLUG: El hardware envía un texto, DRF busca el objeto Sensor
    sensor_slug = serializers.SlugRelatedField(
        queryset=Sensor.objects.select_related('dispositivo').all(),
        slug_field='slug',
        source='sensor'
    )

    class Meta:
        model = Lectura
        fields = ['chip_id', 'sensor_slug', 'tipo', 'valor', 'timestamp']
        read_only_fields = ['timestamp']

    def validate_valor(self, value):
        """
        Filtro de Rango Físico.
        Evita el registro de ruidos eléctricos o valores fuera de escala 
        industrial razonable (-50°C a 150°C).
        """
        if value < -50 or value > 150:
            raise serializers.ValidationError(
                "Valor fuera de rango físico razonable (-50 a 150)."
            )
        return value

    def create(self, validated_data):
        """
        Lógica de Persistencia con Check de Seguridad.
        """
        # 1. Extracción de datos validados
        chip_id = validated_data.pop('chip_id')
        sensor_obj = validated_data.pop('sensor') 

        # 2. Validación de Integridad de Hardware (Cross-check)
        # Previene que un dispositivo reporte datos de un sensor que no tiene conectado
        if sensor_obj.dispositivo.chip_id != chip_id:
            raise serializers.ValidationError({
                "hardware_mismatch": (
                    f"Seguridad: El sensor '{sensor_obj.slug}' "
                    f"no pertenece al hardware con ID '{chip_id}'."
                )
            })

        # 3. Escritura final en PostgreSQL
        return Lectura.objects.create(sensor=sensor_obj, **validated_data)


class DispositivoConSensoresSerializer(serializers.ModelSerializer):
    """
    Estructura Jerárquica para la Interfaz de Usuario (Dashboard).
    
    Mapea la relación Dispositivo -> [Lista de Sensores] para construir 
    el menú de navegación dinámica en el frontend.
    """
    sensores = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = Dispositivo
        fields = ['id', 'nombre_placa', 'chip_id', 'sensores']
        

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Campos personalizados del modelo 'Usuario'
        token['email'] = user.email
        token['nombre'] = user.nombre_completo
        token['rut'] = user.rut
        token['cargo'] = user.cargo
        token['es_admin'] = user.es_admin # Tu booleano personalizado
        
        return token