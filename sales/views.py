from rest_framework import viewsets
from accounts.permissions import IsCashier, IsManager
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Sale, SaleItem
from .serializers import CustomerSerializer, SaleSerializer, SaleItemSerializer
from django.db.models import Sum, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Sale, SaleItem
import csv
from django.http import HttpResponse
from inventory.models import Product


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsManager])  # Only Admin & Manager can access reports
def sales_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Total sales count & revenue
    total_sales = Sale.objects.filter(created_at__range=[start_date, end_date])
    total_revenue = total_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    sales_count = total_sales.count()

    # Best-selling products
    top_products = SaleItem.objects.values('product__name').annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]

    # Sales by cashier
    sales_by_cashier = total_sales.values('cashier__username').annotate(
        total_sales=Count('id'),
        revenue=Sum('total_amount')
    )

    data = {
        'total_sales': sales_count,
        'total_revenue': total_revenue,
        'top_products': list(top_products),
        'sales_by_cashier': list(sales_by_cashier),
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsManager])  # Only Admin & Manager can access reports
def inventory_report(request):
    # Total inventory value
    total_inventory_value = Product.objects.aggregate(
        total_value=Sum('price_per_unit') * Sum('stock_quantity')
    )['total_value'] or 0

    # Low-stock items
    low_stock_items = Product.objects.filter(stock_quantity__lt=10).values(
        'name', 'stock_quantity'
    )

    data = {
        'total_inventory_value': total_inventory_value,
        'low_stock_items': list(low_stock_items),
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsManager])
def unified_report(request):
    report_type = request.GET.get('type', 'sales')  # Default to sales report

    if report_type == 'sales':
        return sales_report(request)
    elif report_type == 'inventory':
        return inventory_report(request)
    else:
        return Response({'error': 'Invalid report type'}, status=400)


def export_sales_csv(request):
    # Create the HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

    # Write CSV headers
    writer = csv.writer(response)
    writer.writerow(['Date', 'Customer', 'Total Amount'])

    # Fetch sales data
    sales = Sale.objects.all()
    for sale in sales:
        writer.writerow([sale.date, sale.customer.name, sale.total_amount])

    return response


def export_inventory_csv(request):
    # Create the HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'

    # Write CSV headers
    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Stock Quantity', 'Price Per Unit'])

    # Fetch inventory data
    from inventory.models import Product
    products = Product.objects.all()
    for product in products:
        writer.writerow([product.name, product.stock_quantity, product.price_per_unit])

    return response


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-created_at')
    serializer_class = SaleSerializer
    permission_classes = [IsCashier]  # Only admin, manager, and cashier can access

    def perform_create(self, serializer):
        serializer.save(cashier=self.request.user)  # Assigns cashier automatically
        
class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    permission_classes = [IsAuthenticated]


