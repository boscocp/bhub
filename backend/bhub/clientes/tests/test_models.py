from decimal import Decimal
from uuid import UUID
from django.test import TestCase
from clientes.models import Cliente, DadosBancarios
from bson.decimal128 import Decimal128
from django.core.exceptions import ObjectDoesNotExist
# Create your tests here.

class ClienteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Cliente.objects.create(
                id = 1,
                razao_social = 'CNPJ', 
                telefone = '112222-222',
                endereco = 'Ali na rua',
                faturamento_declarado = 100.51,               
            )
        
        
    def test_razao_social(self):
        cliente = Cliente.objects.get(id=1)
        field_label = cliente._meta.get_field('razao_social').verbose_name
        self.assertEquals(field_label, 'razao social')
        
        
    def test_data_cadastro_not_null(self):
        cliente = Cliente.objects.get(telefone='112222-222')
        self.assertIsNotNone(cliente.data_cadastro)
        
        
    def test_update_client(self):
        cliente = Cliente.objects.get(id=1)
        cliente.endereco = "Rua Ytaipu"
        cliente.faturamento_declarado = 555.55
        cliente.save()
        updated_cliente = Cliente.objects.get(id=1)
        self.assertEquals(updated_cliente.endereco, 'Rua Ytaipu')
        self.assertEquals(updated_cliente.faturamento_declarado, Decimal128('555.55'))
        self.assertEquals(updated_cliente.telefone, cliente.telefone)
    
    def test_delete_client(self):
        Cliente.objects.get(id=1).delete()
        with self.assertRaises(ObjectDoesNotExist, msg='Cliente matching query does not exist'):
            Cliente.objects.get(id=1)
        
        
class DadosBancariosModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cliente = Cliente(
            id = 2,
            razao_social = 'CPF', 
            telefone = '112222-222',
            endereco = 'Ali na rua',
            faturamento_declarado = 100.51,               
        )
        cliente.save()
        novo_banco = DadosBancarios(
            id = 1,
            agencia = 1,
            conta = 2,
            banco = "banco1",
            cliente = cliente,
        )
        novo_banco.save()
  
  
    def test_adiciona_banco(self):
        cliente = Cliente.objects.get(id=2)
        novo_banco = DadosBancarios(
            id=2,
            agencia = 1,
            conta = 2,
            banco = "banco2",
            cliente = cliente,
        )
        novo_banco.save()
        banco_salvo = DadosBancarios.objects.get(id=2)
        self.assertEquals(banco_salvo.banco, novo_banco.banco)
        self.assertEquals(banco_salvo.cliente.id, novo_banco.cliente.id)
    
    
    def test_deleta_cliente_cascata(self):
        Cliente.objects.get(id=2).delete()
        with self.assertRaises(ObjectDoesNotExist, msg='DadosBancarios matching query does not exist'):
            DadosBancarios.objects.get(id=1)
        with self.assertRaises(ObjectDoesNotExist, msg='DadosBancarios matching query does not exist'):
            DadosBancarios.objects.get(id=2)