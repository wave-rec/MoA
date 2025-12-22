// 금융 용어 데이터 (토스뱅크 아티클 기반)

export const FINANCIAL_TERMS = [
  // 📚 기본 개념
  {
    category: '기본개념',
    emoji: '📚',
    title: '예금 vs 적금 차이',
    description: '목돈 굴리기와 목돈 만들기의 차이점',
    query: '예금 적금 차이 쉽게 설명',
    keywords: ['예금', '적금', '정기예금', '정기적금'],
  },
  {
    category: '기본개념',
    emoji: '🏦',
    title: '파킹통장이란?',
    description: '하루만 맡겨도 이자 받는 통장',
    query: '파킹통장 뜻 장단점',
    keywords: ['파킹통장', '수시입출금', '보통예금'],
  },
  {
    category: '기본개념',
    emoji: '🛡️',
    title: '예금자 보호제도',
    description: '5000만원까지 보호받는 방법',
    query: '예금자 보호제도 5000만원',
    keywords: ['예금자보호', '예보', '5000만원'],
  },
  {
    category: '기본개념',
    emoji: '💰',
    title: '자유적금 vs 정기적금',
    description: '자유롭게 저축 vs 정기적 저축',
    query: '자유적금 정기적금 차이',
    keywords: ['자유적금', '정기적금', '적금종류'],
  },

  // 📊 금리 이해
  {
    category: '금리이해',
    emoji: '📊',
    title: '복리 vs 단리',
    description: '이자에도 이자가 붙는다?',
    query: '복리 단리 차이 계산',
    keywords: ['복리', '단리', '이자계산'],
  },
  {
    category: '금리이해',
    emoji: '📈',
    title: '우대금리 받는 법',
    description: '최고금리로 이자 더 받기',
    query: '예금 적금 우대금리 조건',
    keywords: ['우대금리', '최고금리', '금리우대'],
  },
  {
    category: '금리이해',
    emoji: '💹',
    title: '금리 비교하는 법',
    description: '어느 은행이 금리가 높을까?',
    query: '은행 예금 적금 금리 비교',
    keywords: ['금리비교', '예금금리', '적금금리'],
  },
  {
    category: '금리이해',
    emoji: '🎯',
    title: '실질금리란?',
    description: '물가상승률 고려한 진짜 금리',
    query: '실질금리 명목금리 차이',
    keywords: ['실질금리', '명목금리', '물가'],
  },

  // 🔐 가입 방법
  {
    category: '가입방법',
    emoji: '📱',
    title: '비대면 계좌 개설',
    description: '집에서 간편하게 통장 만들기',
    query: '비대면 예금 계좌 개설 방법',
    keywords: ['비대면', '계좌개설', '인터넷뱅킹'],
  },
  {
    category: '가입방법',
    emoji: '👨‍👩‍👧',
    title: '미성년자 통장',
    description: '자녀 명의로 통장 만들기',
    query: '미성년자 예금 적금 만들기',
    keywords: ['미성년자', '자녀통장', '청소년'],
  },
  {
    category: '가입방법',
    emoji: '🆔',
    title: '계좌 개설 준비물',
    description: '통장 만들 때 필요한 것들',
    query: '예금 계좌 개설 필요 서류',
    keywords: ['계좌개설', '준비물', '신분증'],
  },
  {
    category: '가입방법',
    emoji: '🔄',
    title: '예금 갈아타기',
    description: '더 높은 금리로 옮기기',
    query: '예금 갈아타기 방법',
    keywords: ['갈아타기', '예금이동', '전환'],
  },

  // ⚠️ 주의사항
  {
    category: '주의사항',
    emoji: '⚠️',
    title: '중도해지 불이익',
    description: '만기 전에 깨면 손해?',
    query: '예금 적금 중도해지 불이익',
    keywords: ['중도해지', '위약금', '해지'],
  },
  {
    category: '주의사항',
    emoji: '💸',
    title: '이자소득세란?',
    description: '이자에도 세금이 붙어요',
    query: '예금 이자소득세 세율',
    keywords: ['이자소득세', '세금', '세율'],
  },
  {
    category: '주의사항',
    emoji: '🚨',
    title: '보이스피싱 예방',
    description: '금융사기 당하지 않는 법',
    query: '보이스피싱 예방 방법',
    keywords: ['보이스피싱', '금융사기', '피싱'],
  },
  {
    category: '주의사항',
    emoji: '🔒',
    title: '휴면계좌 관리',
    description: '안 쓰는 통장 어떻게 할까?',
    query: '휴면계좌 해지 찾기',
    keywords: ['휴면계좌', '잠자는돈', '계좌정리'],
  },

  // 💡 절세/활용
  {
    category: '절세활용',
    emoji: '💡',
    title: '비과세 예금',
    description: '세금 안 내고 이자 받기',
    query: '비과세 예금 적금 조건',
    keywords: ['비과세', '세금면제', '노인우대'],
  },
  {
    category: '절세활용',
    emoji: '🎁',
    title: '목돈 굴리는 법',
    description: '1억 있으면 어디에 넣을까?',
    query: '목돈 굴리기 예금 재테크',
    keywords: ['목돈굴리기', '재테크', '자산관리'],
  },
  {
    category: '절세활용',
    emoji: '💰',
    title: '비상금 통장 만들기',
    description: '급할 때 쓸 돈 관리법',
    query: '비상금 통장 추천 파킹통장',
    keywords: ['비상금', '예비자금', '파킹'],
  },
  {
    category: '절세활용',
    emoji: '📅',
    title: '만기일 선택 팁',
    description: '언제 만기를 정할까?',
    query: '예금 만기일 정하는 방법',
    keywords: ['만기일', '저축기간', '만기'],
  },
]

// 카테고리별 색상
export const CATEGORY_COLORS = {
  기본개념: { bg: '#EBF5FF', text: '#2563EB', icon: '📚' },
  금리이해: { bg: '#F0FDF4', text: '#16A34A', icon: '📊' },
  가입방법: { bg: '#FEF3C7', text: '#D97706', icon: '🔐' },
  주의사항: { bg: '#FEE2E2', text: '#DC2626', icon: '⚠️' },
  절세활용: { bg: '#F3E8FF', text: '#9333EA', icon: '💡' },
}
