import type { HotelCard } from '../features/vibecheck/types'

type DemoHotel = HotelCard & {
  highlights: string[]
  amenities: string[]
}

const mapsUrl = (name: string, city: string) =>
  `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${name} ${city} otel`)}`

const cityCatalog: Record<string, DemoHotel[]> = {
  İstanbul: [
    {
      id: 'istanbul-bosphorus-family',
      name: 'Bosphorus Family Suites',
      district: 'Beşiktaş, İstanbul',
      officialPhotoLabel: 'Resmi bilgi',
      userPhotoLabel: 'Kullanıcı yorum özeti',
      officialDate: '2026-06-01',
      userDate: '2026-06-10',
      smartScore: 8.7,
      wifiScore: 8,
      sleepScore: 8,
      socialScore: 7,
      bookingUrl: mapsUrl('Bosphorus Family Suites', 'İstanbul'),
      highlights: ['Aile odaları geniş', 'Metro yakın', 'Kahvaltı çeşitli'],
      amenities: ['Çocuk oyun alanı', 'Havuz', 'Ücretsiz Wi-Fi', 'Kahvaltı dahil'],
      reviews: [
        'Oda ve banyo çok temizdi, çocuklar için güvenli hissettik.',
        'Gece genelde sessizdi, sadece caddeden hafif ses geldi.',
        'Kahvaltı çeşitliydi, personel ilgiliydi.',
        'Çocuk oyun alanı küçük ama yeterliydi.',
      ],
      flags: ['Yoğun sezonda fiyat artışı'],
      summary: 'Aile tatili için dengeli bir seçenek. Temizlik ve konfor güçlü, fiyat sezona göre değişebilir.',
    },
    {
      id: 'istanbul-kadikoy-quiet',
      name: 'Kadıköy Quiet Stay',
      district: 'Kadıköy, İstanbul',
      officialPhotoLabel: 'Resmi bilgi',
      userPhotoLabel: 'Kullanıcı yorum özeti',
      officialDate: '2026-06-01',
      userDate: '2026-06-10',
      smartScore: 8.3,
      wifiScore: 9,
      sleepScore: 9,
      socialScore: 6,
      bookingUrl: mapsUrl('Kadıköy Quiet Stay', 'İstanbul'),
      highlights: ['Sessiz odalar', 'Hızlı Wi-Fi', 'Merkezi konum'],
      amenities: ['Sessiz oda seçeneği', 'Çalışma masası', 'Kahve makinesi'],
      reviews: [
        'Uyku kalitesi çok iyiydi, odalar sessizdi.',
        'Wi-Fi hızlı, uzaktan çalışma için uygun.',
        'Temizlik düzenli, personel yardımsever.',
      ],
      flags: ['Oda küçük olabilir'],
      summary: 'Sessizlik ve çalışma konforu arayanlar için güçlü bir seçenek.',
    },
  ],
  Antalya: [
    {
      id: 'antalya-lara-family',
      name: 'Lara Family Beach Hotel',
      district: 'Lara, Antalya',
      officialPhotoLabel: 'Resmi bilgi',
      userPhotoLabel: 'Kullanıcı yorum özeti',
      officialDate: '2026-06-01',
      userDate: '2026-06-10',
      smartScore: 8.9,
      wifiScore: 8,
      sleepScore: 8,
      socialScore: 8,
      bookingUrl: mapsUrl('Lara Family Beach Hotel', 'Antalya'),
      highlights: ['Denize yakın', 'Aile havuzu', 'Animasyon programı'],
      amenities: ['Çocuk havuzu', 'Mini club', 'All-inclusive', 'Plaj servisi'],
      reviews: [
        'Temizlik çok iyiydi, aile için ideal.',
        'Çocuklar mini clubu çok sevdi.',
        'Gece sakin, kahvaltı zengin.',
        'Wi-Fi ortak alanlarda iyiydi.',
      ],
      flags: ['Yoğun sezonda kalabalık'],
      summary: 'Aile tatili için güçlü profil. Temizlik ve çocuk aktiviteleri öne çıkıyor.',
    },
    {
      id: 'antalya-kaleici-boutique',
      name: 'Kaleiçi Boutique Hotel',
      district: 'Kaleiçi, Antalya',
      officialPhotoLabel: 'Resmi bilgi',
      userPhotoLabel: 'Kullanıcı yorum özeti',
      officialDate: '2026-06-01',
      userDate: '2026-06-10',
      smartScore: 8.2,
      wifiScore: 7,
      sleepScore: 7,
      socialScore: 9,
      bookingUrl: mapsUrl('Kaleiçi Boutique Hotel', 'Antalya'),
      highlights: ['Tarihi merkez', 'Butik deneyim', 'Yürüyüş mesafesi'],
      amenities: ['Teras', 'Kahvaltı', 'Rehber önerileri'],
      reviews: [
        'Konum harika, her yere yürüyerek gittik.',
        'Oda temiz ama biraz küçük.',
        'Sosyal ortam canlı, gece biraz sesli olabiliyor.',
      ],
      flags: ['Dar sokak nedeniyle araç parkı zor'],
      summary: 'Konum ve atmosfer güçlü. Sessizlikten çok deneyim arayanlar için uygun.',
    },
  ],
  İzmir: [
    {
      id: 'izmir-alsancak-sea',
      name: 'Alsancak Sea View Hotel',
      district: 'Alsancak, İzmir',
      officialPhotoLabel: 'Resmi bilgi',
      userPhotoLabel: 'Kullanıcı yorum özeti',
      officialDate: '2026-06-01',
      userDate: '2026-06-10',
      smartScore: 8.5,
      wifiScore: 8,
      sleepScore: 8,
      socialScore: 8,
      bookingUrl: mapsUrl('Alsancak Sea View Hotel', 'İzmir'),
      highlights: ['Deniz manzarası', 'Merkezi konum', 'Kahvaltı kalitesi'],
      amenities: ['Deniz manzaralı oda', 'Kahvaltı', 'Fitness'],
      reviews: [
        'Manzara güzel, odalar temiz.',
        'Kahvaltı lezzetli, personel güler yüzlü.',
        'Gece orta seviye sessiz.',
      ],
      flags: ['Otopark sınırlı'],
      summary: 'Şehir + deniz dengesi arayanlar için iyi bir profil.',
    },
  ],
}

export function getDemoHotelsForCity(city: string): DemoHotel[] {
  if (cityCatalog[city]) {
    return cityCatalog[city]
  }

  return [
    {
      id: `${city.toLowerCase()}-aile-otel`,
      name: `${city} Aile Otel`,
      district: `${city} Merkez`,
      officialPhotoLabel: 'Resmi bilgi',
      userPhotoLabel: 'Kullanıcı yorum özeti',
      officialDate: '2026-06-01',
      userDate: '2026-06-10',
      smartScore: 8.4,
      wifiScore: 8,
      sleepScore: 8,
      socialScore: 7,
      bookingUrl: mapsUrl(`${city} Aile Otel`, city),
      highlights: ['Aile dostu', 'Temiz odalar', 'Merkezi konum'],
      amenities: ['Çocuk alanı', 'Kahvaltı', 'Wi-Fi'],
      reviews: [
        'Temizlik iyi, aile için uygun.',
        'Personel yardımsever.',
        'Gece genelde sakin.',
      ],
      flags: ['Canlı veri yok, demo profil gösteriliyor'],
      summary: `${city} için demo otel profili. Canlı API kredisi olmadan sunum akışı test edilebilir.`,
    },
    {
      id: `${city.toLowerCase()}-sakin-otel`,
      name: `${city} Sakin Konak`,
      district: `${city}`,
      officialPhotoLabel: 'Resmi bilgi',
      userPhotoLabel: 'Kullanıcı yorum özeti',
      officialDate: '2026-06-01',
      userDate: '2026-06-10',
      smartScore: 8.1,
      wifiScore: 9,
      sleepScore: 9,
      socialScore: 6,
      bookingUrl: mapsUrl(`${city} Sakin Konak`, city),
      highlights: ['Sessiz odalar', 'Hızlı internet', 'Uyku kalitesi'],
      amenities: ['Sessiz kat', 'Çalışma masası', 'Kahvaltı'],
      reviews: [
        'Uyku kalitesi yüksek, odalar sessiz.',
        'Wi-Fi stabil ve hızlı.',
        'Temizlik düzenli.',
      ],
      flags: ['Sosyal aktivite sınırlı'],
      summary: 'Sessizlik ve konfor odaklı demo profil.',
    },
  ]
}
