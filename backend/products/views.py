from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from django.conf import settings
import re
from .models import Product, Favorite, Subscription
from .serializers import ProductListSerializer, ProductDetailSerializer, RecommendRequestSerializer, AIAnalysisRequestSerializer


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

    if product.type == 'DEPOSIT':
        principal = amount
        interest = amount * (max_rate / 100) * (months / 12)
        max_amount = int(amount + interest)
        amount_desc = f"{amount:,}원 일시 예치"
        
    elif product.type == 'SAVINGS':
        monthly = amount
        total_principal = monthly * months
        interest = monthly * ((months * (months + 1)) / 2) * (max_rate / 100 / 12)
        max_amount = int(total_principal + interest)
        amount_desc = f"매월 {monthly:,}원씩 {months}개월 (총 {total_principal:,}원)"
        
    else:
        principal = amount
        interest = amount * (max_rate / 100) * (months / 12)
        max_amount = int(amount + interest)
        amount_desc = f"{amount:,}원"

    age = user.age

    # 연령대별 가이드
    if age < 30:
        age_guide = """
[20대 맞춤 전략]
- 핵심 목표: 종잣돈 모으기, 결혼 자금, 첫 투자 시드머니
- 추천 포인트: 단기 적금(6~12개월), 비대면 편의성, 소액으로 시작
- 금지 단어: "노후", "은퇴", "연금"
- 사용 단어: "첫 목돈", "결혼 준비", "종잣돈", "여행 자금"
"""
    elif age < 40:
        age_guide = """
[30대 맞춤 전략]
- 핵심 목표: 주택 구입 자금(전세/매매), 육아 준비금, 목돈 굴리기
- 추천 포인트: 중기 상품(12~24개월), 목돈 예치, 안정성 중시
- 금지 단어: "노후" (아직 이름)
- 사용 단어: "내집 마련", "자녀 교육비", "목돈 운용", "재테크 시작"
"""
    elif age < 50:
        age_guide = """
[40대 맞춤 전략]
- 핵심 목표: 자녀 교육비 마련, 노후 준비 시작, 안정적 자산 운용
- 추천 포인트: 장기 상품, 예금자보호, 안정성 최우선
- 사용 단어: "교육비 준비", "노후 대비 시작", "안정적 수익", "목돈 보관"
"""
    else:
        age_guide = """
[50대+ 맞춤 전략]
- 핵심 목표: 은퇴 준비, 연금 보완, 생활비 마련, 리스크 최소화
- 추천 포인트: 단기 예금, 예금자보호 필수, 높은 금리, 유동성
- 사용 단어: "은퇴 준비", "안전한 자산", "생활비 마련", "확실한 보호"
"""

    prompt = f"""
금융 전문가로서 {age}세 {user.name}님께 상품을 상담합니다.

**상품**: {product.bank_name} {product.name}
**금리**: 기본 {base_rate:.2f}% / 최고 {max_rate:.2f}%
**목표**: {amount_desc} → 만기 시 예상 {max_amount:,}원 (이자 약 {int(max_amount - amount):,}원)
**특징**: {"비대면 가입" if product.is_non_face_to_face else "영업점 방문"} / {"예금자보호" if product.is_deposit_protected else "보호 미적용"}
**우대조건 원문**: {product.prefer_condition_text}

{age_guide}

⚠️ 아래 형식을 정확히 따르세요:

1. 한줄평:
{age}세에게 이 상품의 핵심 가치를 50자 이내 한 문장으로 작성하세요.

2. 종합 분석:
250자로 작성하되, 위의 연령대 맞춤 전략을 반드시 반영하세요:
- {age}대의 구체적인 재무 목표 (위 가이드 참고)
- 시중금리 대비 이 상품의 경쟁력
- {amount:,}원 {months}개월 저축 시 정확한 수익 계산
- 우대조건, 가입 편의성

3. 핵심 우대 혜택:
우대조건 원문을 분석하여 {user.name}님이 챙겨야 할 핵심 행동을 3가지만 요약하세요.
- 각 줄은 '조건: 혜택(금리)' 형태로 작성 (예: 급여이체 실적 충족 시: +0.2%p 우대)

4. 추천 이유:
각 100자로 정확히 3개를 작성하세요. 불렛포인트(-)로 시작:
- 첫째: 금리를 구체적 숫자로 (예: "평균 2.5% 대비 +0.3%p, {amount:,}원 기준 약 X만원 추가")
- 둘째: {age}대의 실제 자금 용도 (위 가이드의 핵심 목표 활용)
- 셋째: 안전성, 편의성 등 부가 혜택

4. 주의사항:
120자로 작성:
- 중도 해지 시 불이익
- 우대금리 조건 미충족 시 기본금리
- {months}개월 자금 묶임

필수 규칙:
✓ 존댓말(~합니다, ~하세요)
✓ 위 연령대 가이드의 "사용 단어"만 사용
✓ 위 연령대 가이드의 "금지 단어" 절대 사용 금지
✓ 구체적 숫자 필수
✓ 형식: "1. 한줄평:", "2. 종합 분석:", "3. 추천 이유:", "4. 주의사항:"
✗ 추가 서론/마무리 금지
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
                        "content": f"""당신은 금융 상담사입니다. 
{age}세 고객에게 맞는 표현만 사용하세요.
지정된 형식을 정확히 따르세요.
연령대 가이드의 금지 단어는 절대 사용하지 마세요.
추가 서론, 마무리 절대 금지."""
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.6,
                "top_p": 0.9,
                "max_tokens": 700,
                "presence_penalty": 0,
                "frequency_penalty": 0
            },
            timeout=25
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
        return Response(
            {"detail": "AI 분석 요청 시간이 초과되었습니다."}, 
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )

    except Exception as e:
        return Response(
            {"detail": f"오류가 발생했습니다: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



def parse_ai_response(text):
    # 기본값 설정
    result = {
        "summary": "안정적인 금리로 목표 달성을 지원하는 상품입니다.",
        "detailed_analysis": "경쟁력 있는 조건으로 체계적인 저축을 돕습니다.",
        "prefer_benefits": [],
        "reasons": [
            "시중 평균 대비 높은 금리로 추가 수익 기대",
            "예금자 보호로 원금 안정성 보장",
            "간편한 가입으로 빠른 저축 시작"
        ],
        "warning": "중도 해지 시 약정 금리보다 낮은 금리가 적용됩니다."
    }

    try:
        # 전처리: 마크다운 기호 및 이모지 제거
        text = text.replace('**', '').replace('##', '').replace('###', '')
        text = re.sub(r'[✨💡⚠️🎯📊💰🏦]', '', text).strip()

        # 1. 한줄평
        match = re.search(r'1\.\s*한줄평\s*[:：]\s*(.+?)(?=\n\s*2\.)', text, re.DOTALL)
        if match: result["summary"] = match.group(1).strip()

        # 2. 종합 분석
        match = re.search(r'2\.\s*종합\s*분석\s*[:：]\s*(.+?)(?=\n\s*3\.)', text, re.DOTALL)
        if match: result["detailed_analysis"] = match.group(1).strip()

        # 3. 핵심 우대 혜택 (줄바꿈 기준으로 유연하게 추출)
        match = re.search(r'3\.\s*핵심\s*우대\s*혜택\s*[:：]\s*(.+?)(?=\n\s*4\.)', text, re.DOTALL)
        if match:
            benefits = []
            for line in match.group(1).split('\n'):
                line = line.strip()
                # 불렛포인트가 없더라도 내용이 있으면 추가
                clean = re.sub(r'^[-•*]\s*', '', line).strip()
                if clean and len(clean) > 2:
                    benefits.append(clean)
            result["prefer_benefits"] = benefits

        # 4. 추천 이유
        # 추천 이유와 주의사항의 번호가 4번으로 겹칠 수 있으므로 뒤에 '주의사항'이 오는지 체크
        match = re.search(r'4\.\s*추천\s*이유\s*[:：]\s*(.+?)(?=\n\s*4\.\s*주의사항|\n\s*5\.|\Z)', text, re.DOTALL)
        if match:
            reasons = []
            for line in match.group(1).split('\n'):
                line = line.strip()
                clean = re.sub(r'^[-•*]\s*', '', line).strip()
                if len(clean) > 5:
                    reasons.append(clean)
            if reasons: result["reasons"] = reasons[:3]

        # 5. 주의사항 (4. 주의사항 또는 5. 주의사항 모두 대응)
        match = re.search(r'(?:4|5)\.\s*주의사항\s*[:：]\s*(.+?)$', text, re.DOTALL)
        if match:
            result["warning"] = match.group(1).strip()

    except Exception as e:
        print(f"⚠️ 파싱 오류: {e}")

    return result