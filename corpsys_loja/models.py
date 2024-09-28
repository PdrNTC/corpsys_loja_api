from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True) # Permitindo somente emails unicos
    telefone = models.CharField(max_length=20)

class Vendedor(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

class GrupoProduto(models.Model):
    tipo_produto = models.CharField(max_length=255)

class Produto(models.Model):
    nome_produto = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    grupo = models.ForeignKey(GrupoProduto, on_delete=models.CASCADE) # Atribuindo fk do grupo produto

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    data_venda = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venda {self.id} - {self.vendedor.nome}"
    
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.produto.nome} - (Venda {self.venda.id})"