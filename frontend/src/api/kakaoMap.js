let isLoaded = false
let loadingPromise = null

export function loadKakaoMap() {
  if (isLoaded && window.kakao?.maps) return Promise.resolve(window.kakao)

  if (loadingPromise) return loadingPromise

  const key = import.meta.env.VITE_KAKAO_JS_KEY
  if (!key) {
    return Promise.reject(new Error('VITE_KAKAO_JS_KEY가 .env에 없습니다.'))
  }

  loadingPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${key}&autoload=false&libraries=services`
    script.async = true

    script.onload = () => {
      window.kakao.maps.load(() => {
        isLoaded = true
        resolve(window.kakao)
      })
    }
    script.onerror = () => reject(new Error('카카오맵 SDK 로드 실패'))
    document.head.appendChild(script)
  })

  return loadingPromise
}
