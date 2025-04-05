from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, StockTransaction
from .serializers import CategorySerializer, ProductSerializer, StockTransactionSerializer
from accounts.permissions import IsManager


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # Assign current user

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsManager]  # Only admin and manager can access

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class StockTransactionViewSet(viewsets.ModelViewSet):
    queryset = StockTransaction.objects.all().order_by('-created_at')
    serializer_class = StockTransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(handled_by=self.request.user)  # Assign current user
