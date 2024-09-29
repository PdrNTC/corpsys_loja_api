from corpsys_loja.models import Cliente, Vendedor, Produto, GrupoProduto, Venda
from corpsys_loja.serializers import ClienteSerializer, VendedorSerializer, ProdutoSerializer, GrupoProdutoSerializer, VendaSerializer
from rest_framework import viewsets

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class GrupoProdutoViewSet(viewsets.ModelViewSet):
    queryset = GrupoProduto.objects.all()
    serializer_class = GrupoProdutoSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer