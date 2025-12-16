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
  서울: ['강남구','서초구','송파구','마포구','영등포구','종로구','중구','용산구'],
  경기: ['수원시','성남시','부천시','고양시','용인시','안양시','평택시'],
  부산: ['해운대구','부산진구','동래구','남구','사하구'],
  대구: ['중구','동구','서구','남구','북구','수성구','달서구'],
  인천: ['남동구','연수구','부평구','서구','미추홀구'],
  광주: ['동구','서구','남구','북구','광산구'],
  대전: ['동구','중구','서구','유성구','대덕구'],
  울산: ['중구','남구','동구','북구','울주군'],
  세종: ['세종시'],
  강원: ['춘천시','원주시','강릉시','속초시'],
  충북: ['청주시','충주시','제천시'],
  충남: ['천안시','아산시','서산시'],
  전북: ['전주시','군산시','익산시'],
  전남: ['목포시','여수시','순천시'],
  경북: ['포항시','경주시','구미시','안동시'],
  경남: ['창원시','김해시','양산시','진주시'],
  제주: ['제주시','서귀포시']
}

const sigunguList = ref([])

const bankList = [
  '국민은행','신한은행','하나은행','우리은행',
  '농협은행','기업은행','카카오뱅크','토스뱅크'
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
