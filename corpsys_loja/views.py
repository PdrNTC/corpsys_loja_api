from corpsys_loja.models import Cliente, Vendedor, Produto, GrupoProduto, Venda
from corpsys_loja.serializers import ClienteSerializer, VendedorSerializer, ProdutoSerializer, GrupoProdutoSerializer, VendaSerializer
from rest_framework import viewsets, status
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.utils.dateparse import parse_date
import pandas as pd
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
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

@api_view(['GET'])
def vendas_efetuadas(request):
    # Filtros para o usuário #
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    vendedor_id = request.GET.get('vendedor_id')
    cliente_id = request.GET.get('cliente_id')
    exportar = request.GET.get('exportar')  # 'pdf' ou 'excel'

    # Filtrar as vendas conforme os parâmetros fornecidos #
    vendas = Venda.objects.all()

    ## Tratando a data para ser igual com o datetime no banco ##
    if data_inicial:
        try:
            data_inicial = datetime.strptime(data_inicial, "%Y-%m-%d")
            vendas = vendas.filter(data_venda__gte=data_inicial)
        except ValueError:
            return Response({"error": "Formato de data inicial inválido."}, status=status.HTTP_400_BAD_REQUEST)

    if data_final:
        try:
            # Adicionando hora, minuto e segundo ao final do dia para garantir que a data final seja incluída no filtro
            data_final = datetime.strptime(data_final, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
            vendas = vendas.filter(data_venda__lte=data_final)
        except ValueError:
            return Response({"error": "Formato de data final inválido."}, status=status.HTTP_400_BAD_REQUEST)

    if vendedor_id:
        vendas = vendas.filter(vendedor_id=vendedor_id)
    if cliente_id:
        vendas = vendas.filter(cliente_id=cliente_id)

    # Serializar os dados #
    serializer = VendaSerializer(vendas, many=True)

    # Seleções para Exportar para PDF ou Excel #
    if exportar == 'pdf':
        return gerar_pdf(vendas)
    elif exportar == 'excel':
        return gerar_excel(vendas)

    # Retornar os dados filtrados em JSON #
    return Response(serializer.data, status=status.HTTP_200_OK)

def gerar_pdf(vendas):
    # Configurar um objeto BytesIO para o PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # Configurar o título do PDF
    p.drawString(100, 800, "Relatório de Vendas Efetuadas")

    y = 750
    for venda in vendas:
        p.drawString(100, y, f"Venda ID: {venda.id}, Cliente: {venda.cliente.nome}, Vendedor: {venda.vendedor.nome}, Valor Total: R$ {venda.valor_total_venda}")
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def gerar_excel(vendas):
    # Criar um DataFrame do pandas com os dados das vendas
    vendas_data = [
        {
            'Venda ID': venda.id,
            'Cliente': venda.cliente.nome,
            'Vendedor': venda.vendedor.nome,
            'Data da Venda': venda.data_venda.strftime("%d/%m/%Y %H:%M"),
            'Valor Total': venda.valor_total_venda,
        }
        for venda in vendas
    ]
    df = pd.DataFrame(vendas_data)

    # Gerar o arquivo Excel
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Vendas Efetuadas')
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=vendas_efetuadas.xlsx'
    return response