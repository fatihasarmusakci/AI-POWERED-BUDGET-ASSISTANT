# Plan — Velo / VibeCheck

PRD'den türetilmiş kullanıcı hikayeleri ve teknik adımlar.

## Faz 1 — Temel Altyapı

| # | Kullanıcı Hikayesi | Teknik Adım | Durum |
|---|-------------------|-------------|-------|
| 1.1 | Geliştirici projeyi klonlayıp çalıştırabilmeli | FastAPI skeleton, React+Vite, `.env.example` | ✅ |
| 1.2 | API sağlık kontrolü yapılabilmeli | `GET /health` | ✅ |
| 1.3 | Oteller listelenebilmeli | `GET /hotels`, seed script | ✅ |

## Faz 2 — AI Çekirdek (Velo)

| # | Kullanıcı Hikayesi | Teknik Adım | Durum |
|---|-------------------|-------------|-------|
| 2.1 | Kullanıcı yorum yapıştırıp analiz alabilmeli | `POST /api/hotels/analyze`, Gemini entegrasyonu | ✅ |
| 2.2 | 6 kriterde skor görmeli | `HotelAnalysisResponse` schema, frontend kart | ✅ |
| 2.3 | “Çocuğum var” filtresi ile aile skoruna odaklanabilmeli | Persona filter UI | ✅ |
| 2.4 | API key yoksa uygulama çalışmaya devam etmeli | Heuristic fallback | ✅ |

## Faz 3 — VibeCheck Prototype

| # | Kullanıcı Hikayesi | Teknik Adım | Durum |
|---|-------------------|-------------|-------|
| 3.1 | 3 adımlı onboarding ile persona seçebilmeli | Persona Engine UI | ✅ |
| 3.2 | Resmi vs kullanıcı foto karşılaştırması görmeli | Truth Dashboard | ✅ |
| 3.3 | Smart Score ve TL;DR görmeli | Mock + OpenAI summary API | ✅ |
| 3.4 | Vibe-Map katmanlarını açıp kapatabilmeli | Layer toggle UI | ✅ |
| 3.5 | Günlük oyun ve insight ile geri dönebilmeli | Retention surface | ✅ |

## Faz 4 — Backend NLP Pipeline

| # | Kullanıcı Hikayesi | Teknik Adım | Durum |
|---|-------------------|-------------|-------|
| 4.1 | Yeni yorum gönderildiğinde NLP analizi yapılmalı | `POST /reviews`, Celery task | ✅ |
| 4.2 | Otel özeti 3 maddelik TL;DR olmalı | `SummarizationService` (OpenAI) | ✅ |
| 4.3 | Görsel dürüstlük skoru hesaplanmalı | `honesty_service` | ✅ |

## Faz 5 — Entegrasyon ve Deploy

| # | Kullanıcı Hikayesi | Teknik Adım | Durum |
|---|-------------------|-------------|-------|
| 5.1 | Frontend canlı backend'e bağlanabilmeli | `VITE_API_BASE_URL`, CORS | ✅ |
| 5.2 | Uygulama internette erişilebilir olmalı | Render + Vercel deploy | ⏳ Kullanıcı deploy edecek |
| 5.3 | Teslim dokümanları tam olmalı | PRD, README, Progress, prodocs | ✅ |

## Faz 6 — Demo ve Teslim

| # | Adım | Durum |
|---|------|-------|
| 6.1 | Canlı URL test | ⏳ |
| 6.2 | 5 dk demo video (Loom/YouTube) | ⏳ |
| 6.3 | Teslim formu | ⏳ |

## Sprint Notları

- **Hafta 1–2:** FastAPI + React iskelet, mock veri
- **Hafta 3–4:** VibeCheck prototype UI, design system
- **Hafta 5–6:** OpenAI NLP, Celery, seed data
- **Hafta 7:** Gemini otel analizi, frontend entegrasyon
- **Hafta 8:** Deploy, dokümantasyon, demo video
