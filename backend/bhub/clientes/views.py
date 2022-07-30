from django.shortcuts import render
from django.http import HttpResponse
from clientes.serializers import ClienteSerializer
from clientes.models import Cliente, DadosBancarios
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class ClienteCreateView(APIView):
    def post(self, request):
        print(request.data)
        cliente_serializer = ClienteSerializer(data=request.data['cliente'])
        cliente_serializer.is_valid(raise_exception=True)
        cliente = cliente_serializer.save()
        print(cliente.id)
        response = Response()
        response.data = {
            'cliente':'Cliente criado com sucesso',
            'id': cliente.id
        }
        return response