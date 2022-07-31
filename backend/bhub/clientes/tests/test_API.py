from uuid import UUID
from django.test import TestCase
from clientes.models import Cliente, DadosBancarios
import json
from rest_framework.test import APIClient
client = APIClient()
# Create your tests here.
# TODO - enum para selecionavel fixo
class ClienteAPITest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        pass
    
    
    def test_view_post(self):
        request = {
            "cliente": {
                "razao_social": "solteiro",
                "telefone": "1155555",
                "endereco": "Rua Api",
                "faturamento_declarado": 1054.51
            }
        }
        response = client.post('/clientes/',request , format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_view_get_list(self):
        cliente1 = Cliente.objects.create(
            razao_social = 'Casado', 
            telefone = '112222-222',
            endereco = 'Ali na rua',
            faturamento_declarado = 100.51,               
        )
        cliente2 = Cliente.objects.create(
            razao_social = 'divorciado', 
            telefone = '112222-232',
            endereco = 'Ali na rua',
            faturamento_declarado = 100.51,               
        )
        cliente3 = Cliente.objects.create(
            razao_social = 'solteiro', 
            telefone = '112222-242',
            endereco = 'Ali na rua',
            faturamento_declarado = 100.51,               
        )
        response = client.get('/clientes/')
        self.assertEqual(response.status_code, 200)
        
        
    def test_get_by_uuid(self):
        Cliente.objects.create(
            id = UUID("35fc86f3-5533-412b-8ce0-93107079b469"),
            razao_social = 'Casado', 
            telefone = '112222-222',
            endereco = 'Ali na rua',
            faturamento_declarado = 100.51,               
        )
        response = client.get('/clientes/35fc86f3-5533-412b-8ce0-93107079b469')
        self.assertEqual(response.status_code, 200)