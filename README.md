# VibeCheck Monorepo

VibeCheck, otel yorumlarını AI destekli analiz eden ve kullanıcı tercihleriyle eşleştirerek karar desteği veren bir web uygulamasıdır.

Bu repo **monorepo** yapısındadır:
- `frontend/` -> React + Vite (Vercel'e deploy edilir)
- `backend/` -> FastAPI (Render'a deploy edilir)
- `prodocs/` -> Jüri teslimi için zorunlu ürün dokümantasyonu (`PRD`, `tech-stack`, `Plan`, `DesignSystem`, `Progress`)

## Onepager Deployment Rehberi

### 1) Frontend Deployment (Vercel)
- Platform: [Vercel](https://vercel.com/)
- Import: GitHub repo
- **Root Directory: `frontend` (zorunlu)**
- Build Command: `npm run build`
- Output Directory: `dist`
- Environment Variables:
  - `VITE_API_BASE_URL=https://<render-backend-url>`
  - `VITE_DATA_SOURCE=live` (veya demo mod için `demo`)

### 2) Backend Deployment (Render)
- Platform: [Render](https://render.com/)
- Service Type: Web Service (Python)
- **Root Directory: `backend` (zorunlu)**
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment Variables (örnek):
  - `GEMINI_API_KEY=...`
  - `FOURSQUARE_API_KEY=...`
  - `DATABASE_URL=...` (prod için önerilir)
  - `APP_ENV=production`

### 3) Frontend <-> Backend Bağlantısı
- Render deploy URL'sini alın (ör. `https://vibecheck-api.onrender.com`)
- Vercel'de `VITE_API_BASE_URL` değerini bu URL ile güncelleyin
- Backend health kontrolü:
  - `GET https://<render-url>/health`
- API docs:
  - `https://<render-url>/docs`

### 4) Jüri Teslim Kontrol Listesi
- Monorepo ayrımı net:
  - Frontend sadece `frontend/`
  - Backend sadece `backend/`
- Gizli anahtarlar Git'e gitmez:
  - `backend/.env` ve `frontend/.env` ignore edilir
- Şablon env dosyaları mevcut:
  - `backend/.env.example`
  - `frontend/.env.example`
- `prodocs/` belgeleri güncel:
  - `PRD.md`, `tech-stack.md`, `Plan.md`, `DesignSystem.md`, `Progress.md`

## Yerel Geliştirme

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Güvenlik Notu

`.env` dosyaları commit edilmez. Sadece `.env.example` şablonları repo içinde tutulur.
