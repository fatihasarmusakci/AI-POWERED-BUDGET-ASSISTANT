import type { VibecheckService } from './vibecheck-service'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const buildMapsUrl = (name: string, address: string) =>
  `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${name} ${address} otel`)}`

export const vibecheckLiveService: VibecheckService = {
  getBundle: async (city: string) => {
    const hotelsResponse = await fetch(
      `${API_BASE}/places/hotels?city=${encodeURIComponent(city)}&limit=6&light=true`,
    )

    if (!hotelsResponse.ok) {
      let detail = 'Otel verisi alınamadı.'
      try {
        const errBody = (await hotelsResponse.json()) as { detail?: string }
        if (errBody.detail) {
          detail = errBody.detail
        }
      } catch {
        // ignore parse errors
      }
      throw new Error(detail)
    }

    const hotelsData = (await hotelsResponse.json()) as {
      items: Array<{
        place_id: string
        name: string
        address: string
        rating?: number | null
        user_rating_count?: number | null
        booking_url?: string | null
        reviews: string[]
        analysis: {
          cleaning_score: number
          quietness_score: number
          wifi_score: number
          pros: string[]
          cons: string[]
        }
      }>
    }

    if (!Array.isArray(hotelsData.items) || hotelsData.items.length === 0) {
      throw new Error(`${city} için canlı otel verisi bulunamadı.`)
    }

    return {
      dataSource: 'live' as const,
      personas: ['Sakin Tatilci', 'Sosyal Kaşif', 'Verim Odaklı'],
      hotels: hotelsData.items.map((item) => ({
        id: item.place_id,
        name: item.name,
        district: item.address || city,
        officialPhotoLabel: 'Resmi bilgi',
        userPhotoLabel: 'Kullanıcı yorum özeti',
        bookingUrl:
          item.booking_url && !item.booking_url.includes('foursquare.com/placemakers')
            ? item.booking_url
            : buildMapsUrl(item.name, item.address || city),
        highlights: item.analysis.pros.slice(0, 3),
        amenities: [
          item.rating ? `Foursquare puanı: ${item.rating}/10` : 'Otel kaydı doğrulandı',
          item.user_rating_count ? `${item.user_rating_count} değerlendirme` : 'Değerlendirme sayısı yok',
          'Harita üzerinden rezervasyon',
        ],
        officialDate: new Date().toISOString().slice(0, 10),
        userDate: new Date().toISOString().slice(0, 10),
        smartScore: Number(
          ((item.analysis.cleaning_score + item.analysis.quietness_score + item.analysis.wifi_score) / 1.5).toFixed(1),
        ),
        wifiScore: item.analysis.wifi_score,
        sleepScore: item.analysis.quietness_score,
        socialScore: 7,
        reviews: item.reviews,
        flags: item.analysis.cons.slice(0, 3),
        summary: item.analysis.pros.slice(0, 3).join(' ') || `${item.name} için canlı veri özeti.`,
      })),
      mapLayers: [],
      insight: {
        city,
        message: `${city} için Foursquare araması tamamlandı (hafif mod — fotoğraf API'si kullanılmadı).`,
      },
      staycation: {
        coworking: 8.5,
        brunch: 8.8,
        wifiReliability: 8.6,
      },
    }
  },
}
