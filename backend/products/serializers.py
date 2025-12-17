from rest_framework import serializers
from .models import Product, ProductRate

class ProductRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRate
        fields = ("save_terms_months", "base_rate", "max_rate")

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "fin_prdt_cd",
            "bank_name",
            "name",
            "type",
            "is_non_face_to_face",
            "is_deposit_protected",
            "base_rate",
            "max_rate",
        )

class ProductDetailSerializer(serializers.ModelSerializer):
    rates = ProductRateSerializer(many=True, read_only=True)
    is_favorite = serializers.BooleanField(read_only=True, default=False)
    
    class Meta:
        model = Product
        fields = (
            "id",
            "fin_prdt_cd",
            "bank_name",
            "name",
            "type",
            "is_non_face_to_face",
            "is_deposit_protected",
            "prefer_condition_text",
            "base_rate",
            "max_rate",
            "rates",
            "is_favorite",
        )