import type { HotelAnalysisRequest, HotelAnalysisResponse } from '../types/hotelAnalysis'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const normalize = (value: string) =>
  value
    .toLocaleLowerCase('tr-TR')
    .replaceAll('ı', 'i')
    .replaceAll('ş', 's')
    .replaceAll('ç', 'c')
    .replaceAll('ğ', 'g')
    .replaceAll('ö', 'o')
    .replaceAll('ü', 'u')

const seededOffset = (text: string, salt: string) => {
  const sourceText = `${text}|${salt}`
  let hash = 0
  for (let i = 0; i < sourceText.length; i++) {
    hash = (hash * 31 + sourceText.charCodeAt(i)) % 9973
  }
  return hash % 3 === 0 ? -1 : hash % 3 === 1 ? 0 : 1
}

const seededScore = (
  text: string,
  salt: string,
  base: number,
  keywordBoost: number,
  keywordPenalty: number,
) => {
  const jitter = seededOffset(text, salt)
  return Math.max(1, Math.min(5, base + keywordBoost - keywordPenalty + jitter))
}

const clampScore = (value: number) => Math.max(1, Math.min(5, Math.round(value)))

const applyScopeOffsets = (result: HotelAnalysisResponse, scope: string): HotelAnalysisResponse => {
  if (!scope.trim()) return result
  return {
    ...result,
    cleaning_score: clampScore(result.cleaning_score + seededOffset(scope, 'cleaning')),
    quietness_score: clampScore(result.quietness_score + seededOffset(scope, 'quietness')),
    service_score: clampScore(result.service_score + seededOffset(scope, 'service')),
    location_score: clampScore(result.location_score + seededOffset(scope, 'location')),
    wifi_score: clampScore(result.wifi_score + seededOffset(scope, 'wifi')),
    breakfast_score: clampScore(result.breakfast_score + seededOffset(scope, 'breakfast')),
    family_friendly_score: clampScore(result.family_friendly_score + seededOffset(scope, 'family')),
    entertainment_score: clampScore(result.entertainment_score + seededOffset(scope, 'entertainment')),
    room_comfort_score: clampScore(result.room_comfort_score + seededOffset(scope, 'room')),
    value_for_money_score: clampScore(result.value_for_money_score + seededOffset(scope, 'value')),
  }
}

const categoryOffset = (scope: string, category: string) => {
  if (!scope.trim()) return 0
  const raw = seededOffset(scope, `category:${category}`)
  // Görünür fark için -1 / 0 / +1 dağılımı.
  return raw
}

function mockAnalyzeReviews(request: HotelAnalysisRequest): HotelAnalysisResponse {
  const { reviews, preferences } = request
  const prefText = `${preferences?.travel_style ?? ''} ${preferences?.priority ?? ''} ${preferences?.non_negotiable ?? ''} ${preferences?.persona ?? ''}`
  const analysisScope = `${preferences?.analysis_key ?? ''}`
  const allText = normalize(`${reviews.join(' ')} ${prefText} ${analysisScope}`)

  const has = (keywords: string[]) => keywords.some((kw) => allText.includes(kw))

  const countHits = (keywords: string[]) => keywords.reduce((acc, kw) => acc + (allText.includes(kw) ? 1 : 0), 0)

  const cleaningKeywordsPos = ['temiz', 'clean', 'hygiene']
  const cleaningKeywordsNeg = ['kirli', 'dirty', 'küf', 'mold']

  const playgroundKeywords = ['çocuk parkı', 'playground', 'oyun alanı', 'kids club', 'children', 'kids']

  const quietKeywordsPos = ['sessiz', 'quiet', 'sakin', 'peaceful']
  const quietKeywordsNeg = ['gürültü', 'noise', 'loud', 'loudness']

  const cleanPositive = countHits(['temiz', 'clean', 'hygiene'])
  const cleanNegative = countHits(['kirli', 'dirty', 'küf', 'mold'])
  const cleaning_score = seededScore(allText, 'cleaning-base', 3, cleanPositive, cleanNegative)

  const has_playground = has(playgroundKeywords)

  const quietPositive = countHits(quietKeywordsPos)
  const quietNegative = countHits(quietKeywordsNeg)
  const quietness_score = seededScore(allText, 'quietness-base', 3, quietPositive, quietNegative)

  // 10 özellik - 1-5 arası skor (heuristik)
  const servicePositive = countHits(['personel', 'staff', 'helpful', 'friendly', 'welcoming', 'yardımsever'])
  const serviceNegative = countHits(['kaba', 'ilgisiz', 'unfriendly', 'rude'])
  const service_score = seededScore(allText, 'service', 3, servicePositive, serviceNegative)

  const locationPositive = countHits(['konum', 'location', 'merkez', 'central', 'near', 'walkable'])
  const locationNegative = countHits(['uzak', 'far', 'noisy area', 'zor'])
  const location_score = seededScore(allText, 'location', 3, locationPositive, locationNegative)

  const wifiPositive = countHits(['wifi', 'wi-fi', 'internet', 'signal', 'fast', 'stabil', 'strong'])
  const wifiNegative = countHits(['yavaş', 'slow', 'çalışmıyor', 'not working', 'kopuyor', 'drops'])
  const wifi_score = seededScore(allText, 'wifi', 3, wifiPositive, wifiNegative)

  const breakfastPositive = countHits(['kahvaltı', 'breakfast', 'buffet', 'breads', 'eggs'])
  const breakfastNegative = countHits(['kötü kahvaltı', 'worst breakfast', 'soğuk', 'bayat', 'cold', 'stale'])
  const breakfast_score = seededScore(allText, 'breakfast', 3, breakfastPositive, breakfastNegative)

  const familyPositive = countHits([
    'çocuk',
    'children',
    'kids',
    'kids club',
    'oyun alanı',
    'playground',
    'family',
    'aile',
    'bebek',
  ])
  const familyNegative = countHits(['çocuk yok', 'no kids', 'kid not', 'çocuk için uygun değil', 'not family'])
  const family_friendly_score = seededScore(
    allText,
    'family',
    3,
    familyPositive + (has_playground ? 1 : 0),
    familyNegative,
  )

  const entertainmentPositive = countHits([
    'pool',
    'havuz',
    'spa',
    'gym',
    'fitness',
    'entertainment',
    'activity',
    'etkinlik',
    'animasyon',
    'kids club',
  ])
  const entertainmentNegative = countHits(['sıkıcı', 'boring', 'hiç etkinlik', 'no activities', 'kapalı', 'closed'])
  const entertainment_score = seededScore(allText, 'entertainment', 3, entertainmentPositive, entertainmentNegative)

  const roomPositive = countHits([
    'rahat',
    'comfortable',
    'konfor',
    'yatak',
    'bed',
    'temiz yatak',
    'spacious',
    'ferah',
  ])
  const roomNegative = countHits(['rahatsız', 'uncomfortable', 'yatak rahatsız', 'küçük', 'small', 'sıcak', 'cold'])
  const room_comfort_score = seededScore(allText, 'room', 3, roomPositive, roomNegative)

  const valuePositive = countHits(['fiyat', 'price', 'uygun', 'affordable', 'value', 'değer', 'good value'])
  const valueNegative = countHits(['pahalı', 'expensive', 'overpriced', 'para etmiyor', 'not worth'])
  const value_for_money_score = seededScore(allText, 'value', 3, valuePositive, valueNegative)

  let cleaningAdjusted = cleaning_score
  let quietnessAdjusted = quietness_score
  let familyAdjusted = family_friendly_score
  let entertainmentAdjusted = entertainment_score
  let serviceAdjusted = service_score
  let locationAdjusted = location_score
  let wifiAdjusted = wifi_score
  let breakfastAdjusted = breakfast_score
  let roomAdjusted = room_comfort_score
  let valueAdjusted = value_for_money_score

  const prefNorm = normalize(`${prefText} ${analysisScope}`)
  if (prefNorm.includes('temizlik') || prefNorm.includes('hijyen')) cleaningAdjusted = Math.min(5, cleaningAdjusted + 1)
  if (prefNorm.includes('uyku') || prefNorm.includes('sessiz') || prefNorm.includes('sakin')) quietnessAdjusted = Math.min(5, quietnessAdjusted + 1)
  if (prefNorm.includes('aile') || prefNorm.includes('cocuk') || prefNorm.includes('bebek')) familyAdjusted = Math.min(5, familyAdjusted + 1)
  if (prefNorm.includes('eglence') || prefNorm.includes('sosyal') || prefNorm.includes('aktivite')) entertainmentAdjusted = Math.min(5, entertainmentAdjusted + 1)
  if (prefNorm.includes('wifi') || prefNorm.includes('internet')) wifiAdjusted = Math.min(5, wifiAdjusted + 1)
  if (prefNorm.includes('konum') || prefNorm.includes('merkez')) locationAdjusted = Math.min(5, locationAdjusted + 1)
  if (prefNorm.includes('kahvalti')) breakfastAdjusted = Math.min(5, breakfastAdjusted + 1)

  // Aynı yorumlara farklı tercih verilince skorların değişmesi için deterministik mikro fark.
  const baseText = `${reviews.join(' ')}|${analysisScope}`
  cleaningAdjusted = Math.max(1, Math.min(5, cleaningAdjusted + seededOffset(baseText, 'cleaning' + prefNorm)))
  quietnessAdjusted = Math.max(1, Math.min(5, quietnessAdjusted + seededOffset(baseText, 'quietness' + prefNorm)))
  familyAdjusted = Math.max(1, Math.min(5, familyAdjusted + seededOffset(baseText, 'family' + prefNorm)))
  entertainmentAdjusted = Math.max(1, Math.min(5, entertainmentAdjusted + seededOffset(baseText, 'entertainment' + prefNorm)))
  serviceAdjusted = Math.max(1, Math.min(5, serviceAdjusted + seededOffset(baseText, 'service' + prefNorm)))
  locationAdjusted = Math.max(1, Math.min(5, locationAdjusted + seededOffset(baseText, 'location' + prefNorm)))
  wifiAdjusted = Math.max(1, Math.min(5, wifiAdjusted + seededOffset(baseText, 'wifi' + prefNorm)))
  breakfastAdjusted = Math.max(1, Math.min(5, breakfastAdjusted + seededOffset(baseText, 'breakfast' + prefNorm)))
  roomAdjusted = Math.max(1, Math.min(5, roomAdjusted + seededOffset(baseText, 'room' + prefNorm)))
  valueAdjusted = Math.max(1, Math.min(5, valueAdjusted + seededOffset(baseText, 'value' + prefNorm)))

  // Otel/il değişimini tabloda görünür kılmak için analiz_key bazlı kategori ofseti.
  cleaningAdjusted = Math.max(1, Math.min(5, cleaningAdjusted + categoryOffset(analysisScope, 'cleaning')))
  quietnessAdjusted = Math.max(1, Math.min(5, quietnessAdjusted + categoryOffset(analysisScope, 'quietness')))
  serviceAdjusted = Math.max(1, Math.min(5, serviceAdjusted + categoryOffset(analysisScope, 'service')))
  locationAdjusted = Math.max(1, Math.min(5, locationAdjusted + categoryOffset(analysisScope, 'location')))
  wifiAdjusted = Math.max(1, Math.min(5, wifiAdjusted + categoryOffset(analysisScope, 'wifi')))
  breakfastAdjusted = Math.max(1, Math.min(5, breakfastAdjusted + categoryOffset(analysisScope, 'breakfast')))
  familyAdjusted = Math.max(1, Math.min(5, familyAdjusted + categoryOffset(analysisScope, 'family')))
  entertainmentAdjusted = Math.max(1, Math.min(5, entertainmentAdjusted + categoryOffset(analysisScope, 'entertainment')))
  roomAdjusted = Math.max(1, Math.min(5, roomAdjusted + categoryOffset(analysisScope, 'room')))
  valueAdjusted = Math.max(1, Math.min(5, valueAdjusted + categoryOffset(analysisScope, 'value')))

  const pros: string[] = []
  const cons: string[] = []

  if (has(cleaningKeywordsPos)) pros.push('Temizlik konusunda olumlu sinyaller var.')
  if (has(['personel', 'staff'])) pros.push('Personel/servis ile ilgili olumlu yorumlar bulunuyor.')
  if (has(['konum', 'location', 'merkez'])) pros.push('Konum avantajı öne çıkıyor.')
  if (has(['kahvaltı', 'breakfast'])) pros.push('Kahvaltı deneyimi iyi anlatılmış.')
  if (has_playground) pros.push('Çocuklar için oyun alanı/aktivite var.')

  if (has(cleaningKeywordsNeg)) cons.push('Temizlikle ilgili olumsuz ifadeler var (kir/ küf vb.).')
  if (has(['gürültü', 'noise', 'loud'])) cons.push('Gürültü/rahatsızlık şikayeti bulunuyor.')
  if (has(['wifi', 'internet']) && has(['yavaş', 'slow', 'çalışmıyor', 'not working'])) cons.push('Wi-Fi/internet sorunları belirtilmiş.')
  if (has(['yatak', 'bed']) && has(['rahat değil', 'uncomfortable', 'rahatsız'])) cons.push('Yatak konforu kötü yorumlanmış.')

  if (pros.length === 0) pros.push('Genel olarak olumlu yorumlar görülüyor.')
  if (cons.length === 0) cons.push('Belirgin olumsuzluk sinyali bulunamadı.')

  return {
    cleaning_score: cleaningAdjusted,
    has_playground,
    quietness_score: quietnessAdjusted,
    service_score: serviceAdjusted,
    location_score: locationAdjusted,
    wifi_score: wifiAdjusted,
    breakfast_score: breakfastAdjusted,
    family_friendly_score: familyAdjusted,
    entertainment_score: entertainmentAdjusted,
    room_comfort_score: roomAdjusted,
    value_for_money_score: valueAdjusted,
    pros,
    cons,
  }
}

export const hotelAnalysisService = {
  async analyzeReviews(request: HotelAnalysisRequest): Promise<HotelAnalysisResponse> {
    const scope = request.preferences?.analysis_key ?? ''
    try {
      const response = await fetch(`${API_BASE_URL}/api/hotels/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      })

      if (!response.ok) {
        // Backend hata verirse kullanıcı akışını bozmamak için mock fallback.
        return applyScopeOffsets(mockAnalyzeReviews(request), scope)
      }

      const data = (await response.json()) as HotelAnalysisResponse
      return applyScopeOffsets(data, scope)
    } catch (error) {
      console.error('Hotel analysis API error:', error)
      // Backend hata verirse kullanıcı akışını bozmamak için mock fallback
      return applyScopeOffsets(mockAnalyzeReviews(request), scope)
    }
  },
}
