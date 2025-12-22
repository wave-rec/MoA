from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from django.conf import settings
import re
from .models import Product, Favorite, Subscription
from .serializers import ProductListSerializer, ProductDetailSerializer, RecommendRequestSerializer, RecommendResponseSerializer, AIAnalysisRequestSerializer


# ============================================================
# - 상품 목록 조회 API
# ============================================================
@api_view(["GET"])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
# - 조건 기반 상품 추천 및 검색 API
# ============================================================
@api_view(["POST"])
@permission_classes([AllowAny]) 
def product_recommend(request):
    is_logged_in = request.user.is_authenticated
    user_age = getattr(request.user, 'age', None) if is_logged_in else None
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

    if request.data.get('count_only') == True:
        return Response({'count': qs.count()}, status=status.HTTP_200_OK)


    qs = qs.order_by("-max_rate", "-base_rate")[:limit]
    
    results = []
    
    is_logged_in = request.user.is_authenticated
    user_age = request.user.age if is_logged_in else None

    for p in qs:
        rate_obj = next((r for r in p.rates.all() if r.save_terms_months == target_months), None)
        base_rate = rate_obj.base_rate if rate_obj and rate_obj.base_rate is not None else p.base_rate
        max_rate = rate_obj.max_rate if rate_obj and rate_obj.max_rate is not None else p.max_rate
        use_rate = max_rate or base_rate or 0

        is_recommended = False
        if is_logged_in and user_age:
            age_match = (user_age < 40 and p.is_non_face_to_face) or (user_age >= 40 and p.is_deposit_protected)
            
            if age_match and (max_rate or 0) >= 3.0: 
                is_recommended = True

        results.append({
            "product_id": p.id,
            "bank_name": p.bank_name,
            "name": p.name,
            "base_rate": base_rate,
            "max_rate": max_rate,
            "is_recommended": is_recommended,
            "match_score": _score(p, target_months, want_nftf, want_dp),
            "expected_amount": _calc_expected_amount(target_amount, target_months, use_rate),
        })

    results.sort(key=lambda x: (x["is_recommended"], x["match_score"]), reverse=True)

    return Response({"results": results[:limit]}, status=status.HTTP_200_OK)

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
    priority_banks = ['국민은행', '신한은행', '중소기업은행', '우리은행', '농협은행주식회사']
    
    all_banks = list(
        Product.objects
        .exclude(bank_name__isnull=True)
        .exclude(bank_name__exact="")
        .values_list("bank_name", flat=True)
        .distinct()
    )
    
    sorted_banks = []
    for bank in priority_banks:
        if bank in all_banks:
            sorted_banks.append(bank)
    
    for bank in sorted(all_banks):
        if bank not in sorted_banks:
            sorted_banks.append(bank)
    
    return Response({"banks": sorted_banks})

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


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def get_ai_analysis(request, product_id):
    try:
        product = Product.objects.prefetch_related('rates').get(id=product_id)
    except Product.DoesNotExist:
        return Response({"detail": "존재하지 않는 상품입니다."}, status=404)
    
    serializer = AIAnalysisRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    amount = serializer.validated_data['amount']
    months = serializer.validated_data['months']

    user = request.user

    gms_key = settings.GMS_API_KEY
    if not gms_key:
        return Response(
            {"detail": "GMS API 키가 설정되지 않았습니다."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    base_rate = product.base_rate or 0
    max_rate = product.max_rate or 0
    max_amount = int(amount * (1 + (max_rate / 100) * (months / 12)))

    prompt = f"""
당신은 대한민국 최고의 금융 자산관리 전문가입니다. 
{user.name}({user.age}세)님의 프로필에 맞춰 이 금융상품을 전문적으로 분석해주세요. 
답변은 친절하면서도 '불필요한 미사여구 없이' 정보 전달에 집중하여 6~8초 내에 생성이 완료되도록 작성하세요.

[분석 대상] {product.bank_name} - {product.name}
[가입 조건] {months}개월 / {amount:,}원 투자 / 예상 최대 {max_amount:,}원 수령

다음 형식을 엄격히 지켜주세요:

1. 한줄평: ({user.age}세 {user.name}님을 위한 자산관리 핵심 전략 1문장)

2. 상세 분석: ({user.age}대의 생애주기 특징과 이 상품의 금리/안정성 혜택을 결합하여 150자 내외로 심도 있게 분석)

3. 추천 이유 (구체적으로):
- 연령대별 자산 형성 전략과의 적합성 (예: {user.age}세의 위험 선호도 반영)
- 금리 경쟁력 및 실질 수익성 분석 (시중 금리와 비교한 장점)
- 가입 편의성 및 {user.name}님만을 위한 우대 혜택 포인트

4. 주의사항: ({user.age}세 사용자가 자금 운용 시 반드시 기억해야 할 리스크나 조건 1~2문장)
"""
    
    gms_url = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions"
    
    try:
        response = requests.post(
            gms_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {gms_key}"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system", 
                        "content": "당신은 빠르고 정확한 금융 분석가입니다. 정보를 명확한 구조로 제공하며, 문장은 간결한 '다'/'요'체로 끝맺으세요."
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.6,    
                "max_tokens": 800,    
                "presence_penalty": 0.1, 
                "frequency_penalty": 0.1
            },
            timeout=30
        )
        
        gms_data = response.json()
        
        if not gms_data.get('choices') or not gms_data['choices'][0].get('message'):
            return Response(
                {"detail": "AI 응답 형식이 올바르지 않습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        ai_text = gms_data['choices'][0]['message']['content']
        
        parsed_data = parse_ai_response(ai_text)
        
        return Response(parsed_data, status=status.HTTP_200_OK)
        
    except requests.Timeout:
        return Response({"detail": "AI 분석 요청 시간이 초과되었습니다."}, status=status.HTTP_504_GATEWAY_TIMEOUT)
    except Exception as e:
        return Response({"detail": f"오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def parse_ai_response(text):
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
        summary_match = re.search(r'한줄평[:\s]*(.+?)(?=\n|2\.|상세)', text, re.IGNORECASE)
        if summary_match:
            summary = summary_match.group(1).strip()
            summary = summary.strip('"\'')
            if summary and len(summary) > 10:
                result["summary"] = summary[:200]
        
        analysis_match = re.search(r'상세\s*분석[:\s]*(.+?)(?=3\.|추천\s*이유|$)', text, re.DOTALL | re.IGNORECASE)
        if analysis_match:
            analysis = analysis_match.group(1).strip()
            analysis = analysis.strip('"\'')
            if analysis and len(analysis) > 20:
                result["detailed_analysis"] = analysis[:500]
        
        reasons_match = re.search(r'추천\s*이유[:\s]*(.+?)(?=4\.|주의사항|$)', text, re.DOTALL | re.IGNORECASE)
        if reasons_match:
            reasons_text = reasons_match.group(1)
            lines = reasons_text.split('\n')
            reasons = []
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or re.match(r'^\d+[.).]', line)):
                    clean_line = re.sub(r'^[-•\d.).\s]+', '', line).strip()
                    if clean_line and len(clean_line) > 5:
                        reasons.append(clean_line[:200])
            
            if reasons:
                result["reasons"] = reasons[:3]
        
        warning_match = re.search(r'주의사항[:\s]*(.+?)$', text, re.DOTALL | re.IGNORECASE)
        if warning_match:
            warning = warning_match.group(1).strip()
            warning = warning.strip('"\'')
            if warning and len(warning) > 10:
                result["warning"] = warning[:500]
    
    except Exception as e:
        print(f"AI 응답 파싱 오류: {e}")
    
    return result