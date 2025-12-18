from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Product, Favorite
from .serializers import ProductListSerializer, ProductDetailSerializer

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

@api_view(["GET"])
def product_detail(request, product_id):
    product = Product.objects.prefetch_related("rates").filter(id=product_id).first()

    if not product:
        return Response({"detail": "존재하지 않는 상품입니다."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)

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