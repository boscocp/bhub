from django.db import models
import uuid

RAZAO_SOCIAL = [
    ('CPF', 'pessoa fisica'),
    ('CNPJ', 'pessoa juridica'),
]

# Create your models here.
class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular cient')
    razao_social = models.CharField(choices=RAZAO_SOCIAL, max_length=100)
    telefone = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    faturamento_declarado = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.razao_social}, {self.telefone}'
    
class DadosBancarios(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular cient')
    agencia = models.PositiveSmallIntegerField()
    conta = models.PositiveSmallIntegerField()
    banco = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.banco}'