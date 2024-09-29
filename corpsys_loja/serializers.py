from rest_framework import serializers
from corpsys_loja.models import Cliente, Vendedor, Produto, GrupoProduto, Venda

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

class VendaSerializer(serializers.ModelSerializer):
    # Campos para leitura
    cliente = serializers.StringRelatedField(read_only=True)  # Mostra o nome do cliente
    vendedor = serializers.StringRelatedField(read_only=True)
    produto = serializers.StringRelatedField(read_only=True)

    # Campos para escrita
    cliente_id = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), write_only=True)
    vendedor_id = serializers.PrimaryKeyRelatedField(queryset=Vendedor.objects.all(), write_only=True)
    produto_id = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all(), write_only=True)

    # Formatação do campo data_venda
    data_venda = serializers.DateTimeField(format="%d/%m/%Y %H:%M", input_formats=["%Y-%m-%dT%H:%M:%S%z"])
    class Meta:
        model = Venda
        fields = [
            'id', 'cliente', 'vendedor', 'data_venda',
            'produto', 'quantidade', 'preco_unitario',
            'cliente_id', 'vendedor_id', 'produto_id'
        ]

    # Método para criar uma venda combinando os campos de leitura e escrita #
    def create(self, validated_data):
        cliente = validated_data.pop('cliente_id')
        vendedor = validated_data.pop('vendedor_id')
        produto = validated_data.pop('produto_id')
        venda = Venda.objects.create(cliente=cliente, vendedor=vendedor, produto=produto, **validated_data)
        return venda

    ## Método para atualizar a instancia e salvar ##
    def update(self, instance, validated_data):
        instance.cliente = validated_data.get('cliente_id', instance.cliente)
        instance.vendedor = validated_data.get('vendedor_id', instance.vendedor)
        instance.produto = validated_data.get('produto_id', instance.produto)
        instance.data_venda = validated_data.get('data_venda', instance.data_venda)
        instance.quantidade = validated_data.get('quantidade', instance.quantidade)
        instance.preco_unitario = validated_data.get('preco_unitario', instance.preco_unitario)
        instance.save()
        return instance
