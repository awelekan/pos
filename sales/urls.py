from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, SaleViewSet, SaleItemViewSet
from .views import sales_report, inventory_report, export_inventory_csv, unified_report


router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'sale-items', SaleItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reports/sales/', sales_report, name='sales_report'),
    path('reports/inventory/', inventory_report, name='inventory_report'),
    path('reports/inventory/export/csv/', export_inventory_csv, name='export_inventory_csv'),
    path('reports/', unified_report, name='unified_report'),
]
