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
    vendedor = serializers.StringRelatedField() # Mostrar o nome do vendedor #
    cliente = serializers.StringRelatedField()
    itens = ItemVendaSerializer(many=True, read_only=True)
    valor_total_venda = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    # Campos para escrita (mas ocultos na interface de navegação HTML) #
    vendedor_id = serializers.PrimaryKeyRelatedField(queryset=Vendedor.objects.all(), write_only=True, label='Vendedor')
    cliente_id = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), write_only=True, label='Cliente')
    itens_data = serializers.ListField(child=serializers.DictField(), write_only=True, label='Itens')

    # Formatação do campo data #
    data_venda = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)

    class Meta:
        model = Venda
        fields = [
            'id', 'vendedor', 'cliente', 'data_venda', 'itens', 'vendedor_id', 'cliente_id', 'itens_data', 'valor_total_venda'
        ]
        read_only_fields = ['data_venda', 'valor_total_venda']  # A data de venda é preenchida automaticamente #

    def create(self, validated_data):
        cliente = validated_data.pop('cliente_id')
        vendedor = validated_data.pop('vendedor_id')
        itens_data = validated_data.pop('itens_data')

        # Criação da venda #
        venda = Venda.objects.create(cliente=cliente, vendedor=vendedor)

        # Criação dos itens da venda e cálculo do valor total #
        valor_total = 0
        for item_data in itens_data:
            produto_id = item_data['produto']
            produto = Produto.objects.get(id=produto_id)
            quantidade = item_data['quantidade']
            preco_unitario = produto.preco

            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=preco_unitario
            )
            valor_total += preco_unitario * quantidade

        # Atualizando o valor total da venda
        venda.valor_total_venda = valor_total
        venda.save()

        return venda

    def update(self, instance, validated_data):
        instance.cliente = validated_data.get('cliente_id', instance.cliente)
        instance.vendedor = validated_data.get('vendedor_id', instance.vendedor)
        instance.save()

        itens_data = validated_data.get('itens_data')
        if itens_data:
            instance.itens.all().delete()
            valor_total = 0
            for item_data in itens_data:
                produto_id = item_data['produto']
                produto = Produto.objects.get(id=produto_id)
                quantidade = item_data['quantidade']
                preco_unitario = produto.preco

                ItemVenda.objects.create(
                    venda=instance,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario
                )
                valor_total += preco_unitario * quantidade

            # Atualizando o valor total da venda
            instance.valor_total_venda = valor_total
            instance.save()

        return instance