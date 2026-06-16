import { vibecheckLiveService } from './vibecheck-live-service'
import { vibecheckMockService } from './vibecheck-mock-service'
import type { VibecheckService } from './vibecheck-service'

const withTimeout = async <T>(promise: Promise<T>, ms: number): Promise<T> => {
  return await Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error('Canlı veri zaman aşımına uğradı.')), ms),
    ),
  ])
}

/** Sunum için güvenilir demo verisi — varsayılan akış. */
export const vibecheckService: VibecheckService = vibecheckMockService

/** Kullanıcı istediğinde tek seferlik canlı arama (hafif mod, kredi dostu). */
export async function fetchLiveBundle(city: string) {
  return await withTimeout(vibecheckLiveService.getBundle(city), 8000)
}
