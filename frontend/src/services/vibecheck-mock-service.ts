import type { VibecheckDataBundle } from '../features/vibecheck/types'
import type { VibecheckService } from './vibecheck-service'

const mockBundle: VibecheckDataBundle = {
  personas: ['Quiet Seeker', 'Social Butterfly', 'Productivity Focused'],
  hotels: [
    {
      id: 'camden-loft',
      name: 'Camden Loft Hotel',
      district: 'Camden',
      officialPhotoLabel: 'Official: Rooftop suite photo',
      userPhotoLabel: 'User: Same room, natural light',
      officialDate: '2024-09-12',
      userDate: '2026-04-25',
      smartScore: 8.4,
      wifiScore: 9,
      sleepScore: 6,
      socialScore: 8,
      flags: ['12 duplicate phrases', '4 same-IP reviews'],
      summary:
        'Pros: Great coffee and stable Wi-Fi. Cons: Elevator waits at peak hours. Vibe: Industrial, youthful, and active.',
    },
    {
      id: 'shoreditch-stay',
      name: 'Shoreditch Stay',
      district: 'Shoreditch',
      officialPhotoLabel: 'Official: Minimalist business room',
      userPhotoLabel: 'User: Desk setup with noise meter',
      officialDate: '2025-01-10',
      userDate: '2026-04-21',
      smartScore: 8.8,
      wifiScore: 9,
      sleepScore: 8,
      socialScore: 7,
      flags: ['3 repetitive 5-star templates'],
      summary:
        'Pros: Strong desk setup and quiet nights. Cons: Gym is small. Vibe: Focused, design-driven, and balanced.',
    },
  ],
  mapLayers: [
    { id: 'quiet', label: 'Quiet zone', emoji: 'Q' },
    { id: 'party', label: 'Party zone', emoji: 'P' },
    { id: 'metro', label: 'Near metro', emoji: 'M' },
  ],
  insight: {
    city: 'London',
    message:
      'Best honest breakfast workspace this week is in Soho; quietest hours are 08:00-10:00.',
  },
  staycation: {
    coworking: 8.7,
    brunch: 9.1,
    wifiReliability: 8.9,
  },
}

export const vibecheckMockService: VibecheckService = {
  getBundle: async () => mockBundle,
}
