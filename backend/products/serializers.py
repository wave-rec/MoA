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

class RecommendRequestSerializer(serializers.Serializer):
    target_amount = serializers.IntegerField(min_value=1)
    target_months = serializers.IntegerField(min_value=1)
    type = serializers.CharField()
    bank_name = serializers.CharField(required=False)
    is_non_face_to_face = serializers.BooleanField(required=False)
    is_deposit_protected = serializers.BooleanField(required=False)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=50, default=20)

class RecommendItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    fin_prdt_cd = serializers.CharField()
    bank_name = serializers.CharField()
    name = serializers.CharField()
    base_rate = serializers.FloatField(allow_null=True)
    max_rate = serializers.FloatField(allow_null=True)

    match_score = serializers.IntegerField()
    expected_amount = serializers.FloatField()

class RecommendResponseSerializer(serializers.Serializer):
    results = RecommendItemSerializer(many=True)

class ProductRecommendRequestSerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    bank_name = serializers.CharField(required=False)
    is_non_face_to_face = serializers.BooleanField(required=False)
    is_deposit_protected = serializers.BooleanField(required=False)

    save_terms_months = serializers.IntegerField(required=False, min_value=1)
    min_base_rate = serializers.FloatField(required=False, min_value=0)
    min_max_rate = serializers.FloatField(required=False, min_value=0)

    sort = serializers.ChoiceField(
        required=False,
        choices=["max_rate_desc", "base_rate_desc"],
        default="max_rate_desc",
    )

    limit = serializers.IntegerField(required=False, min_value=1, max_value=50, default=10)

class AIAnalysisRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(
        required=True,
        min_value=10000,
        error_messages={
            'required': '금액을 입력해주세요.',
            'invalid': '유효한 금액을 입력해주세요.',
            'min_value': '최소 1만원 이상 입력해주세요.',
        }
    )
    months = serializers.IntegerField(
        required=True,
        min_value=1,
        max_value=60,
        error_messages={
            'required': '기간을 입력해주세요.',
            'invalid': '유효한 기간을 입력해주세요.',
        }
    )

class AIAnalysisResponseSerializer(serializers.Serializer):
    summary = serializers.CharField()
    detailed_analysis = serializers.CharField()
    reasons = serializers.ListField(child=serializers.CharField())
    warning = serializers.CharField()