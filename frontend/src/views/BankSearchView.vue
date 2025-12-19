<template>
  <div class="bank-page">
    <h2 class="title">은행 지점 찾기</h2>
    <hr class="line" />

    <div class="content">
      <!-- 왼쪽 패널 -->
      <section class="panel">
        <!-- 광역시 / 도 -->
        <label class="label">광역시 / 도</label>
        <select v-model="sido" class="select" @change="onChangeSido">
          <option disabled value="">광역시 / 도를 선택하세요.</option>
          <option v-for="x in sidoList" :key="x" :value="x">{{ x }}</option>
        </select>

        <!-- 시 / 군 / 구 -->
        <label class="label">시 / 군 / 구</label>
        <select v-model="sigungu" class="select" :disabled="!sido">
          <option disabled value="">시 / 군 / 구를 선택하세요.</option>
          <option v-for="g in sigunguList" :key="g" :value="g">{{ g }}</option>
        </select>

        <!-- 은행 -->
        <label class="label">은행</label>
        <select v-model="bank" class="select">
          <option disabled value="">은행을 선택하세요.</option>
          <option v-for="b in bankList" :key="b" :value="b">{{ b }}</option>
        </select>

        <!-- 버튼 -->
        <button class="btn" @click="searchBanks" :disabled="isSearching">
          {{ isSearching ? '검색 중...' : '찾기' }}
        </button>

        <!-- 결과 -->
        <div class="result">
          <div class="result-title">검색 결과</div>
          <div v-if="results.length === 0" class="empty">결과가 없습니다.</div>

          <ul v-else class="list">
            <li
              v-for="(p, idx) in results"
              :key="p.id"
              class="item"
              @click="focusPlace(p)"
            >
              <div class="name">{{ idx + 1 }}. {{ p.place_name }}</div>
              <div class="addr">{{ p.road_address_name || p.address_name }}</div>
              <div class="tel" v-if="p.phone">{{ p.phone }}</div>
            </li>
          </ul>
        </div>
      </section>

      <!-- 지도 -->
      <section class="map-wrap">
        <div ref="mapEl" class="map"></div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { loadKakaoMap } from '@/api/kakaoMap'

const mapEl = ref(null)
const map = ref(null)
const places = ref(null)
const markers = ref([])
const infoWindow = ref(null)

const isSearching = ref(false)
const results = ref([])

const sido = ref('')
const sigungu = ref('')
const bank = ref('')

/* 시 / 도 */
const sidoList = [
  '서울','부산','대구','인천','광주','대전','울산','세종',
  '경기','강원','충북','충남','전북','전남','경북','경남','제주'
]

/* 시 / 군 / 구 */
const sigunguMap = {
  서울: [
    '강남구','강동구','강북구','강서구','관악구','광진구','구로구','금천구',
    '노원구','도봉구','동대문구','동작구','마포구','서대문구','서초구',
    '성동구','성북구','송파구','양천구','영등포구','용산구','은평구',
    '종로구','중구','중랑구'
  ],

  부산: [
    '강서구','금정구','기장군','남구','동구','동래구','부산진구',
    '북구','사상구','사하구','서구','수영구','연제구','영도구','중구','해운대구'
  ],

  대구: [
    '남구','달서구','달성군','동구','북구','서구','수성구','중구'
  ],

  인천: [
    '강화군','계양구','남동구','동구','미추홀구','부평구',
    '서구','연수구','옹진군','중구'
  ],

  광주: [
    '광산구','남구','동구','북구','서구'
  ],

  대전: [
    '대덕구','동구','서구','유성구','중구'
  ],

  울산: [
    '남구','동구','북구','중구','울주군'
  ],

  세종: [
    '세종시'
  ],

  경기: [
    '가평군','고양시','과천시','광명시','광주시','구리시','군포시',
    '김포시','남양주시','동두천시','부천시','성남시','수원시',
    '시흥시','안산시','안성시','안양시','양주시','양평군','여주시',
    '연천군','오산시','용인시','의왕시','의정부시','이천시',
    '파주시','평택시','포천시','하남시','화성시'
  ],

  강원: [
    '강릉시','고성군','동해시','삼척시','속초시','양구군','양양군',
    '영월군','원주시','인제군','정선군','철원군','춘천시','태백시',
    '평창군','홍천군','화천군','횡성군'
  ],

  충북: [
    '괴산군','단양군','보은군','영동군','옥천군','음성군',
    '제천시','증평군','진천군','청주시','충주시'
  ],

  충남: [
    '계룡시','공주시','금산군','논산시','당진시','보령시',
    '부여군','서산시','서천군','아산시','예산군',
    '천안시','청양군','태안군','홍성군'
  ],

  전북: [
    '고창군','군산시','김제시','남원시','무주군','부안군',
    '순창군','완주군','익산시','임실군','장수군',
    '전주시','정읍시','진안군'
  ],

  전남: [
    '강진군','고흥군','곡성군','광양시','구례군','나주시',
    '담양군','목포시','무안군','보성군','순천시',
    '신안군','여수시','영광군','영암군','완도군',
    '장성군','장흥군','진도군','함평군','해남군','화순군'
  ],

  경북: [
    '경산시','경주시','고령군','구미시','군위군','김천시',
    '문경시','봉화군','상주시','성주군','안동시',
    '영덕군','영양군','영주시','영천시','예천군',
    '울릉군','울진군','의성군','청도군','청송군',
    '칠곡군','포항시'
  ],

  경남: [
    '거제시','거창군','고성군','김해시','남해군','밀양시',
    '사천시','산청군','양산시','의령군','진주시',
    '창녕군','창원시','통영시','하동군','함안군',
    '함양군','합천군'
  ],

  제주: [
    '서귀포시','제주시'
  ]
}

const sigunguList = ref([])

const bankList = [
  // 시중은행
  '국민은행','신한은행','하나은행','우리은행','농협은행',

  // 인터넷은행
  '카카오뱅크','토스뱅크','케이뱅크',

  // 특수 · 정책은행
  '기업은행','수협은행','우체국',

  // 외국계
  'SC제일은행','한국씨티은행',

  // 지방은행
  '부산은행','경남은행','광주은행',
  '전북은행','제주은행','대구은행',

  // 협동조합 · 기타
  '새마을금고','신협','저축은행'
]


function onChangeSido () {
  sigungu.value = ''
  sigunguList.value = sigunguMap[sido.value] || []
}

/* 지도 초기화 */
onMounted(async () => {
  const kakao = await loadKakaoMap()

  map.value = new kakao.maps.Map(mapEl.value, {
    center: new kakao.maps.LatLng(37.5665, 126.9780),
    level: 5,
    draggable: true,
    scrollwheel: true
  })

  places.value = new kakao.maps.services.Places()
  infoWindow.value = new kakao.maps.InfoWindow({ zIndex: 3 })
})

function clearMarkers () {
  markers.value.forEach(m => m.setMap(null))
  markers.value = []
}

/* 리스트 클릭 */
function focusPlace(place) {
  const kakao = window.kakao
  const latlng = new kakao.maps.LatLng(place.y, place.x)

  map.value.setCenter(latlng)
  map.value.setLevel(4)

  const marker = markers.value.find(m => m.__placeId === place.id)
  if (!marker) return

  infoWindow.value.setContent(`
    <div style="padding:8px 12px;font-size:13px;line-height:1.4;">
      <b>${place.place_name}</b><br/>
      ${place.road_address_name || place.address_name}<br/>
      ${place.phone || ''}
    </div>
  `)

  infoWindow.value.open(map.value, marker)
}

/* 검색 */
function searchBanks () {
  if (!sido.value || !sigungu.value || !bank.value) return

  isSearching.value = true
  results.value = []
  clearMarkers()

  const kakao = window.kakao
  const keyword = `${sido.value} ${sigungu.value} ${bank.value}`

  places.value.keywordSearch(keyword, (data, status) => {
    if (status !== kakao.maps.services.Status.OK) {
      isSearching.value = false
      return
   }

    results.value = data
    const bounds = new kakao.maps.LatLngBounds()

    data.forEach(p => {
      const pos = new kakao.maps.LatLng(p.y, p.x)
      bounds.extend(pos)

      const marker = new kakao.maps.Marker({ map: map.value, position: pos })
      marker.__placeId = p.id
      markers.value.push(marker)

      kakao.maps.event.addListener(marker, 'click', () => {
        map.value.setCenter(pos)
        infoWindow.value.setContent(`
          <div style="padding:8px 12px;font-size:13px;">
            <b>${p.place_name}</b><br/>
            ${p.road_address_name || p.address_name}<br/>
            ${p.phone || ''}
          </div>
        `)
        infoWindow.value.open(map.value, marker)
      })
    })

    map.value.setBounds(bounds)
    isSearching.value = false
  })
}
</script>

<style scoped>
.bank-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px;
}

.title {
  font-size: 28px;
  font-weight: 700;
  margin: 10px 0 12px;
}

.line {
  border: none;
  border-top: 1px solid #111;
  margin-bottom: 24px;
}

.content {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 24px;
}

.panel {
  padding: 12px 8px;
}

.label {
  display: block;
  font-weight: 700;
  margin: 20px 0 8px;
}

.select {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  border: 1px solid #ccc;
  font-size: 15px;
  padding: 0 52px 0 14px;
  appearance: none;
  background-color: #fff;
  background-image: url("data:image/svg+xml,%3Csvg width='14' height='8' viewBox='0 0 14 8' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1L7 7L13 1' stroke='%23999' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 22px center;
}

.select:focus {
  border-color: #6393F2;
  box-shadow: 0 0 0 2px rgba(99,147,242,0.15);
  outline: none;
}

.btn {
  margin-top: 22px;
  width: 100%;
  height: 52px;
  border-radius: 14px;
  border: none;
  background: #6393F2;
  color: #fff;
  font-weight: 700;
  font-size: 16px;
  cursor: pointer;
}

.btn:hover {
  background: #4f7fe8;
}

.result {
  margin-top: 22px;
}

.result-title {
  font-weight: 800;
  margin-bottom: 12px;
}

.empty {
  font-size: 14px;
  color: #777;
}

.item {
  padding: 12px 10px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.item:hover {
  background: #f3f7ff;
}

.map-wrap {
  border: 1px solid #eee;
  border-radius: 14px;
  overflow: hidden;
}

.map {
  width: 100%;
  height: 560px;
}
</style>
