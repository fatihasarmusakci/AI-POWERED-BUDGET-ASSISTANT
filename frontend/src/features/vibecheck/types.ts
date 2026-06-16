export type PersonaType =
  | 'Sakin Tatilci'
  | 'Sosyal Kaşif'
  | 'Verim Odaklı'

export type SurfaceType = 'decision' | 'retention'

export interface HotelCard {
  id: string
  name: string
  district: string
  officialPhotoLabel: string
  userPhotoLabel: string
  officialPhotoUrl?: string
  userPhotoUrl?: string
  bookingUrl?: string
  highlights?: string[]
  amenities?: string[]
  officialDate: string
  userDate: string
  smartScore: number
  wifiScore: number
  sleepScore: number
  socialScore: number
  /**
   * Review analiz ekranı için (temizlik, sessizlik ve çocuk parkı gibi).
   * Live backend `/hotels` endpoint’i şu an ham yorum döndürmüyor; bu alan isteğe bağlı.
   */
  reviews?: string[]
  flags: string[]
  summary: string
}

export interface MapLayer {
  id: string
  label: string
  emoji: string
}

export interface InsightCard {
  city: string
  message: string
}

export interface StaycationScores {
  coworking: number
  brunch: number
  wifiReliability: number
}

export interface VibecheckDataBundle {
  dataSource?: 'demo' | 'live'
  personas: PersonaType[]
  hotels: HotelCard[]
  mapLayers: MapLayer[]
  insight: InsightCard
  staycation: StaycationScores
}
