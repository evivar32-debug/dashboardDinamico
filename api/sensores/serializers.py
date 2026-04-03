from rest_framework import serializers
from .models import Dispositivo, Sensor, Lectura

class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    # Mostramos el nombre de la placa en lugar de solo el ID numérico
    dispositivo_nombre = serializers.ReadOnlyField(source='dispositivo.nombre_placa')

    class Meta:
        model = Sensor
        fields = ['id', 'dispositivo', 'dispositivo_nombre', 'nombre', 'pin_conexion', 'tipo']

class LecturaSerializer(serializers.ModelSerializer):
    # Estos campos son para que la Wemos D1 nos hable de forma sencilla
    chip_id = serializers.CharField(write_only=True)
    sensor_nombre = serializers.CharField(write_only=True)

    class Meta:
        model = Lectura
        fields = ['chip_id', 'sensor_nombre', 'tipo', 'valor', 'timestamp']
        read_only_fields = ['timestamp']

    def create(self, validated_data):
        # Extraemos los datos de identificación que envió la Wemos
        chip_id = validated_data.pop('chip_id')
        sensor_nombre = validated_data.pop('sensor_nombre')

        # Buscamos el sensor exacto que pertenece a esa Wemos específica
        try:
            sensor = Sensor.objects.get(
                nombre=sensor_nombre,
                dispositivo__chip_id=chip_id
            )
        except Sensor.DoesNotExist:
            raise serializers.ValidationError(
                f"Error: No existe un sensor '{sensor_nombre}' para el dispositivo '{chip_id}'. "
                "Regístralos primero en el panel de Admin."
            )

        # Si todo está bien, creamos la lectura asociada a ese sensor
        return Lectura.objects.create(sensor=sensor, **validated_data)
    
    
# Ejemplo de JSON recibido por la Wemos
# {
#     "chip_id": "16777215",
#     "sensor_nombre": "DHT11_Terraza",
#     "tipo": "Temperatura",
#     "valor": 24.8
# }