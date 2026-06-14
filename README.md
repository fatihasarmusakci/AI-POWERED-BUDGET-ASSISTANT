# Velo — AI-Powered Hotel Review Analyzer

Velo (VibeCheck), otel yorumlarını yapay zeka ile 6 kritere göre puanlayıp özetleyen web uygulamasıdır. Seyahat eden kullanıcılar yüzlerce yorum arasında kaybolmak yerine, kendi önceliklerine göre hızlı karar verebilir.

## Canlı Demo

| Servis | URL |
|--------|-----|
| Frontend | `https://YOUR-VERCEL-APP.vercel.app` *(deploy sonrası güncelleyin)* |
| Backend API | `https://YOUR-RENDER-SERVICE.onrender.com` *(deploy sonrası güncelleyin)* |
| API Docs | `https://YOUR-RENDER-SERVICE.onrender.com/docs` |

## Özellikler

- **Velo AI Analiz:** Otel yorumlarını Gemini ile 6 kritere göre puanlama (temizlik, aile dostu, yemek, konum, hizmet, fiyat/performans)
- **VibeCheck Prototype:** Persona onboarding, Truth Dashboard, Smart Score, Vibe-Map
- **OpenAI NLP:** Tekil yorum analizi, TL;DR özet ve sentiment skorları
- **REST API:** Frontend'den bağımsız, mobil/web istemcilerine hizmet verebilir yapı

## Klasör Yapısı

```
/frontend   → React + Vite arayüz
/backend    → FastAPI + SQLAlchemy API
/prodocs    → AI ajanları için geliştirme referansları
PRD.md      → Ürün gereksinimleri
tech-stack.md, Plan.md, DesignSystem.md, Progress.md
```

## Yerel Kurulum

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # GEMINI_API_KEY ve OPENAI_API_KEY ekleyin
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Tarayıcı: `http://localhost:5173` — API: `http://localhost:8000`

## Deploy

### Backend (Render)

1. [render.com](https://render.com) → New Blueprint → repo'yu bağla
2. `render.yaml` otomatik algılanır
3. Environment Variables: `GEMINI_API_KEY`, isteğe bağlı `OPENAI_API_KEY`
4. Deploy tamamlanınca URL'yi kopyala (ör. `https://velo-api.onrender.com`)

### Frontend (Vercel)

1. [vercel.com](https://vercel.com) → Import Git Repository
2. Root Directory: `frontend`
3. Environment Variable: `VITE_API_BASE_URL=https://velo-api.onrender.com`
4. Deploy

## Ortam Değişkenleri

Kök `.env.example` dosyasına bakın. **Gerçek API anahtarlarını asla commit etmeyin.**

## Demo Video

5 dakikalık demo videosu Loom/YouTube'da paylaşılmalıdır. İçerik: problem, çözüm, mimari, canlı demo, tech stack, rekabet farkı, gelecek planları.

## Lisans

Eğitim projesi — 2026
