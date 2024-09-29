from django.db import models
from django.utils import timezone  # Para obter a data e hora atuais
class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True) # Permitindo somente emails unicos
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nome}"

class Vendedor(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nome}"

class GrupoProduto(models.Model):
    tipo_produto = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo_produto

class Produto(models.Model):
    nome_produto = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    grupo = models.ForeignKey(GrupoProduto, on_delete=models.CASCADE) # Atribuindo fk do grupo produto

    def __str__(self):
        return self.nome_produto

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    data_venda = models.DateTimeField(default=timezone.now)  # Data atual no momento do cadastro

    def __str__(self):
        return f"Venda {self.id} - {self.vendedor.nome} para {self.cliente.nome} em {self.data_venda}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Valor será atribuído ao criar o item

    def __str__(self):
        return f"Item {self.produto.nome_produto} - (Venda {self.venda.id})"