# 🪙 MoA (My Own Adviser)

<img width="737" height="487" alt="Image" src="https://github.com/user-attachments/assets/c10cc700-2a59-461b-a849-f1ccbac51a1c" />

&nbsp;

**처음 재테크, 나만의 금융 친구 MoA**

MoA는 금융 초보자를 위한 맞춤형 예적금 추천 플랫폼입니다.
</br>
AI 기반 상품 분석과 직관적인 UI/UX를 통해 복잡한 금융 상품을 쉽게 비교하고 선택할 수 있습니다.

<br/>

## 📌 프로젝트 개요

-   **프로젝트명**: MoA (My Own Adviser)
-   **개발 기간**: 2025.12.03 ~ 2025.12.26 (24일)
-   **팀 구성**: 2인 (풀스택)
-   **목표**: 금융 초보자도 쉽게 이해하고 선택할 수 있는 예적금 추천 서비스

<br/>

## 🐿 서비스 특징

-   AI 기반 연령대별 맞춤 상품 분석 제공
-   사용자 조건(금액, 기간)을 고려한 실시간 추천 서비스

<br/>

## 👥 팀 소개

|                                                        안수연                                                         |                                                        최지현                                                         |
| :-------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------: |
|                                                         팀장                                                          |                                                         팀원                                                          |
|                                                   Frontend, Backend                                                   |                                                   Frontend, Backend                                                   |
| <img src="https://github.com/user-attachments/assets/7e69eb19-4a38-4670-9ed2-67f9dafa3ee1" width="200" height="200"/> | <img src="https://github.com/user-attachments/assets/0564b600-10ed-4fda-904f-6a834a1e405b" width="200" height="200"/> |
|                                       [@wave-rec](https://github.com/wave-rec)                                        |                                     [@jihyun0805](https://github.com/jihyun0805)                                      |

### 🤝 역할 분담

<br/>

**안수연 (팀장)**

-   메인 페이지, 예/적금 추천, 상품 상세, 유튜브 검색
-   헤더/푸터, 메인 레이아웃, 탑 버튼
-   목업 디자인, 플로우 차트, 와이어프레임 제작
-   프론트엔드 초기 환경 세팅

**최지현 (팀원)**

-   주변 은행 페이지, 로그인/회원가입, 마이페이지, 게시판, 금은시세
-   플로우 차트, 와이어프레임 제작
-   백엔드 초기 개발 환경 구성

<br/>

## 🛠 기술 스택

### Backend

![Django](https://img.shields.io/badge/DJANGO-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLITE-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

### Frontend

![Vue.js](https://img.shields.io/badge/VUE.JS-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![Pinia](https://img.shields.io/badge/PINIA-FFD859?style=for-the-badge&logo=vue.js&logoColor=black)
![JavaScript](https://img.shields.io/badge/JAVASCRIPT-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Vite](https://img.shields.io/badge/VITE-646CFF?style=for-the-badge&logo=vite&logoColor=white)

### AI & API

![OpenAI](https://img.shields.io/badge/OPENAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![FSS](https://img.shields.io/badge/금융감독원_API-0066CC?style=for-the-badge)
![Kakao](https://img.shields.io/badge/KAKAO_MAP-FFCD00?style=for-the-badge&logo=kakao&logoColor=black)
![YouTube](https://img.shields.io/badge/YOUTUBE_API-FF0000?style=for-the-badge&logo=youtube&logoColor=white)

### Tools

![Git](https://img.shields.io/badge/GIT-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GITHUB-181717?style=for-the-badge&logo=github&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/VISUAL_STUDIO_CODE-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![Postman](https://img.shields.io/badge/POSTMAN-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Figma](https://img.shields.io/badge/FIGMA-F24E1E?style=for-the-badge&logo=figma&logoColor=white)

<br/>

## 💻 개발 환경

### Backend

-   **Python**: 3.12+
-   **Django**: 5.2.9
-   **Django REST Framework**: 3.16.1
-   **djangorestframework-simplejwt**: 5.5.1
-   **Pillow**: 12.0.0
-   **requests**: 2.32.5

### Frontend

-   **Node.js**: 18.x+
-   **Vue.js**: 3.5.13
-   **Vite**: 6.0.3
-   **Pinia**: 2.2.8
-   **Axios**: 1.7.9
-   **XLSX**: (금은시세 데이터 파싱)

<br/>

## 📂 프로젝트 구조

### Backend

```
backend/
├── manage.py
├── requirements.txt
│
├── pjt/                          # 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                     # 회원 관리
│   ├── models.py                # User 모델
│   ├── views.py                 # 로그인, 회원가입
│   ├── serializers.py
│   └── urls.py
│
├── products/                     # 금융 상품
│   ├── models.py                # Product, ProductRate, Subscription, Favorite
│   ├── views.py                 # AI 분석, 추천 알고리즘
│   ├── serializers.py
│   ├── urls.py
│   ├── services/
│   │   └── fss_api.py           # 금융감독원 API 연동
│   └── management/commands/
│       └── fetch_products.py    # 데이터 수집 명령어
│
└── articles/                     # 커뮤니티
    ├── models.py                # Post, Comment, PostImage
    ├── views.py                 # 게시글, 댓글 CRUD
    ├── serializers.py
    ├── permissions.py
    └── urls.py
```

### Frontend

```
frontend/
├── package.json
├── vite.config.js
│
├── public/
│   └── assets/
│       ├── banks/               # 은행 로고 이미지
│       ├── data/                # 금은시세 XLSX 데이터
│       └── main/                # 메인 배너 이미지
│
└── src/
    ├── main.js
    ├── App.vue
    │
    ├── router/
    │   └── index.js             # 라우터 설정
    │
    ├── stores/                  # Pinia 상태 관리
    │   ├── auth.js             # 인증 상태
    │   ├── posts.js            # 게시글 상태
    │   └── comments.js         # 댓글 상태
    │
    ├── api/                     # API 통신 모듈
    │   ├── client.js           # Axios 인스턴스
    │   ├── auth.js             # 인증 API
    │   ├── products.js         # 상품 API
    │   ├── user.js             # 사용자 API
    │   └── kakaoMap.js         # 카카오맵 SDK
    │
    ├── layouts/
    │   └── MainLayout.vue       # 메인 레이아웃
    │
    ├── components/
    │   ├── common/              # 공통 컴포넌트
    │   │   ├── AppHeaderUser.vue
    │   │   ├── AppHeaderGuest.vue
    │   │   ├── AppFooter.vue
    │   │   └── ScrollToTop.vue
    │   └── commodity/
    │       └── PriceChart.vue   # 금은시세 차트
    │
    ├── views/                   # 페이지 컴포넌트
    │   ├── MainView.vue                # 메인 페이지
    │   ├── LoginView.vue               # 로그인
    │   ├── SignupView.vue              # 회원가입
    │   ├── RecommendView.vue           # 상품 추천
    │   ├── ProductDetailView.vue       # 상품 상세 (AI 분석)
    │   ├── BankSearchView.vue          # 은행 지점 찾기
    │   ├── YoutubeSearchview.vue       # 금융 교육 (유튜브)
    │   ├── CommodityView.vue           # 금은시세
    │   ├── PostListView.vue            # 게시판 목록
    │   ├── PostDetailView.vue          # 게시글 상세
    │   ├── PostCreateView.vue          # 게시글 작성
    │   ├── PostEditView.vue            # 게시글 수정
    │   ├── MyPageView.vue              # 마이페이지
    │   ├── LikedProductsView.vue       # 가입 상품 목록
    │   ├── MyPostsView.vue             # 내가 쓴 글
    │   └── ProfileEditView.vue         # 프로필 수정
    │
    └── constants/
        └── financialTerms.js    # 금융 용어 데이터 (24개)
```

<br/>

## 🖨 ERD

<img width="1344" height="913" alt="Image" src="https://github.com/user-attachments/assets/bd7648b5-c69a-4d56-8daf-7419a68beb55" />

&nbsp;

## 📝 코드 컨벤션

<details>
<summary><b>Backend (Python/Django)</b></summary>

### 네이밍 규칙

-   **변수/함수**: snake_case
    ```python
    user_age = 25
    def calculate_interest_rate():
        pass
    ```
-   **클래스**: PascalCase
    ```python
    class ProductRate(models.Model):
        pass
    ```
-   **상수**: UPPER_SNAKE_CASE
    ```python
    MAX_RATE = 5.0
    FSS_API_KEY = "your_key"
    ```

</details>

<details>
<summary><b>Frontend (Vue.js/JavaScript)</b></summary>

### 네이밍 규칙

-   **변수/함수**: camelCase
    ```javascript
    const userName = 'MoA';
    const fetchProducts = async () => {};
    ```
-   **컴포넌트**: PascalCase
    ```javascript
    MainView.vue;
    AppHeader.vue;
    ```
-   **상수**: UPPER_SNAKE_CASE
    ```javascript
    const API_BASE_URL = 'http://localhost:8000';
    ```

</details>

<details>
<summary><b>Git Commit Convention</b></summary>

### Commit Message 형식

```
<#이슈 번호> <type>: <subject>

<body>
```

### Type 종류

-   `feat`: 새로운 기능 추가
-   `fix`: 버그 수정
-   `docs`: 문서 수정
-   `style`: 코드 포맷팅, 세미콜론 누락 등
-   `refactor`: 코드 리팩토링
-   `test`: 테스트 코드
-   `chore`: 빌드 업무, 패키지 매니저 설정 등

### 예시

```
#1 [feat]: AI 상품 분석 기능 추가

- GPT-4o-mini 연동
- 연령대별 프롬프트 엔지니어링 적용
```

</details>

<br/>

## 🚀 설치 및 실행 방법

<details>
<summary><b>1. 저장소 클론</b></summary>

```bash
git clone https://github.com/your-username/moa.git
cd moa
```

</details>

<details>
<summary><b>2. 백엔드 설정</b></summary>

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정 (.env 파일 생성)
FSS_API_KEY=your_fss_api_key
GMS_API_KEY=your_openai_api_key

# 데이터베이스 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 금융 데이터 수집 (선택사항)
python manage.py fetch_products --type all

# 서버 실행
python manage.py runserver
```

</details>

<details>
<summary><b>3. 프론트엔드 설정</b></summary>

```bash
cd frontend

# 패키지 설치
npm install

# 환경변수 설정 (.env 파일 생성)
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_KAKAO_JS_KEY=your_kakao_js_key
VITE_YOUTUBE_API_KEY=your_youtube_api_key

# 개발 서버 실행
npm run dev
```

</details>

<details>
<summary><b>4. 접속</b></summary>

-   **Frontend**: http://localhost:5173
-   **Backend**: http://localhost:8000

</details>

<br/>

## 🔑 환경변수 설정

### Backend (.env)

```env
# Django
SECRET_KEY=your_django_secret_key
DEBUG=True

# FSS (금융감독원 API)
FSS_API_KEY=your_fss_api_key

# OpenAI (GMS API)
GMS_API_KEY=your_openai_api_key
```

### Frontend (.env)

```env
# API Base URL
VITE_API_BASE_URL=http://127.0.0.1:8000

# Kakao Map
VITE_KAKAO_JS_KEY=your_kakao_js_key

# YouTube
VITE_YOUTUBE_API_KEY=your_youtube_api_key
```

<br/>

## 🎬 주요 기능 시연

### 1. 회원 인증

<details>
<summary><b>회원가입 & 로그인</b></summary>

#### 회원가입

![Image](https://github.com/user-attachments/assets/d6bfff83-b047-43d4-b01b-60ca95b5f52e)

-   이메일, 비밀번호, 이름, 나이 입력
-   실시간 유효성 검사
-   회원가입 완료 후 자동 로그인

#### 로그인

![로그인](https://github.com/user-attachments/assets/d5a87954-d7d9-44a3-9b11-7c84b9d183a2)

-   JWT 토큰 기반 인증
-   로그인 상태 유지

</details>

### 2. 상품 추천 및 조회

<details>
<summary><b>예·적금 상품 추천</b></summary>

#### 상품 추천

![상품 추천](https://github.com/user-attachments/assets/2c0fa820-62db-4d4a-ad2c-8031a3e5d5b5)

-   예금 / 적금 선택
-   은행, 금액, 기간 조건 입력
-   실시간 매칭 상품 개수 표시
-   조건에 맞는 상품 리스트 제공

#### 상품 상세 조회

![상품 상세](https://github.com/user-attachments/assets/60f04d6a-6843-4604-9887-2bfcb8a0832b)

-   기본 금리 / 최고 금리 정보
-   기간별 금리 테이블
-   예상 수령액 자동 계산
-   우대 조건 상세 안내

</details>

### 3. AI 기반 상품 분석

<details>
<summary><b>AI 맞춤 분석</b></summary>

![AI 분석](https://github.com/user-attachments/assets/455b326a-14a2-41aa-b415-e962dde5ee50)

-   연령대별 맞춤 한줄평
-   종합 분석 제공
-   핵심 우대 혜택 요약
-   추천 이유 3가지 제시
-   주의사항 안내

</details>

### 4. 마이페이지

<details>
<summary><b>개인화 서비스</b></summary>

#### 마이페이지

![마이페이지](https://github.com/user-attachments/assets/54d4304d-f580-4078-b75f-1e90ed1e1bfe)

-   프로필 정보 조회
-   회원 정보 수정
-   비밀번호 변경

#### 가입 상품 관리

![가입 상품 관리](https://github.com/user-attachments/assets/bdca2e9c-7585-43b8-bd2a-4227292845d8)

-   가입한 상품 목록 조회
-   상품별 금리 정보 확인
-   재가입 방지 기능
-   가입 취소 기능

#### 게시판 작성 글 관리

![게시판 작성 글 관리](https://github.com/user-attachments/assets/d1892f9f-0b6e-441c-b4b1-8c2260e810ab)

-   게시한 글 목록 조회

</details>

### 5. 커뮤니티

<details>
<summary><b>게시판 & 댓글</b></summary>

#### 게시글 작성

![게시글 작성](https://github.com/user-attachments/assets/81514ee6-6b2e-40d1-9b3a-87bcb64ce5b4)
![게시글 작성 제한](https://github.com/user-attachments/assets/c8516d10-3e4e-43e7-8388-e2b7efc02aea)

-   카테고리 선택 (예금 / 적금 / 기타)
-   제목 및 내용 입력
-   이미지 첨부 기능
-   로그인 한 사용자만 게시글 및 댓글 작성 가능

#### 게시글 조회 및 검색

![게시글 조회 및 검색](https://github.com/user-attachments/assets/00c52e22-f905-42a7-90b1-1e41c81df840)

-   카테고리별 필터링
-   검색 기능
-   페이지네이션

#### 게시글 수정 및 댓글 작성, 삭제

![게시글 수정](https://github.com/user-attachments/assets/72aae4db-072e-4ce2-8dfb-003533889485)

-   작성자만 수정 / 삭제 가능
-   권한 검증

</details>

### 6. 금융 정보

<details>
<summary><b>은행 찾기 & 금·은 시세</b></summary>

#### 은행 지점 찾기

![은행 지점 찾기](https://github.com/user-attachments/assets/4beb795b-d4c9-4bf1-9b7c-5d3b9e253b6c)

-   카카오맵 연동
-   시/도 → 시/군/구 → 은행 3단계 검색
-   지도 마커 표시
-   지점 정보 제공 (주소, 전화번호)

#### 금·은 시세 비교

![금은 시세](https://github.com/user-attachments/assets/d266ca58-eacf-4be1-8b25-8912af74c308)

-   금 / 은 가격 차트 제공
-   날짜 범위 필터링
-   실시간 시세 확인

</details>

### 7. 금융 교육

<details>
<summary><b>유튜브 금융 콘텐츠</b></summary>

![유튜브 검색](https://github.com/user-attachments/assets/29851846-8789-4635-ab69-19ff36f0b62d)

-   금융 용어 검색 기능
-   5개 카테고리
    -   기본 개념
    -   금리 이해
    -   가입 방법
    -   주의 사항
    -   절세 활용
-   총 24개 금융 용어 카드
-   유튜브 영상 검색 및 재생
-   무한 스크롤

</details>

<br/>

## 🐛 트러블슈팅

### 1. CORS 에러

**문제**: 프론트엔드에서 백엔드 API 호출 시 CORS 에러 발생

**해결**: Django settings.py에 CORS 설정 추가

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### 2. AI 응답 지연 및 타임아웃

**문제**: OpenAI API 호출 시 응답 시간이 길어 사용자 경험 저하

**해결**:

-   로딩 스피너 UI 추가
-   타임아웃 설정 (25초)
-   에러 발생 시 기본 메시지 제공

```python
try:
    response = requests.post(gms_url, json=payload, timeout=25)
except requests.Timeout:
    return Response({"detail": "AI 분석 요청 시간이 초과되었습니다."}, status=504)
```

### 3. AI 응답 파싱 오류

**문제**: GPT 응답 형식이 불규칙하여 파싱 실패

**해결**:

-   프롬프트에 명확한 형식 지정 (`1. 한줄평:`, `2. 종합 분석:` 등)
-   정규표현식 유연하게 작성 (`[:：]` 전각/반각 모두 대응)
-   기본값(fallback) 설정으로 파싱 실패 시에도 정상 동작

### 4. 중복 가입 문제

**문제**: 이미 가입한 상품을 재가입할 수 있는 버그

**해결**:

-   프론트엔드에서 가입 전 중복 체크
-   백엔드에서 unique_together 제약 조건 설정

```python
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")
```

### 5. 카카오맵 SDK 로딩 타이밍 이슈

**문제**: 페이지 로드 시 카카오맵 SDK가 준비되지 않아 에러 발생

**해결**: Promise 기반 SDK 로딩 함수 작성

```javascript
export function loadKakaoMap() {
    if (isLoaded && window.kakao?.maps) return Promise.resolve(window.kakao);

    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${key}&autoload=false`;
        script.onload = () => {
            window.kakao.maps.load(() => {
                isLoaded = true;
                resolve(window.kakao);
            });
        };
        document.head.appendChild(script);
    });
}
```

<br/>

## 📚 배운 점 & 느낀 점

### 기술적 성장

-   **AI 통합 경험**: GPT API를 실제 서비스에 통합하며 프롬프트 엔지니어링의 중요성 체감
-   **풀스택 개발**: Vue.js와 Django를 활용한 완전한 웹 애플리케이션 개발 경험
-   **RESTful API 설계**: 효율적인 엔드포인트 설계와 HTTP 상태 코드 활용
-   **외부 API 연동**: FSS, 카카오맵, 유튜브 등 다양한 API 통합 경험
-   **상태 관리**: Pinia를 활용한 전역 상태 관리 및 최적화

### 협업 & 프로젝트 관리

-   **역할 분담**: 각자 강점을 살린 Frontend/Backend 분업으로 효율성 증대
-   **문서화**: 플로우 차트, 와이어프레임, ERD 등 체계적인 설계 문서 작성
-   **Git 협업**: 브랜치 전략 수립 및 코드 리뷰를 통한 품질 관리

### UX/UI 설계

-   **사용자 중심 설계**: 금융 초보자를 타겟으로 한 직관적인 UI 구성
-   **반응형 디자인**: 모바일, 태블릿, 데스크톱 모두 지원
-   **에러 핸들링**: 사용자 친화적인 오류 메시지 및 가이드 제공

<br/>

## 🔮 향후 개선 사항

-   [ ] 소셜 로그인 (카카오, 네이버) 추가
-   [ ] 예/적금 모의 투자 서비스
-   [ ] 금융 용어 퀴즈
-   [ ] 알림 기능 (만기 알림, 금리 변동 알림)

<br/>

---

<div align="center">
  
**처음 재테크, 나만의 금융 친구 MoA**

Made by 안수연 & 최지현

</div>
