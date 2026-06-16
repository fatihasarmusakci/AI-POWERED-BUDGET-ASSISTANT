import type { VibecheckDataBundle } from '../features/vibecheck/types'

export interface VibecheckService {
  getBundle: (city: string) => Promise<VibecheckDataBundle>
}
