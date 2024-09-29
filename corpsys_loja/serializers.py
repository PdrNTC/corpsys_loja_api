from rest_framework import serializers
from corpsys_loja.models import Cliente, Vendedor, Produto, GrupoProduto, Venda, ItemVenda

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
    produto_nome = serializers.StringRelatedField(source='produto', read_only=True)
    preco_unitario = serializers.SerializerMethodField()  # Obter o preço do produto

    class Meta:
        model = ItemVenda
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario']

    def get_preco_unitario(self, obj):
        return obj.produto.preco  # Retorna o preço do produto

class VendaSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField(read_only=True)
    vendedor = serializers.StringRelatedField(read_only=True)
    itens = ItemVendaSerializer(many=True, read_only=True)  # Somente leitura

    # Campos para escrita
    cliente_id = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), write_only=True)
    vendedor_id = serializers.PrimaryKeyRelatedField(queryset=Vendedor.objects.all(), write_only=True)
    itens_data = serializers.ListField(child=serializers.DictField(), write_only=True)  # Usado para criar os itens

    # Formatação do campo `data_venda`
    data_venda = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    class Meta:
        model = Venda
        fields = [
            'id', 'cliente', 'vendedor', 'data_venda', 'itens',
            'cliente_id', 'vendedor_id', 'itens_data'
        ]
        read_only_fields = ['data_venda']  # A data de venda é preenchida automaticamente

    def create(self, validated_data):
        cliente = validated_data.pop('cliente_id')
        vendedor = validated_data.pop('vendedor_id')
        itens_data = validated_data.pop('itens_data')

        # Criação da venda
        venda = Venda.objects.create(cliente=cliente, vendedor=vendedor)

        # Criação dos itens da venda
        for item_data in itens_data:
            produto_id = item_data['produto']  # Pegando apenas o ID do produto
            produto = Produto.objects.get(id=produto_id)
            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=item_data['quantidade'],
                preco_unitario=produto.preco  # Define o preço unitário do produto
            )
        return venda

    def update(self, instance, validated_data):
        instance.cliente = validated_data.get('cliente_id', instance.cliente)
        instance.vendedor = validated_data.get('vendedor_id', instance.vendedor)
        instance.save()

        itens_data = validated_data.get('itens_data')
        if itens_data:
            instance.itens.all().delete()  # Exclui todos os itens antigos
            for item_data in itens_data:
                produto_id = item_data['produto']  # Pegando apenas o ID do produto
                produto = Produto.objects.get(id=produto_id)
                ItemVenda.objects.create(
                    venda=instance,
                    produto=produto,
                    quantidade=item_data['quantidade'],
                    preco_unitario=produto.preco  # Define o preço unitário do produto
                )
        return instance