import { useEffect, useMemo, useState } from 'react'

import { getDemoHotelsForCity } from './data/demo-hotels'
import type { VibecheckDataBundle } from './features/vibecheck/types'
import { fetchLiveBundle } from './services/vibecheck-provider'
import HotelAnalysisCard from './components/HotelAnalysisCard'

const keywordGroups = {
  quiet: ['sakin', 'sessiz', 'huzur', 'uyku', 'dinlen', 'gürültü olmasın'],
  social: ['sosyal', 'eğlence', 'gece', 'canlı', 'aktivite'],
  family: ['aile', 'çocuk', 'bebek', 'family'],
  clean: ['temiz', 'hijyen', 'temizlik'],
  wifi: ['wifi', 'internet', 'çalışma', 'uzaktan', 'laptop'],
  breakfast: ['kahvaltı', 'yemek', 'restoran'],
  location: ['merkez', 'konum', 'ulaşım', 'metro', 'yakın'],
} as const

function normalizeText(value: string): string {
  return value
    .toLocaleLowerCase('tr-TR')
    .replaceAll('ı', 'i')
    .replaceAll('ş', 's')
    .replaceAll('ç', 'c')
    .replaceAll('ğ', 'g')
    .replaceAll('ö', 'o')
    .replaceAll('ü', 'u')
}

function canonicalizeCityName(raw: string, options: string[]): string {
  const trimmed = raw.trim()
  if (!trimmed) {
    return ''
  }
  const normalized = normalizeText(trimmed)
  const direct = options.find((city) => normalizeText(city) === normalized)
  return direct ?? trimmed
}

function calculateHotelFitScore(hotel: VibecheckDataBundle['hotels'][number], criteriaText: string): number {
  const normalizedCriteria = normalizeText(criteriaText.trim())
  if (!normalizedCriteria) {
    return hotel.smartScore
  }

  const searchableBlob = normalizeText([
    hotel.name,
    hotel.district,
    hotel.summary,
    ...(hotel.highlights ?? []),
    ...(hotel.amenities ?? []),
    ...(hotel.reviews ?? []),
  ].join(' '))

  let score = hotel.smartScore

  for (const term of normalizedCriteria.split(/\s+/).filter(Boolean)) {
    if (searchableBlob.includes(term)) {
      score += 1.3
    }
  }

  const applyWeightedBoost = (terms: readonly string[], fieldValue: number) => {
    if (terms.some((term) => normalizedCriteria.includes(normalizeText(term)))) {
      score += fieldValue * 0.35
    }
  }

  applyWeightedBoost(keywordGroups.quiet, hotel.sleepScore)
  applyWeightedBoost(keywordGroups.social, hotel.socialScore)
  applyWeightedBoost(keywordGroups.wifi, hotel.wifiScore)

  if (keywordGroups.family.some((term) => normalizedCriteria.includes(normalizeText(term)))) {
    score += (hotel.highlights ?? []).some((item) => normalizeText(item).includes('aile') || normalizeText(item).includes('cocuk')) ? 2.5 : 0
  }
  if (keywordGroups.clean.some((term) => normalizedCriteria.includes(normalizeText(term)))) {
    score += (hotel.reviews ?? []).some((item) => normalizeText(item).includes('temiz')) ? 2.2 : 0
  }
  if (keywordGroups.breakfast.some((term) => normalizedCriteria.includes(normalizeText(term)))) {
    score += (hotel.amenities ?? []).some((item) => normalizeText(item).includes('kahvalti')) ? 1.6 : 0
  }
  if (keywordGroups.location.some((term) => normalizedCriteria.includes(normalizeText(term)))) {
    score += (hotel.highlights ?? []).some((item) => normalizeText(item).includes('merkezi') || normalizeText(item).includes('yakin')) ? 1.8 : 0
  }

  return Number(score.toFixed(2))
}

function createDemoBundle(city: string): VibecheckDataBundle {
  return {
    dataSource: 'demo',
    personas: ['Sakin Tatilci', 'Sosyal Kaşif', 'Verim Odaklı'],
    hotels: getDemoHotelsForCity(city),
    mapLayers: [],
    insight: {
      city,
      message: `${city} için demo otel profilleri hazır. Sunumda güvenle gösterebilirsin.`,
    },
    staycation: {
      coworking: 8.2,
      brunch: 8.8,
      wifiReliability: 8.4,
    },
  }
}

function App() {
  const cityOptions = [
    'Adana', 'Adıyaman', 'Afyonkarahisar', 'Ağrı', 'Aksaray', 'Amasya', 'Ankara', 'Antalya', 'Ardahan',
    'Artvin', 'Aydın', 'Balıkesir', 'Bartın', 'Batman', 'Bayburt', 'Bilecik', 'Bingöl', 'Bitlis', 'Bolu',
    'Burdur', 'Bursa', 'Çanakkale', 'Çankırı', 'Çorum', 'Denizli', 'Diyarbakır', 'Düzce', 'Edirne',
    'Elazığ', 'Erzincan', 'Erzurum', 'Eskişehir', 'Gaziantep', 'Giresun', 'Gümüşhane', 'Hakkari', 'Hatay',
    'Iğdır', 'Isparta', 'İstanbul', 'İzmir', 'Kahramanmaraş', 'Karabük', 'Karaman', 'Kars', 'Kastamonu',
    'Kayseri', 'Kırıkkale', 'Kırklareli', 'Kırşehir', 'Kilis', 'Kocaeli', 'Konya', 'Kütahya', 'Malatya',
    'Manisa', 'Mardin', 'Mersin', 'Muğla', 'Muş', 'Nevşehir', 'Niğde', 'Ordu', 'Osmaniye', 'Rize', 'Sakarya',
    'Samsun', 'Şanlıurfa', 'Siirt', 'Sinop', 'Şırnak', 'Sivas', 'Tekirdağ', 'Tokat', 'Trabzon', 'Tunceli',
    'Uşak', 'Van', 'Yalova', 'Yozgat', 'Zonguldak',
  ]

  const [sessionStart] = useState(() => Date.now())
  const [selectedCity, setSelectedCity] = useState('')
  const [cityInput, setCityInput] = useState('')
  const [bundle, setBundle] = useState<VibecheckDataBundle | null>(null)
  const [errorMessage, setErrorMessage] = useState('')
  const [isLiveLoading, setIsLiveLoading] = useState(false)
  const [step, setStep] = useState(1)
  const [persona, setPersona] = useState<VibecheckDataBundle['personas'][number]>('Sakin Tatilci')
  const [travelStyle, setTravelStyle] = useState('Aile ile sakin bir tatil planlıyoruz.')
  const [priority, setPriority] = useState('Uyku kalitesi ve sessizlik önceliğim.')
  const [nonNegotiable, setNonNegotiable] = useState('Temizlik benim için vazgeçilmez.')
  const [activeHotelId, setActiveHotelId] = useState('')
  const [timeToActionSeconds, setTimeToActionSeconds] = useState<number | null>(null)

  useEffect(() => {
    if (!selectedCity) {
      setBundle(null)
      setActiveHotelId('')
      return
    }

    const nextBundle = createDemoBundle(selectedCity)
    setBundle(nextBundle)
    setPersona(nextBundle.personas[0])
    setActiveHotelId(nextBundle.hotels[0]?.id ?? '')
    setErrorMessage('')

    let cancelled = false
    const loadLive = async () => {
      setIsLiveLoading(true)
      try {
        const liveBundle = await fetchLiveBundle(selectedCity)
        if (cancelled) {
          return
        }
        setBundle(liveBundle)
        setPersona(liveBundle.personas[0])
        setActiveHotelId(liveBundle.hotels[0]?.id ?? '')
      } catch (error) {
        if (cancelled) {
          return
        }
        const message = error instanceof Error ? error.message : 'Canlı veri alınamadı.'
        setErrorMessage(`${message} Bu şehirde demo veriler gösteriliyor.`)
      } finally {
        if (!cancelled) {
          setIsLiveLoading(false)
        }
      }
    }

    void loadLive()
    return () => {
      cancelled = true
    }
  }, [selectedCity])

  const hotelsWithBooking = useMemo(() => {
    if (!bundle) {
      return []
    }
    return bundle.hotels.map((hotel) => {
      if (hotel.bookingUrl) {
        return hotel
      }
      const query = encodeURIComponent(`${hotel.name} ${hotel.district} otel`)
      return {
        ...hotel,
        bookingUrl: `https://www.google.com/maps/search/?api=1&query=${query}`,
      }
    })
  }, [bundle])

  const rankingCriteria = useMemo(
    () => `${travelStyle} ${priority} ${nonNegotiable}`,
    [travelStyle, priority, nonNegotiable],
  )

  const rankedHotels = useMemo(() => {
    return hotelsWithBooking
      .map((hotel) => ({
        hotel,
        fitScore: calculateHotelFitScore(hotel, rankingCriteria),
      }))
      .sort((a, b) => b.fitScore - a.fitScore)
  }, [hotelsWithBooking, rankingCriteria])

  useEffect(() => {
    if (rankedHotels.length === 0) {
      return
    }
    const currentStillVisible = rankedHotels.some((item) => item.hotel.id === activeHotelId)
    if (!currentStillVisible) {
      setActiveHotelId(rankedHotels[0].hotel.id)
    }
  }, [activeHotelId, rankedHotels])

  const activeRankedHotel = useMemo(() => {
    if (rankedHotels.length === 0) {
      return null
    }
    return rankedHotels.find((item) => item.hotel.id === activeHotelId) ?? rankedHotels[0]
  }, [activeHotelId, rankedHotels])

  const activeHotelWithBooking = activeRankedHotel?.hotel ?? null
  const bookingUrl = activeHotelWithBooking?.bookingUrl ?? ''
  const analysisReviews = useMemo(() => {
    if (!activeHotelWithBooking) {
      return []
    }
    return [
      `Otel: ${activeHotelWithBooking.name}. Bölge: ${activeHotelWithBooking.district}.`,
      `Öne çıkanlar: ${(activeHotelWithBooking.highlights ?? []).join(', ') || 'Belirtilmemiş'}.`,
      ...(activeHotelWithBooking.reviews ?? []),
    ]
  }, [activeHotelWithBooking])

  const handleBookingClick = () => {
    if (!bookingUrl) {
      return
    }
    const seconds = Math.round((Date.now() - sessionStart) / 1000)
    setTimeToActionSeconds(seconds)
    window.open(bookingUrl, '_blank', 'noopener,noreferrer')
  }

  const handleCitySearch = () => {
    const normalized = canonicalizeCityName(cityInput, cityOptions)
    if (!normalized) {
      setErrorMessage('Lütfen önce bir il seç.')
      return
    }
    setErrorMessage('')
    setCityInput(normalized)
    setSelectedCity(normalized)
  }

  const handleTryLive = async () => {
    if (!selectedCity) {
      setErrorMessage('Canlı veri için önce bir il seç.')
      return
    }
    setIsLiveLoading(true)
    setErrorMessage('')
    try {
      const liveBundle = await fetchLiveBundle(selectedCity)
      setBundle(liveBundle)
      setPersona(liveBundle.personas[0])
      setActiveHotelId(liveBundle.hotels[0]?.id ?? '')
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Canlı veri alınamadı.'
      setErrorMessage(`${message} Demo verilerle devam ediliyor.`)
    } finally {
      setIsLiveLoading(false)
    }
  }

  const handleBackToDemo = () => {
    if (!selectedCity) {
      return
    }
    const demoBundle = createDemoBundle(selectedCity)
    setBundle(demoBundle)
    setPersona(demoBundle.personas[0])
    setActiveHotelId(demoBundle.hotels[0]?.id ?? '')
    setErrorMessage('')
  }

  if (!selectedCity) {
    return (
      <main className="app-shell">
        <header className="hero-card">
          <div className="hero-top-row">
            <p className="eyebrow">VibeCheck Travel — Türkiye</p>
            <span className="data-badge">Demo Verisi</span>
          </div>
          <h1>Ailene en uygun oteli güvenle seç</h1>
          <p className="subtitle">Başlamak için şehir seç ve kriterlerini yaz.</p>
          <div className="grid" style={{ marginTop: '0.8rem' }}>
            <label htmlFor="city-input" className="muted">İl seç</label>
            <div className="step-row">
              <input
                id="city-input"
                list="turkiye-illeri"
                className="text-input"
                value={cityInput}
                onChange={(event) => setCityInput(event.target.value)}
                placeholder="Seçiniz"
              />
              <datalist id="turkiye-illeri">
                {cityOptions.map((city) => (
                  <option key={city} value={city} />
                ))}
              </datalist>
              <button type="button" className="chip chip-active" onClick={handleCitySearch}>
                Otelleri Getir
              </button>
            </div>
          </div>
        </header>
        {errorMessage ? (
          <section className="panel panel-warning">
            <p>{errorMessage}</p>
          </section>
        ) : null}
      </main>
    )
  }

  if (!activeHotelWithBooking || !bundle) {
    return (
      <main className="app-shell">
        <section className="panel">
          <h2>VibeCheck</h2>
          <p>Bu il için otel bulunamadı. Farklı bir il deneyebilirsin.</p>
        </section>
      </main>
    )
  }

  const dataSourceLabel = bundle.dataSource === 'live' ? 'Canlı Veri' : 'Demo Verisi'

  return (
    <main className="app-shell">
      <header className="hero-card">
        <div className="hero-top-row">
          <p className="eyebrow">VibeCheck Travel — Türkiye</p>
          <span className={`data-badge ${bundle.dataSource === 'live' ? 'data-badge-live' : ''}`}>
            {dataSourceLabel}
          </span>
        </div>
        <h1>Ailene en uygun oteli güvenle seç</h1>
        <p className="subtitle">
          Fotoğrafa değil, yorum analizi ve yaşam tarzı uyumuna odaklan. Rezervasyonu sen karar verince aç.
        </p>
        <div className="grid" style={{ marginTop: '0.8rem' }}>
          <label htmlFor="city-input" className="muted">İl seç veya yaz</label>
          <div className="step-row">
            <input
              id="city-input"
              list="turkiye-illeri"
              className="text-input"
              value={cityInput}
              onChange={(event) => setCityInput(event.target.value)}
              placeholder="Seçiniz"
            />
            <datalist id="turkiye-illeri">
              {cityOptions.map((city) => (
                <option key={city} value={city} />
              ))}
            </datalist>
            <button type="button" className="chip chip-active" onClick={handleCitySearch}>
              Otelleri Getir
            </button>
            <button
              type="button"
              className="chip"
              onClick={() => void handleTryLive()}
              disabled={isLiveLoading}
            >
              {isLiveLoading ? 'Canlı aranıyor...' : 'Canlı Veri Dene'}
            </button>
            {bundle.dataSource === 'live' ? (
              <button type="button" className="chip" onClick={handleBackToDemo}>
                Demo Moduna Dön
              </button>
            ) : null}
          </div>
        </div>
      </header>

      {errorMessage ? (
        <section className="panel panel-warning">
          <p>{errorMessage}</p>
        </section>
      ) : null}

      <section className="panel">
        <h2>1) Tercihlerini Yaz (3 adım)</h2>
        <div className="step-row" role="tablist" aria-label="Onboarding adımları">
          {[1, 2, 3].map((item) => (
            <button
              key={item}
              type="button"
              className={`chip ${step === item ? 'chip-active' : ''}`}
              onClick={() => setStep(item)}
            >
              Adım {item}
            </button>
          ))}
        </div>
        <div className="grid two-col">
          <article className="card">
            <p className="muted">Adım {step} sorusu</p>
            <p>
              {step === 1 && 'Tatilde önceliğin nedir: sakinlik mi sosyal ortam mı?'}
              {step === 2 && 'En önemli kriterin hangisi: uyku kalitesi, eğlence veya verimlilik?'}
              {step === 3 && 'Rezervasyon yaparken vazgeçilmezin nedir?'}
            </p>
            <div className="grid" style={{ marginTop: '0.7rem' }}>
              {step === 1 && (
                <textarea
                  className="question-input"
                  value={travelStyle}
                  onChange={(event) => setTravelStyle(event.target.value)}
                  placeholder="Tatilde nasıl bir deneyim istediğini yaz..."
                />
              )}
              {step === 2 && (
                <textarea
                  className="question-input"
                  value={priority}
                  onChange={(event) => setPriority(event.target.value)}
                  placeholder="Önceliğini detaylı yaz..."
                />
              )}
              {step === 3 && (
                <textarea
                  className="question-input"
                  value={nonNegotiable}
                  onChange={(event) => setNonNegotiable(event.target.value)}
                  placeholder="Vazgeçilmez kriterini yaz..."
                />
              )}
            </div>
          </article>
          <article className="card">
            <p className="muted">Persona sonucu</p>
            <div className="step-row">
              {bundle.personas.map((item) => (
                <button
                  key={item}
                  type="button"
                  className={`chip ${persona === item ? 'chip-active' : ''}`}
                  onClick={() => setPersona(item)}
                >
                  {item}
                </button>
              ))}
            </div>
            <p className="status">
              Aktif persona: <strong>{persona}</strong>
            </p>
            <p className="muted">
              Seçimler: {travelStyle} | {priority} | {nonNegotiable}
            </p>
          </article>
        </div>
      </section>

      <section className="panel">
        <h2>2) Otel Karşılaştırması</h2>
        <p className="muted">Otel listesi kriterlerine göre otomatik sıralanır (en uygun en üstte).</p>

        <div className="hotel-switch" role="tablist" aria-label="Otel seçenekleri">
          {rankedHotels.map(({ hotel, fitScore }) => (
            <button
              key={hotel.id}
              type="button"
              className={`hotel-tab ${activeHotelId === hotel.id ? 'hotel-tab-active' : ''}`}
              onClick={() => setActiveHotelId(hotel.id)}
            >
              {hotel.name} ({fitScore.toFixed(1)})
            </button>
          ))}
        </div>

        <article className="card">
          <h3>Otel Bilgi Paneli</h3>
          <p className="muted">
            Fotoğraf API kredisi harcamadan otel profilini gösteriyoruz. Kararını verince rezervasyona geçebilirsin.
          </p>
          <div className="info-compare" aria-label="Resmi bilgi ve kullanıcı yorum özeti">
            <div className="info-box">
              <p className="info-box-title">{activeHotelWithBooking.officialPhotoLabel}</p>
              <p className="info-hotel-name">{activeHotelWithBooking.name}</p>
              <p className="muted">{activeHotelWithBooking.district}</p>
              <ul className="info-list">
                {(activeHotelWithBooking.highlights ?? []).map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
              <p className="photo-date">Güncelleme: {activeHotelWithBooking.officialDate}</p>
            </div>
            <div className="info-box">
              <p className="info-box-title">{activeHotelWithBooking.userPhotoLabel}</p>
              <ul className="info-list review-list">
                {(activeHotelWithBooking.reviews ?? []).slice(0, 4).map((review) => (
                  <li key={review}>{review}</li>
                ))}
              </ul>
              {(activeHotelWithBooking.amenities ?? []).length > 0 ? (
                <div className="amenity-row">
                  {activeHotelWithBooking.amenities!.map((item) => (
                    <span key={item} className="badge">{item}</span>
                  ))}
                </div>
              ) : null}
              <p className="photo-date">Son yorumlar: {activeHotelWithBooking.userDate}</p>
            </div>
          </div>
        </article>

        <HotelAnalysisCard
          key={activeHotelWithBooking.id}
          analysisKey={`${selectedCity}-${activeHotelWithBooking.id}`}
          reviews={analysisReviews}
          preferences={{
            travel_style: travelStyle,
            priority,
            non_negotiable: nonNegotiable,
            persona,
          }}
        />

        <article className="card booking-card">
          <h3>Rezervasyon (İsteğe Bağlı)</h3>
          <p className="muted">
            Bu otel kriterlerine uyuyorsa harita veya rezervasyon sitesinde devam edebilirsin.
            VibeCheck seni yönlendirir; ödeme burada yapılmaz.
          </p>
          <button type="button" className="cta-button" onClick={handleBookingClick}>
            Rezervasyona Git
          </button>
          {timeToActionSeconds !== null ? (
            <p className="status">Karar süresi: {timeToActionSeconds} saniye</p>
          ) : null}
        </article>
      </section>
    </main>
  )
}

export default App
