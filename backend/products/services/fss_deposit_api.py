import requests
from django.conf import settings

FSS_DEPOSIT_API_URL = "https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"

def fetch_deposit_products(top_fin_grp_no="020000", page_no=1):
    if not settings.FSS_API_KEY:
        raise RuntimeError("FSS_API_KEY가 없습니다. settings.py / .env를 확인하세요.")
    
    params = {
        "auth" : settings.FSS_API_KEY,
        "topFinGrpNo" : top_fin_grp_no,
        "pageNo" : page_no,
    }

    response = requests.get(FSS_DEPOSIT_API_URL, params=params, timeout=10)

    response.raise_for_status()

    try:
        data = response.json()
    except ValueError:
        raise RuntimeError(f"FSS API가 JSON이 아닌 응답을 반환함: {response.text[:300]}")

    if "result" not in data:
        raise RuntimeError(f"FSS API 응답 구조 이상: {data}")

    result = data["result"]

    if result.get("err_cd") != "000":
        raise RuntimeError(f"FSS API 오류: {result.get('err_cd')} - {result.get('err_msg')}")

    return result