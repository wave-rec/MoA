import requests
from django.conf import settings
from django.db import transaction
from products.models import Product, ProductRate

FSS_DEPOSIT_API_URL = "https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"


def _to_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_float(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _is_non_face_to_face(join_way: str) -> bool:
    if not join_way:
        return False
    return ("인터넷" in join_way) or ("스마트폰" in join_way)


def fetch_deposit_products(top_fin_grp_no="020000", page_no=1) -> dict:
    if not settings.FSS_API_KEY:
        raise RuntimeError("FSS_API_KEY가 없습니다.")

    params = {
        "auth": settings.FSS_API_KEY,
        "topFinGrpNo": top_fin_grp_no,
        "pageNo": page_no,
    }

    res = requests.get(FSS_DEPOSIT_API_URL, params=params, timeout=10)
    res.raise_for_status()

    data = res.json()
    result = data.get("result")

    if not result or result.get("err_cd") != "000":
        raise RuntimeError(f"FSS API 오류: {result}")

    return result


@transaction.atomic
def upsert_deposit_products(result: dict) -> dict:
    base_list = result.get("baseList", [])
    option_list = result.get("optionList", [])

    product_map = {}

    # 1️⃣ Product
    for item in base_list:
        fin_prdt_cd = item.get("fin_prdt_cd")
        if not fin_prdt_cd:
            continue

        product, _ = Product.objects.update_or_create(
            fin_prdt_cd=fin_prdt_cd,
            defaults={
                "bank_name": item.get("kor_co_nm"),
                "name": item.get("fin_prdt_nm"),
                "type": "DEPOSIT",
                "is_non_face_to_face": _is_non_face_to_face(item.get("join_way")),
                "prefer_condition_text": item.get("spcl_cnd") or "",
                "is_deposit_protected": False,
                "base_rate": 0,
                "max_rate": 0,
            },
        )
        product_map[fin_prdt_cd] = product

    rate_minmax = {}

    # 2️⃣ ProductRate
    for opt in option_list:
        fin_prdt_cd = opt.get("fin_prdt_cd")
        product = product_map.get(fin_prdt_cd)
        if not product:
            continue

        save_trm = _to_int(opt.get("save_trm"))
        if save_trm is None:
            continue

        base_rate = _to_float(opt.get("intr_rate"))
        max_rate = _to_float(opt.get("intr_rate2"))

        ProductRate.objects.update_or_create(
            product=product,
            save_terms_months=save_trm,
            defaults={
                "base_rate": base_rate,
                "max_rate": max_rate,
            },
        )

        cur_min, cur_max = rate_minmax.get(fin_prdt_cd, (None, None))
        rate_minmax[fin_prdt_cd] = (
            base_rate if cur_min is None else min(cur_min, base_rate),
            max_rate if cur_max is None else max(cur_max, max_rate),
        )

    # 3️⃣ Product 금리 반영
    for fin_prdt_cd, (min_r, max_r) in rate_minmax.items():
        Product.objects.filter(fin_prdt_cd=fin_prdt_cd).update(
            base_rate=min_r or 0,
            max_rate=max_r or 0,
        )

    return {
        "products": len(base_list),
        "rates": len(option_list),
    }
