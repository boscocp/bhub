from django.test import TestCase
from clientes.models import Cliente

# Create your tests here.

class ClienteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Cliente.objects.create(
                razao_social = 'Casado', 
                telefone = '112222-222',
                endereco = 'Ali na rua',
                faturamento_declarado = 1000,               
            )
        
        
    def test_razao_social(self):
        cliente = Cliente.objects.get(telefone='112222-222')
        field_label = cliente._meta.get_field('razao_social').verbose_name
        self.assertEquals(field_label, 'razao social')
        
    def test_data_cadastro_not_null(self):
        cliente = Cliente.objects.get(telefone='112222-222')
        self.assertIsNotNone(cliente.data_cadastro)