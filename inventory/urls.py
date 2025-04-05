from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, StockTransactionViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'stock-transactions', StockTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
