from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import requests

from .models import Product, Favorite, ProductRate, Subscription
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
        qs = qs.filter(type=product_type.upper())
    
    # 2) 은행명 필터
    bank_name = request.GET.get("bank_name")
    if bank_name:
        qs = qs.filter(bank_name=bank_name)

    # 3) 비대면 가입 여부
    is_nftf = request.GET.get("is_non_face_to_face")
    if is_nftf in ["true", "false"]:
        qs = qs.filter(is_non_face_to_face=(is_nftf == "true"))

    # 4) 보호 여부
    is_dp = request.GET.get("is_deposit_protected")
    if is_dp in ["true", "false"]:
        qs = qs.filter(is_deposit_protected=(is_dp == "true"))

    # 5) 최대 최소 
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

    # 6) 분류
    sort = request.GET.get("sort")
    if sort == "max_rate_desc":
        qs = qs.order_by("-max_rate", "-base_rate")
    elif sort == "base_rate_desc":
        qs = qs.order_by("-base_rate", "-max_rate")
    else:
        qs = qs.order_by("-max_rate", "-base_rate")

    # 7) limit (기본 20, 최대 50)
    limit = request.GET.get("limit")
    try:
        limit = int(limit) if limit is not None else 20
    except ValueError:
        limit = 20
    limit = max(1, min(limit, 50))

    qs = qs[:limit]

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
    monthly_rate = rate / 100 / 12
    return principal * pow(1 + monthly_rate, months)

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
    ptype = v["type"].upper()

    want_nftf = v.get("is_non_face_to_face", None)
    want_dp = v.get("is_deposit_protected", None)
    bank_name = v.get("bank_name")
    limit = v.get("limit", 20)

    qs = (
        Product.objects.filter(type=ptype, rates__save_terms_months=target_months)
        .prefetch_related("rates")
        .distinct()
    )

    if want_nftf is not None:
        qs = qs.filter(is_non_face_to_face=want_nftf)

    if want_dp is not None:
        qs = qs.filter(is_deposit_protected=want_dp)

    if bank_name:
        qs = qs.filter(bank_name=bank_name)

    qs = qs.order_by("-max_rate", "-base_rate")[:limit]

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

    results = results[:limit]

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

# ============================================================
# - 은행 별로 모아 보기
# ============================================================
@api_view(["GET"])
def bank_list(request):
    banks = (
       Product.objects
        .exclude(bank_name__isnull=True)
        .exclude(bank_name__exact="")
        .values_list("bank_name", flat=True)
        .distinct()
        .order_by("bank_name")
    )
    return Response({"banks": list(banks)}) 

@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def subscribe_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return Response({"detail":"존재하지 않는 상품입니다."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "POST":
        obj, created = Subscription.objects.get_or_create(user=request.user, product=product)
        if created:
            return Response({"is_subscribed":True}, status=status.HTTP_201_CREATED)
        return Response({"is_subscribed":True, "detail":"이미 가입한 상품입니다."}, status=status.HTTP_200_OK)
    
    deleted, _ = Subscription.objects.filter(user=request.user, product=product).delete()
    if deleted:
        return Response({"is_subscribed":False}, status=status.HTTP_200_OK)
    
    return Response({"is_subscribed":False, "detail": "가입 내역이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def subscription_list(request):
    subs = (
        Subscription.objects
        .filter(user=request.user)
        .select_related("product")
        .order_by("-created_at")
    )
    products = [s.product for s in subs]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# products/views.py에 추가할 함수

from django.conf import settings
import requests
import json
import re

@api_view(['POST'])
def get_ai_analysis(request, product_id):
    # 상품 조회
    try:
        product = Product.objects.prefetch_related('rates').get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"detail": "존재하지 않는 상품입니다."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 요청 데이터 검증
    from .serializers import AIAnalysisRequestSerializer
    serializer = AIAnalysisRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    amount = serializer.validated_data['amount']
    months = serializer.validated_data['months']
    
    # GMS API Key 확인
    gms_key = settings.GMS_API_KEY
    if not gms_key:
        return Response(
            {"detail": "GMS API 키가 설정되지 않았습니다."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # 예상 수령액 계산
    base_rate = product.base_rate or 0
    max_rate = product.max_rate or 0
    
    base_amount = int(amount * (1 + (base_rate / 100) * (months / 12)))
    max_amount = int(amount * (1 + (max_rate / 100) * (months / 12)))
    
    # 상품 타입 한글 변환
    product_type = "예금" if product.type == "DEPOSIT" else "적금"
    
    # 프롬프트 생성
    prompt = f"""
다음 금융 상품을 분석하고 사용자에게 맞춤 추천을 제공해주세요:

[상품 정보]
- 상품명: {product.name}
- 은행: {product.bank_name}
- 상품 유형: {product_type}
- 기본 금리: {base_rate:.2f}%
- 최고 금리: {max_rate:.2f}%
- 비대면 가입: {"가능" if product.is_non_face_to_face else "불가능"}
- 예금자 보호: {"보호" if product.is_deposit_protected else "미보호"}
- 우대조건: {product.prefer_condition_text if product.prefer_condition_text else "없음"}

[사용자 정보]
- 목표 금액: {amount:,}원
- 가입 기간: {months}개월
- 예상 수령액 (기본금리): {base_amount:,}원
- 예상 수령액 (최고금리): {max_amount:,}원

다음 형식으로 정확하게 응답해주세요:

1. 한줄평: (이 상품의 핵심 장점을 한 문장으로, 50자 이내)
2. 상세 분석: (상품의 장단점을 객관적으로 분석, 150-200자)
3. 추천 이유:
- 첫 번째 이유 (한 문장)
- 두 번째 이유 (한 문장)
- 세 번째 이유 (한 문장)
4. 주의사항: (가입 전 주의할 점 1-2문장)

친근하고 전문적인 톤으로 작성해주세요.
"""
    
    # GMS API 호출
    gms_url = "https://gms.ssafy.io/gmsapi/generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    try:
        response = requests.post(
            f"{gms_url}?key={gms_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            },
            timeout=30
        )
        
        if response.status_code != 200:
            return Response(
                {"detail": f"GMS API 호출 실패: {response.status_code}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # 응답 파싱
        gms_data = response.json()
        
        if not gms_data.get('candidates') or not gms_data['candidates'][0].get('content'):
            return Response(
                {"detail": "AI 응답 형식이 올바르지 않습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        ai_text = gms_data['candidates'][0]['content']['parts'][0]['text']
        
        # 응답 파싱
        parsed_data = parse_ai_response(ai_text)
        
        return Response(parsed_data, status=status.HTTP_200_OK)
        
    except requests.Timeout:
        return Response(
            {"detail": "AI 분석 요청 시간이 초과되었습니다."},
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )
    except requests.RequestException as e:
        return Response(
            {"detail": f"AI 분석 중 오류가 발생했습니다: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"detail": f"예상치 못한 오류가 발생했습니다: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def parse_ai_response(text):
    # 기본값 설정
    result = {
        "summary": "안정적인 금리로 목표 수익을 달성할 수 있는 상품입니다.",
        "detailed_analysis": "이 상품은 경쟁력 있는 금리와 다양한 우대조건을 제공하여 고객님의 재테크 목표 달성에 도움이 될 것으로 예상됩니다.",
        "reasons": [
            "시장 대비 경쟁력 있는 금리 제공",
            "안정적인 금융기관의 예금자 보호",
            "편리한 가입 절차 및 관리"
        ],
        "warning": "중도 해지 시 약정 금리를 받지 못할 수 있으니 가입 기간을 신중히 결정하시기 바랍니다."
    }
    
    try:
        # 1. 한줄평 추출
        summary_match = re.search(r'한줄평[:\s]*(.+?)(?=\n|2\.|상세)', text, re.IGNORECASE)
        if summary_match:
            summary = summary_match.group(1).strip()
            # 따옴표 제거
            summary = summary.strip('"\'')
            if summary and len(summary) > 10:
                result["summary"] = summary[:200]
        
        # 2. 상세 분석 추출
        analysis_match = re.search(r'상세\s*분석[:\s]*(.+?)(?=3\.|추천\s*이유|$)', text, re.DOTALL | re.IGNORECASE)
        if analysis_match:
            analysis = analysis_match.group(1).strip()
            analysis = analysis.strip('"\'')
            if analysis and len(analysis) > 20:
                result["detailed_analysis"] = analysis[:500]
        
        # 3. 추천 이유 추출
        reasons_match = re.search(r'추천\s*이유[:\s]*(.+?)(?=4\.|주의사항|$)', text, re.DOTALL | re.IGNORECASE)
        if reasons_match:
            reasons_text = reasons_match.group(1)
            # 줄바꿈으로 분리
            lines = reasons_text.split('\n')
            reasons = []
            for line in lines:
                line = line.strip()
                # - 또는 • 또는 숫자로 시작하는 라인만
                if line and (line.startswith('-') or line.startswith('•') or re.match(r'^\d+[.).]', line)):
                    # 앞의 기호 제거
                    clean_line = re.sub(r'^[-•\d.).\s]+', '', line).strip()
                    if clean_line and len(clean_line) > 5:
                        reasons.append(clean_line[:200])
            
            if reasons:
                result["reasons"] = reasons[:3]
        
        # 4. 주의사항 추출
        warning_match = re.search(r'주의사항[:\s]*(.+?)$', text, re.DOTALL | re.IGNORECASE)
        if warning_match:
            warning = warning_match.group(1).strip()
            warning = warning.strip('"\'')
            if warning and len(warning) > 10:
                result["warning"] = warning[:500]
    
    except Exception as e:
        # 파싱 실패 시 기본값 사용
        print(f"AI 응답 파싱 오류: {e}")
    
    return result