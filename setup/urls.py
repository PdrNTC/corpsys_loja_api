from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from corpsys_loja.views import ClienteViewSet, VendedorViewSet, ProdutoViewSet, GrupoProdutoViewSet, VendaViewSet

# Criando obj router do app #
router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'vendedores', VendedorViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'grupo-produtos', GrupoProdutoViewSet)
router.register(r'vendas', VendaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)), # Incluindo objeto com todas rotas
]
