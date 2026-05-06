export type PersonaType =
  | 'Quiet Seeker'
  | 'Social Butterfly'
  | 'Productivity Focused'

export type SurfaceType = 'decision' | 'retention'

export interface HotelCard {
  id: string
  name: string
  district: string
  officialPhotoLabel: string
  userPhotoLabel: string
  officialDate: string
  userDate: string
  smartScore: number
  wifiScore: number
  sleepScore: number
  socialScore: number
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
  personas: PersonaType[]
  hotels: HotelCard[]
  mapLayers: MapLayer[]
  insight: InsightCard
  staycation: StaycationScores
}
