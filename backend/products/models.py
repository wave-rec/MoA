from django.db import models

class Product(models.Model):
    fin_prdt_cd = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=100)
    name = models.CharField(max_length=200)

    # 예금 / 적금 구분
    type = models.CharField(max_length=20)

    #상품 특성
    is_deposit_protected = models.BooleanField(default=False)
    is_non_face_to_face = models.BooleanField(default=False)

    #우대 조건 또는 설명 등
    prefer_condition_text = models.TextField(blank=True)

    #대표 금리 정보 (상품 전체 요약용)
    base_rate = models.FloatField(null=True, blank=True)
    max_rate = models.FloatField(null=True, blank=True)

    #생성/수정 시간
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank_name} - {self.name}"
    

class ProductRate(models.Model):
    product = models.ForeignKey(Product, related_name="rates", on_delete=models.CASCADE)
    save_terms_months = models.IntegerField() # 1 / 3 / 6 / 12개월
    base_rate = models.FloatField(null=True)
    max_rate = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.save_terms_months}개월" 


