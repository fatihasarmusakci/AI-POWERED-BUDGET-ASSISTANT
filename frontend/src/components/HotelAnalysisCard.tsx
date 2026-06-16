import { useEffect, useMemo, useRef, useState } from 'react'
import type { HotelAnalysisResponse } from '../types/hotelAnalysis'
import { hotelAnalysisService } from '../services/hotelAnalysisService'
import './HotelAnalysisCard.css'

interface HotelAnalysisCardProps {
  reviews: string[]
  analysisKey?: string
  preferences?: {
    travel_style?: string
    priority?: string
    non_negotiable?: string
    persona?: string
  }
}

export default function HotelAnalysisCard({ reviews, analysisKey, preferences }: HotelAnalysisCardProps) {
  const [analysis, setAnalysis] = useState<HotelAnalysisResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [manualRefreshCount, setManualRefreshCount] = useState(0)
  const latestSignatureRef = useRef('')
  const signature = useMemo(
    () => JSON.stringify({ analysisKey: analysisKey ?? '', reviews, preferences }),
    [analysisKey, preferences, reviews],
  )
  latestSignatureRef.current = signature

  const runAnalysis = async (requestSignature: string) => {
    if (reviews.length === 0) {
      setAnalysis(null)
      setError('Analiz için en az bir yorum gerekli')
      setLoading(false)
      return
    }
    setLoading(true)
    setError(null)

    try {
      const result = await hotelAnalysisService.analyzeReviews({
        reviews,
        preferences: {
          ...preferences,
          analysis_key: analysisKey,
        },
      })
      // Bu sırada otel/il tekrar değiştiyse eski sonucu ekrana basma.
      if (requestSignature !== latestSignatureRef.current) return
      setAnalysis(result)
    } catch (err) {
      if (requestSignature !== latestSignatureRef.current) return
      setError('Analiz sırasında bir hata oluştu. Lütfen tekrar deneyin.')
      console.error(err)
    } finally {
      if (requestSignature === latestSignatureRef.current) setLoading(false)
    }
  }

  useEffect(() => {
    setAnalysis(null)
    setError(null)
    setLoading(true)

    const timer = window.setTimeout(() => {
      void runAnalysis(signature)
    }, 300)

    return () => {
      window.clearTimeout(timer)
    }
  }, [signature, manualRefreshCount])

  const hasReviews = reviews.length > 0
  const displayError = error ?? (!hasReviews ? 'Analiz için en az bir yorum gerekli' : null)

  const getScoreLabel = (score: number) => {
    if (score >= 5) return 'Mükemmel'
    if (score >= 4) return 'Çok İyi'
    if (score >= 3) return 'İyi'
    if (score >= 2) return 'Orta'
    return 'Kötü'
  }

  const getStarRating = (score: number) => {
    const stars = []
    for (let i = 1; i <= 5; i++) {
      if (i <= score) {
        stars.push('⭐')
      } else if (i - 0.5 <= score) {
        stars.push('✨')
      } else {
        stars.push('☆')
      }
    }
    return stars.join('')
  }

  return (
    <div className="hotel-analysis-card">
      <div className="card-header">
        <h3>Yapay Zeka Analizi</h3>
        <button
          onClick={() => setManualRefreshCount((prev) => prev + 1)}
          disabled={loading}
          className="analyze-button"
        >
          {loading ? 'Analiz ediliyor...' : analysis ? 'Yenile' : 'Analiz Et'}
        </button>
      </div>

      {displayError && (
        <div className="error-message">
          <p>⚠️ {displayError}</p>
        </div>
      )}

      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
        </div>
      )}

      {analysis && !loading && (
        <div className="analysis-results">
          <div className="scores-grid">
            {[
              {
                label: '🧹 Temizlik',
                value: analysis.cleaning_score ?? 3,
                cardClass: 'score-card-green',
                barClass: 'progress-fill-green',
              },
              {
                label: '🤫 Sessizlik',
                value: analysis.quietness_score ?? 3,
                cardClass: 'score-card-purple',
                barClass: 'progress-fill-purple',
              },
              {
                label: '🧑‍🍳 Hizmet',
                value: analysis.service_score ?? 3,
                cardClass: 'score-card-blue',
                barClass: 'progress-fill-blue',
              },
              {
                label: '🗺️ Konum',
                value: analysis.location_score ?? 3,
                cardClass: 'score-card-teal',
                barClass: 'progress-fill-teal',
              },
              {
                label: '📶 Wi-Fi',
                value: analysis.wifi_score ?? 3,
                cardClass: 'score-card-yellow',
                barClass: 'progress-fill-yellow',
              },
              {
                label: '🍳 Kahvaltı',
                value: analysis.breakfast_score ?? 3,
                cardClass: 'score-card-pink',
                barClass: 'progress-fill-pink',
              },
              {
                label: '👨‍👩‍👧 Aile',
                value: analysis.family_friendly_score ?? 3,
                cardClass: 'score-card-orange',
                barClass: 'progress-fill-orange',
              },
              {
                label: '🏊 Eğlence',
                value: analysis.entertainment_score ?? 3,
                cardClass: 'score-card-indigo',
                barClass: 'progress-fill-indigo',
              },
              {
                label: '🛏️ Konfor',
                value: analysis.room_comfort_score ?? 3,
                cardClass: 'score-card-sand',
                barClass: 'progress-fill-sand',
              },
              {
                label: '💸 Fiyat/Değer',
                value: analysis.value_for_money_score ?? 3,
                cardClass: 'score-card-lilac',
                barClass: 'progress-fill-lilac',
              },
            ].map((card) => (
              <div key={card.label} className={`score-card ${card.cardClass}`}>
                <div className="score-header">
                  <span className="score-label">{card.label}</span>
                  <span className="score-value">{card.value}/5</span>
                </div>
                <div className="progress-bar">
                  <div
                    className={`progress-fill ${card.barClass}`}
                    style={{ width: `${(card.value / 5) * 100}%` }}
                  ></div>
                </div>
                <p className="score-text">{getScoreLabel(card.value)}</p>
                <p className="score-text" style={{ fontSize: '0.7rem', marginTop: '0.25rem' }}>
                  {getStarRating(card.value)}
                </p>

                {card.label === '👨‍👩‍👧 Aile' ? (
                  <div
                    className={`playground-indicator ${analysis.has_playground ?? false ? 'has-playground' : 'no-playground'}`}
                  >
                    <span className="icon">{analysis.has_playground ?? false ? '✅' : '❌'}</span>
                    <span>
                      {analysis.has_playground ?? false ? 'Oyun Alanı Var' : 'Oyun Alanı Bilgisi Bulunamadı'}
                    </span>
                  </div>
                ) : null}
              </div>
            ))}
          </div>

          <div className="pros-cons-grid">
            <div className="pros-cons-card pros-card">
              <h4>
                <span className="bullet">💚</span> Olumlu Özellikler
              </h4>
              <ul className="feature-list">
                {analysis.pros.map((pro, index) => (
                  <li key={index}>
                    <span className="bullet">✓</span>
                    <span>{pro}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="pros-cons-card cons-card">
              <h4>
                <span className="bullet">💔</span> Olumsuz Özellikler
              </h4>
              <ul className="feature-list">
                {analysis.cons.map((con, index) => (
                  <li key={index}>
                    <span className="bullet">!</span>
                    <span>{con}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {!analysis && !loading && !displayError && (
        <div className="empty-state">
          <span className="empty-icon">🔍</span>
          <p className="empty-text">Otel yorumları analiz ediliyor...</p>
          <p className="empty-subtext">Soru cevaplarını değiştirdiğinde skorlar otomatik güncellenir</p>
        </div>
      )}
    </div>
  )
}
