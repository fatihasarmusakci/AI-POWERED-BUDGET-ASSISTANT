import { getDemoHotelsForCity } from '../data/demo-hotels'
import type { VibecheckService } from './vibecheck-service'

export const vibecheckMockService: VibecheckService = {
  getBundle: async (city: string) => ({
    dataSource: 'demo',
    personas: ['Sakin Tatilci', 'Sosyal Kaşif', 'Verim Odaklı'],
    hotels: getDemoHotelsForCity(city),
    mapLayers: [],
    insight: {
      city,
      message: `${city} için demo otel profilleri yüklendi. Sunumda akışı güvenle gösterebilirsin.`,
    },
    staycation: {
      coworking: 8.2,
      brunch: 8.8,
      wifiReliability: 8.4,
    },
  }),
}
