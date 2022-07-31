import re
from uuid import UUID
from django.shortcuts import render
from django.http import HttpResponse
from clientes.serializers import ClienteSerializer, DadosBancariosSerializer
from clientes.models import Cliente, DadosBancarios
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# TODO - mudar id de int para string
class ClienteCreateView(APIView):
    def post(self, request):
        cliente_serializer = ClienteSerializer(data=request.data['cliente'])
        cliente_serializer.is_valid(raise_exception=True)
        cliente = cliente_serializer.save()
        response = Response()
        response.data = {
            'cliente':'Cliente criado com sucesso',
            'id': cliente.id
        }
        return response
    
    
    def get(self, request, **pk):
        if pk:
            cliente = Cliente.objects.get(id=pk['pk'])
            serializer = ClienteSerializer(cliente)
            return Response(serializer.data)
        else:
            clientes = Cliente.objects.all()
            serializer = ClienteSerializer(clientes, many = True)
            return Response(serializer.data)
    
    
    def put(self, request, pk):
        cliente = Cliente.objects.get(id=pk)
        serializer = ClienteSerializer(cliente,data=request.data['cliente'])
        serializer.is_valid(raise_exception=True)    
        serializer.save()
        return Response(serializer.data)
    
    
    def delete(self, request, pk):
        Cliente.objects.get(id=pk).delete()
        response = Response()
        response.data = {
            'cliente':'Cliente deletado com sucesso',
        }
        return response

      
class DadosBancariosCreateView(APIView):
    def post(self, request, pk):
        cliente = Cliente.objects.get(id=pk)
        dadosbancarios_serializer = DadosBancariosSerializer(data=request.data['dadosbancarios'])
        dadosbancarios_serializer.is_valid(raise_exception=True)
        dadosbancarios = dadosbancarios_serializer.save()
        cliente.dadosbancarios_set.add(dadosbancarios, bulk=False)
        response = Response()
        response.data = {
            'cliente':'Dados bancarios criado com sucesso',
            'id': dadosbancarios.id
        }
        return response
    
    
    def get(self, request, **pk):
        if 'db_id' not in pk.keys():
            dadosbancarios = DadosBancarios.objects.filter(cliente__id=pk['pk'])
            serializer = DadosBancariosSerializer(dadosbancarios, many = True)
            return Response(serializer.data)
        else:
            dadosbancarios = DadosBancarios.objects.get(id=pk['db_id'])
            serializer = DadosBancariosSerializer(dadosbancarios)
            return Response(serializer.data)
    
    
    def put(self, request, **pk):
        dadosbancarios = DadosBancarios.objects.get(id=pk['db_id'])
        serializer = DadosBancariosSerializer(dadosbancarios,data=request.data['dadosbancarios'])
        serializer.is_valid(raise_exception=True)    
        serializer.save()
        return Response(serializer.data)
    
    
    def delete(self, request, **pk):
        DadosBancarios.objects.get(id=pk['db_id']).delete()
        response = Response()
        response.data = {
            'dadosbancarios':'Dados Bancarios deletados com sucesso',
        }
        return response