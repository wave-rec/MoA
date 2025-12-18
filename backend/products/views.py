from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Product, Favorite, ProductRate
from .serializers import ProductListSerializer, ProductDetailSerializer, RecommendRequestSerializer, RecommendResponseSerializer


# ============================================================
# - 상품 목록 조회 API
# ============================================================
@api_view(["GET"])
def product_list(request):
    qs = Product.objects.all()

    # 1) 예금 / 적금 타입
    product_type = request.GET.get("type")
    if product_type:
        qs = qs.filter(type=product_type)

    # 2) 비대면 가입 여부
    is_nftf = request.GET.get("is_non_face_to_face")
    if is_nftf in ["true", "false"]:
        qs = qs.filter(is_non_face_to_face=(is_nftf == "true"))

    # 3) 보호 여부
    is_dp = request.GET.get("is_deposit_protected")
    if is_dp in ["true", "false"]:
        qs = qs.filter(is_deposit_protected=(is_dp == "true"))

    # 4) 최대 최소 
    min_base_rate = request.GET.get("min_base_rate")
    if min_base_rate:
        try:
            qs = qs.filter(base_rate__gte=float(min_base_rate))
        except ValueError:
            pass

    min_max_rate = request.GET.get("min_max_rate")
    if min_max_rate:
        try:
            qs = qs.filter(max_rate__gte=float(min_max_rate))
        except ValueError:
            pass

    # 5) 분류
    sort = request.GET.get("sort")
    if sort == "max_rate_desc":
        qs = qs.order_by("-max_rate", "-base_rate")
    elif sort == "base_rate_desc":
        qs = qs.order_by("-base_rate", "-max_rate")
    else:
        qs = qs.order_by("-max_rate", "-base_rate")

    serializer = ProductListSerializer(qs, many=True)
    return Response(serializer.data)

# ============================================================
# - 상품 상세 조회 API
# ============================================================
@api_view(["GET"])
def product_detail(request, product_id):
    product = Product.objects.prefetch_related("rates").filter(id=product_id).first()

    if not product:
        return Response({"detail": "존재하지 않는 상품입니다."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)

# ============================================================
# - 상품 찜 토글 API
# ============================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return Response({"detail":"존재하지 않는 상품입니다."}, status=status.HTTP_404_NOT_FOUND)
    
    fav = Favorite.objects.filter(user=request.user, product=product).first()
    if fav:
        fav.delete()
        return Response({"is_favorite":False}, status=status.HTTP_200_OK)
    
    Favorite.objects.create(user=request.user, product=product)
    return Response({"is_favorite":True}, status=status.HTTP_201_CREATED)

# ============================================================
# - 추천 계산용 유틸 함수
# ============================================================
def _calc_expected_amount(principal: float, months: int, rate: float) -> float:
    return principal * (1 + (rate / 100) * (months / 12))

def _score(product: Product, months: int, want_nftf, want_dp) -> int:
    score = 50 

    if want_nftf is not None and product.is_non_face_to_face == want_nftf:
        score += 20

    if want_dp is not None and product.is_deposit_protected == want_dp:
        score += 20

    if product.max_rate is not None or product.base_rate is not None:
        score += 10

    return min(score, 100)


# ============================================================
# - 조건 기반 상품 추천 API
# ============================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def product_recommend(request):
    req = RecommendRequestSerializer(data=request.data)
    req.is_valid(raise_exception=True)
    v = req.validated_data

    target_amount = v["target_amount"]
    target_months = v["target_months"]
    ptype = v["type"]

    want_nftf = v.get("is_non_face_to_face", None)
    want_dp = v.get("is_deposit_protected", None)

    qs = (
        Product.objects.filter(type=ptype, rates__save_terms_months=target_months)
        .prefetch_related("rates")
        .distinct()
    )

    if want_nftf is not None:
        qs = qs.filter(is_non_face_to_face=want_nftf)

    if want_dp is not None:
        qs = qs.filter(is_deposit_protected=want_dp)

    qs = qs.order_by("-max_rate", "-base_rate")[:50]

    results = []
    for p in qs:
        rate_obj = next((r for r in p.rates.all() if r.save_terms_months == target_months), None)

        base_rate = rate_obj.base_rate if rate_obj and rate_obj.base_rate is not None else p.base_rate
        max_rate = rate_obj.max_rate if rate_obj and rate_obj.max_rate is not None else p.max_rate

        use_rate = max_rate or base_rate or 0

        results.append({
            "product_id": p.id,
            "fin_prdt_cd": p.fin_prdt_cd,
            "bank_name": p.bank_name,
            "name": p.name,
            "base_rate": base_rate,
            "max_rate": max_rate,
            "match_score": _score(p, target_months, want_nftf, want_dp),  # ✅ 인자 정상
            "expected_amount": _calc_expected_amount(target_amount, target_months, use_rate),
        })

    results.sort(
        key=lambda x: (x["match_score"], x["max_rate"] or 0, x["base_rate"] or 0),
        reverse=True
    )

    results = results[:20]

    res = RecommendResponseSerializer({"results": results})
    return Response(res.data, status=status.HTTP_200_OK)

# ============================================================
# - 찜 목록 조회 API (마이페이지용)
# ============================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def favorite_list(request):
    favorites = (
        Favorite.objects
        .filter(user=request.user)
        .select_related("product")
        .order_by("-created_at")
    )

    products = [fav.product for fav in favorites]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)