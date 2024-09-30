from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from corpsys_loja.models import Cliente, Vendedor, Produto, Venda, ItemVenda, GrupoProduto
from rest_framework import status
from decimal import Decimal
import json

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from corpsys_loja.models import Cliente, Vendedor, Produto, Venda, ItemVenda, GrupoProduto
from rest_framework import status
import json

class VendaTestCase(TestCase):
    def setUp(self):
        # Criar um grupo de produtos para teste #
        self.grupo = GrupoProduto.objects.create(tipo_produto="Eletrônicos")
        
        # Criar produtos para teste #
        self.produto1 = Produto.objects.create(nome_produto="Mouse", preco=150.00, grupo=self.grupo)
        self.produto2 = Produto.objects.create(nome_produto="Placa Mãe", preco=700.00, grupo=self.grupo)
        
        # Criar clientes e vendedores para teste #
        self.cliente = Cliente.objects.create(nome="Jose da Silva", email="jose@test.com", telefone="123456789")
        self.vendedor = Vendedor.objects.create(nome="Paulo Tevez", email="paulo@test.com")
    
    ## TESTE CRIAR VENDA ##
    def test_criar_venda(self):
        """
        Testa a criação de uma venda com itens e o cálculo do valor total da venda.
        """
        venda_data = {
            "cliente_id": self.cliente.id,
            "vendedor_id": self.vendedor.id,
            "itens_data": [
                {"produto": self.produto1.id, "quantidade": 2},
                {"produto": self.produto2.id, "quantidade": 1}
            ]
        }
        
        response = self.client.post(reverse('venda-list'), json.dumps(venda_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        venda = Venda.objects.get(id=response.data['id'])
        self.assertEqual(venda.valor_total_venda, 1000.00)  # 2 * 150 + 1 * 700

    ## TESTE FILTRAR POR CLIENTE ##
    def test_vendas_filtradas_por_cliente(self):
        """
        Testa o endpoint de vendas efetuadas filtrando pelo cliente.
        """
        venda1 = Venda.objects.create(cliente=self.cliente, vendedor=self.vendedor, data_venda=timezone.now())
        ItemVenda.objects.create(venda=venda1, produto=self.produto1, quantidade=1, preco_unitario=self.produto1.preco)
        
        response = self.client.get(reverse('vendas-efetuadas'), {'cliente_id': self.cliente.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['cliente'], self.cliente.nome)

    ## TESTE FILTRAR POR PERIODO ##
    def test_vendas_filtradas_por_periodo(self):
        """
        Testa o endpoint de vendas efetuadas filtrando por um período de datas.
        """
        venda1 = Venda.objects.create(cliente=self.cliente, vendedor=self.vendedor, data_venda="2024-09-01T10:00:00Z")
        ItemVenda.objects.create(venda=venda1, produto=self.produto1, quantidade=1, preco_unitario=self.produto1.preco)
        
        venda2 = Venda.objects.create(cliente=self.cliente, vendedor=self.vendedor, data_venda="2024-09-15T10:00:00Z")
        ItemVenda.objects.create(venda=venda2, produto=self.produto2, quantidade=1, preco_unitario=self.produto2.preco)
        
        response = self.client.get(reverse('vendas-efetuadas'), {'data_inicial': '2024-09-01', 'data_final': '2024-09-30'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    ## TESTE DO VALOR CALCULADO ##
    def test_venda_valor_total_calculado_corretamente(self):
        """
        Testa se o valor total de uma venda é calculado corretamente ao adicionar itens.
        """
        venda = Venda.objects.create(cliente=self.cliente, vendedor=self.vendedor, data_venda=timezone.now())
        ItemVenda.objects.create(venda=venda, produto=self.produto1, quantidade=3, preco_unitario=self.produto1.preco)
        ItemVenda.objects.create(venda=venda, produto=self.produto2, quantidade=2, preco_unitario=self.produto2.preco)

        venda.refresh_from_db()  # Atualizar a venda do banco de dados para obter o valor total atualizado
        self.assertEqual(venda.valor_total_venda, Decimal('1850.00'))

