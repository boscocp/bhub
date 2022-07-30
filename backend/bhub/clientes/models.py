from django.db import models

# Create your models here.
class Cliente(models.Model):
    razao_social = models.CharField(max_length=100)
    telefone = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    faturamento_declarado = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.razao_social}, {self.telefone}'
    
class DadosBancarios(models.Model):
    agencia = models.PositiveSmallIntegerField()
    conta = models.PositiveSmallIntegerField()
    banco = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)