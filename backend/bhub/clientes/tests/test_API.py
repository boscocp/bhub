from uuid import UUID
from django.test import TestCase
from clientes.models import Cliente, DadosBancarios
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APIClient
client = APIClient()
# Create your tests here.
# TODO - enum para selecionavel fixo
class ClienteAPITest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        Cliente.objects.create(
            id = UUID("35fc86f3-5533-412b-8ce0-93107079b469"),
            razao_social = 'CNPJ', 
            telefone = '112222-222',
            endereco = 'Ali na rua',
            faturamento_declarado = 100.51,               
        )
    
    
    def test_view_post(self):
        request = {
            "cliente": {
                "razao_social": "CPF",
                "telefone": "1155555",
                "endereco": "Rua Api",
                "faturamento_declarado": 1054.51
            }
        }
        response = client.post('/clientes/',request , format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_view_get_list(self):
        cliente1 = Cliente.objects.create(
            razao_social = 'CNPJ', 
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
            razao_social = 'CPF', 
            telefone = '112222-242',
            endereco = 'Ali na rua',
            faturamento_declarado = 100.51,               
        )
        response = client.get('/clientes/')
        self.assertEqual(response.status_code, 200)
        
        
    def test_get_by_uuid(self):
        response = client.get('/clientes/35fc86f3-5533-412b-8ce0-93107079b469/')
        self.assertEqual(response.status_code, 200)
        
    
    def test_update_cliente(self):
        request = {
            "cliente": {
                "razao_social": "CPF",
                "telefone": "1155555",
                "endereco": "Rua Api",
                "faturamento_declarado": 1054.51
            }
        }
        response = client.put('/clientes/35fc86f3-5533-412b-8ce0-93107079b469/', request, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data['telefone'], "1155555")
        
        
    def test_delete_cliente(self):
        response = client.delete('/clientes/35fc86f3-5533-412b-8ce0-93107079b469/')
        self.assertEqual(response.status_code, 200)
        
        
    def test_create_dados_bancarios(self):
        request = {
            "dadosbancarios": {
                "agencia": 1,
                "conta": 3,
                "banco": "Banco11",
            }
        }
        response = client.post('/clientes/35fc86f3-5533-412b-8ce0-93107079b469/dadosbancarios/', request, format='json')
        self.assertEqual(response.status_code, 200)
        dadosbancarios = DadosBancarios.objects.get(id=response.data['id'])
        self.assertEquals(dadosbancarios.cliente.id, UUID("35fc86f3-5533-412b-8ce0-93107079b469"))
    
    def test_get_all_dados_bancarios(self):
        cliente = Cliente.objects.create(
            id = UUID("35fc86f3-5533-412b-8ce0-93107079b468"),
            razao_social = 'CNPJ', 
            telefone = '112222-222',
            endereco = 'Ali na rua',
            faturamento_declarado = 100.51,               
        )
        
        novo_banco = DadosBancarios( 
            agencia = 1,
            conta = 2,
            banco = "banco1",
            cliente = cliente,
        )
        novo_banco.save()
        novo_banco2 = DadosBancarios(
            agencia = 1,
            conta = 2,
            banco = "banco2",
            cliente = cliente,
        )
        novo_banco2.save()
        response = client.get('/clientes/35fc86f3-5533-412b-8ce0-93107079b468/dadosbancarios/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_dados_bancarios_by_id(self):
        cliente = Cliente.objects.get(id="35fc86f3-5533-412b-8ce0-93107079b469")        
        novo_banco = DadosBancarios( 
            agencia = 1,
            conta = 2,
            banco = "banco1",
            cliente = cliente,
        )
        novo_banco.save()
        response = client.get('/clientes/35fc86f3-5533-412b-8ce0-93107079b469/dadosbancarios/'+novo_banco.id.__str__()+'/')
        self.assertEqual(response.status_code, 200)
        
    def test_update_dados_bancarios(self):
        cliente = Cliente.objects.get(id="35fc86f3-5533-412b-8ce0-93107079b469")
        novo_banco = DadosBancarios( 
            agencia = 1,
            conta = 2,
            banco = "banco1",
            cliente = cliente,
        )
        novo_banco.save()
        
        request = {
            "dadosbancarios": {
                "agencia": 54,
                "conta": 333,
                "banco": "Banco_update",
            }
        }
        response = client.put('/clientes/35fc86f3-5533-412b-8ce0-93107079b469/dadosbancarios/'+novo_banco.id.__str__()+'/', request, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data['banco'], "Banco_update")
        
    def test_delete_dados_bancarios(self):
        cliente = Cliente.objects.get(id="35fc86f3-5533-412b-8ce0-93107079b469")
        
        novo_banco = DadosBancarios( 
            agencia = 1,
            conta = 2,
            banco = "banco1",
            cliente = cliente,
        )
        novo_banco.save()
        response = client.delete('/clientes/35fc86f3-5533-412b-8ce0-93107079b469/dadosbancarios/'+novo_banco.id.__str__()+'/')
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist, msg='DadosBancarios matching query does not exist'):
            DadosBancarios.objects.get(id=novo_banco.id)