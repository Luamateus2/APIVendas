from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views.produto_views import ProdutoViewSet
from .views.venda_views import VendaViewSet

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'vendas', VendaViewSet, basename='venda')

urlpatterns = [
    path('api/', include(router.urls)),  
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
