from rest_framework import serializers
from .models import MenuItem, Category
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "title"]

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source="inventory")
    price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    # category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    category = serializers.HyperlinkedRelatedField(
        queryset = Category.objects.all(),
        view_name='categories'
    )
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "stock", "price_after_tax", "category"]
        extra_kwargs = {
            'price': {'min_value': 2},
            'stock':{'source':'inventory', 'min_value': 1}
        }
        
    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)