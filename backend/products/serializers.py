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