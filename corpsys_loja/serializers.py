from rest_framework import serializers
from corpsys_loja.models import Cliente, Vendedor, Produto, GrupoProduto, ItemVenda, Venda

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class GrupoProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoProduto
        fields = '__all__'

class ItemVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVenda
        fields = '__all__'

class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True)

    class Meta:
        model = Venda
        fields = '__all__'