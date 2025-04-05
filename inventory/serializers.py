from rest_framework import serializers
from .models import Category, Product, StockTransaction
from accounts.models import User

class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Product
        fields = '__all__'

class StockTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    handled_by = serializers.ReadOnlyField(source="handled_by.username")

    class Meta:
        model = StockTransaction
        fields = '__all__'
