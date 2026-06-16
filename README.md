# VibeCheck — AI Destekli Otel Seçim Asistanı

VibeCheck, tatil planlayan kullanıcıların otel yorumlarını yapay zeka ile analiz edip kişisel tercihlerine göre otel öneren bir web uygulamasıdır.

## Repo Yapısı (Monorepo)

```text
PlanGo/
├── frontend/          # React + Vite arayüz (Vercel deploy)
├── backend/           # FastAPI REST API (Render deploy)
├── prodocs/           # Zorunlu teslim dokümanları + AI referansları
│   ├── PRD.md
│   ├── tech-stack.md
│   ├── Plan.md
│   ├── DesignSystem.md
│   ├── Progress.md
│   ├── architecture.md
│   └── api-reference.md
├── .gitignore
├── .env.example       # Kök env şablonu (gerçek key yok)
├── README.md          # Bu dosya
└── render.yaml        # Render blueprint (backend)
```

## Ne Yapar?

1. Kullanıcı il seçer ve tatil tercihlerini yazar
2. Oteller kriterlere göre sıralanır
3. Yapay zeka otel yorumlarını 10 kategoride skorlar
4. Kullanıcı beğendiği otelde harita üzerinden rezervasyona yönlendirilir

## Onepager Deployment Rehberi

### Frontend — Vercel

| Ayar | Değer |
|------|-------|
| Root Directory | `frontend` |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Env | `VITE_API_BASE_URL=https://<render-backend-url>` |

### Backend — Render

| Ayar | Değer |
|------|-------|
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Env | `GEMINI_API_KEY`, `FOURSQUARE_API_KEY` (bkz. `backend/.env.example`) |

### Bağlantı Testi

- Health: `GET https://<backend-url>/health`
- API Docs: `https://<backend-url>/docs`

## Yerel Kurulum

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

Tarayıcı: `http://localhost:5173` — API: `http://localhost:8000`

## Güvenlik

- `backend/.env` ve `frontend/.env` Git'e **yüklenmez**
- Sadece `.env.example` şablonları repoda tutulur
- LLM API anahtarları yalnızca backend tarafında kullanılır

## Teslim Dokümanları

Tüm zorunlu belgeler `prodocs/` klasöründedir:

- [PRD.md](prodocs/PRD.md) — Problem, hedef kitle, özellikler
- [tech-stack.md](prodocs/tech-stack.md) — Teknoloji seçimleri ve AI kullanımı
- [Plan.md](prodocs/Plan.md) — Kullanıcı hikayeleri ve teknik adımlar
- [DesignSystem.md](prodocs/DesignSystem.md) — Renk, tipografi, component kuralları
- [Progress.md](prodocs/Progress.md) — Geliştirme günlüğü

## Lisans

Eğitim projesi — Future Talent 2026
