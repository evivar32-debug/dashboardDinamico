from rest_framework import serializers
from .models import Dispositivo, Sensor, Lectura

class DispositivoSerializer(serializers.ModelSerializer):
    """Serializer básico para ABM de dispositivos"""
    class Meta:
        model = Dispositivo
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    """Serializer para sensores, incluyendo el nombre de la placa dueña"""
    dispositivo_nombre = serializers.ReadOnlyField(source='dispositivo.nombre_placa')
    dispositivo_chip = serializers.ReadOnlyField(source='dispositivo.chip_id')

    class Meta:
        model = Sensor
        fields = ['id', 'nombre', 'slug', 'tipo', 'pin_conexion', 'dispositivo_nombre', 'dispositivo_chip']

class LecturaSerializer(serializers.ModelSerializer):
    """Serializer para la ingesta de telemetría desde hardware (Wemos/ESP32)"""
    chip_id = serializers.CharField(write_only=True)
    
    # Vinculamos el slug del JSON directamente con la instancia del modelo Sensor
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
        """Ejemplo de validación de ingeniería: Evitar ruidos o valores fuera de rango"""
        if value < -50 or value > 150:  # Rango típico de un sensor industrial
            raise serializers.ValidationError("Valor fuera de rango físico razonable (-50 a 150).")
        return value

    def create(self, validated_data):
        # 1. Extraemos los datos validados
        chip_id = validated_data.pop('chip_id')
        sensor_obj = validated_data.pop('sensor') 

        # 2. Validación de Integridad de Hardware
        # Verificamos que el chip_id reportado coincida con el dueño del sensor en BD
        if sensor_obj.dispositivo.chip_id != chip_id:
            raise serializers.ValidationError({
                "hardware_mismatch": f"Seguridad: El sensor '{sensor_obj.slug}' no pertenece al hardware '{chip_id}'."
            })

        # 3. Persistencia en PostgreSQL
        return Lectura.objects.create(sensor=sensor_obj, **validated_data)

class DispositivoConSensoresSerializer(serializers.ModelSerializer):
    """Estructura anidada para el menú lateral del Dashboard"""
    sensores = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = Dispositivo
        fields = ['id', 'nombre_placa', 'chip_id', 'sensores']