# Tech Stack — Velo / VibeCheck

## Genel Mimari

```
[React Frontend]  ←HTTP/JSON→  [FastAPI Backend]  ←API→  [Gemini / OpenAI]
                                      ↓
                              [SQLite / PostgreSQL]
                                      ↓
                              [Celery + Redis] (opsiyonel)
```

Frontend ve backend tamamen ayrık; backend ileride mobil istemcilere de hizmet verebilir.

## Frontend

| Teknoloji | Gerekçe |
|-----------|---------|
| **React 19** | Bileşen tabanlı UI, geniş ekosistem |
| **TypeScript** | Tip güvenliği, API sözleşmesi uyumu |
| **Vite** | Hızlı dev server ve production build |
| **CSS (custom)** | Hafif, design token tabanlı; framework bağımlılığı yok |

Deploy: **Vercel** (statik SPA, `VITE_API_BASE_URL` env)

## Backend

| Teknoloji | Gerekçe |
|-----------|---------|
| **FastAPI** | Async REST, otomatik OpenAPI docs, hızlı geliştirme |
| **SQLAlchemy 2** | Async ORM; SQLite (dev) / PostgreSQL (prod) |
| **Pydantic v2** | Request/response validasyonu |
| **Celery + Redis** | Yorum NLP analizi arka plan kuyruğu |
| **pytest** | API entegrasyon testleri |

Deploy: **Render** (`render.yaml` Blueprint)

## Yapay Zeka Servisleri

| Servis | Kullanım | Model |
|--------|----------|-------|
| **Google Gemini** | Otel yorum analizi — 6 kriter skor + özet | `gemini-1.5-flash` |
| **OpenAI** | Tekil yorum NLP, TL;DR özet, sentiment | `gpt-4o-mini` |

API anahtarı yoksa heuristic fallback devreye girer (geliştirme/test).

### AI Entegrasyon Noktaları

1. `POST /api/hotels/analyze` → `HotelAnalysisService` (Gemini)
2. `POST /reviews` → Celery → `NLPService` (OpenAI)
3. `GET /hotels/{id}/summary` → `SummarizationService` (OpenAI)

## Geliştirme Sürecinde AI Kullanımı

| Araç | Nasıl Kullanıldı |
|------|------------------|
| **Cursor IDE** | Kod üretimi, refactoring, dokümantasyon |
| **Claude / GPT** | Mimari kararlar, prompt tasarımı, hata ayıklama |
| **Gemini API** | Ürün çekirdeği — canlı yorum analizi |

### AI Destekli Geliştirici Kararları

- FastAPI + React ayrımı: ödev gereksinimi + ölçeklenebilirlik
- Gemini otel analizi, OpenAI NLP: maliyet/hız dengesi; flash model yeterli
- Mock → Live geçiş: `VITE_DATA_SOURCE` ve API key ile kontrollü mod
- Heuristic fallback: API limiti veya key eksikliğinde uygulama çökmez

## Veritabanı ve Ortam

- **Dev:** SQLite (`vibecheck.db`)
- **Prod:** PostgreSQL (Render add-on) veya SQLite (demo)
- **Env:** `.env` dosyaları gitignore'da; `.env.example` şablon

## CI / Kalite

- `pytest` — backend API testleri
- `npm run build` + `eslint` — frontend
- Manuel usability test (2 tur) — `frontend/docs/usability-test-report.md`
