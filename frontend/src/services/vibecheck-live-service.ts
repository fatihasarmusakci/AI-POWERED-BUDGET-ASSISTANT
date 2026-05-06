import type { VibecheckService } from './vibecheck-service'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export const vibecheckLiveService: VibecheckService = {
  getBundle: async () => {
    const [hotelsResponse, insightResponse] = await Promise.all([
      fetch(`${API_BASE}/hotels?city=london`),
      fetch(`${API_BASE}/insights/daily?city=london`),
    ])

    if (!hotelsResponse.ok || !insightResponse.ok) {
      throw new Error('Failed to fetch live data')
    }

    const hotelsData = (await hotelsResponse.json()) as {
      items: Array<{
        id: string
        name: string
        district: string
        smart_score: number
      }>
    }
    const insightData = (await insightResponse.json()) as {
      city: string
      message: string
    }

    return {
      personas: ['Quiet Seeker', 'Social Butterfly', 'Productivity Focused'],
      hotels: hotelsData.items.map((item) => ({
        id: item.id,
        name: item.name,
        district: item.district,
        officialPhotoLabel: 'Official: Gallery photo',
        userPhotoLabel: 'User: Recent unfiltered upload',
        officialDate: '2025-01-10',
        userDate: '2026-04-21',
        smartScore: item.smart_score,
        wifiScore: 8,
        sleepScore: 8,
        socialScore: 8,
        flags: ['Live integration placeholder'],
        summary: 'Live summary will be fed from /hotels/{id}/summary endpoint.',
      })),
      mapLayers: [
        { id: 'quiet', label: 'Quiet zone', emoji: 'Q' },
        { id: 'party', label: 'Party zone', emoji: 'P' },
        { id: 'metro', label: 'Near metro', emoji: 'M' },
      ],
      insight: {
        city: insightData.city,
        message: insightData.message,
      },
      staycation: {
        coworking: 8.5,
        brunch: 8.8,
        wifiReliability: 8.6,
      },
    }
  },
}
