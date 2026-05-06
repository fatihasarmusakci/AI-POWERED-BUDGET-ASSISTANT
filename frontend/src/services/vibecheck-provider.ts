import { vibecheckLiveService } from './vibecheck-live-service'
import { vibecheckMockService } from './vibecheck-mock-service'
import type { VibecheckService } from './vibecheck-service'

const source = import.meta.env.VITE_DATA_SOURCE ?? 'mock'

export const vibecheckService: VibecheckService =
  source === 'live' ? vibecheckLiveService : vibecheckMockService
