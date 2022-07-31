from rest_framework import serializers
from clientes.models import Cliente, DadosBancarios

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        
class DadosBancariosSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(source="clientes", many=True, read_only=True)
    class Meta:
        model = DadosBancarios
        fields = '__all__'
        extra_kwargs = {'clientes': {'required': False}}