# VibeCheck 8-Week MVP Architecture

Bu dokuman, canlıya alinacak decoupled (frontend/backend ayrik) bir AI web uygulamasi icin baslangic mimarisini tanimlar.

## Tech Stack

- Frontend: React + Vite + TypeScript
- Backend: FastAPI + Pydantic
- AI Provider: Gemini API (backend uzerinden), fallback mock
- Data: Postgres (hedef), mevcutta SQLite/dev
- Deployment: Frontend (Vercel/Netlify), Backend (Render/Railway)

## Monorepo Klasor Yapisi

```text
PlanGo/
  frontend/
    src/
      app/                 # route/layout state
      features/            # domain modules
      services/            # backend API clients
      components/          # shared UI
      pages/               # screen-level components
      lib/                 # helpers, constants
    public/
    .env.example
  backend/
    app/
      main.py
      core/                # config, middleware, security
      api/                 # deps, versioning
      routers/             # REST endpoints
      schemas/             # request/response DTO
      services/            # business logic + AI integration
      repositories/        # db access layer
      models/              # ORM models
      db/                  # session + migrations setup
      workers/             # async jobs (optional)
    tests/
    .env.example
  PROJECT_ARCHITECTURE_MVP.md
```

## 8 Hafta Yol Haritasi

1. Hafta 1: Boilerplate, env, CORS, health, auth iskeleti
2. Hafta 2: Register/Login + token guard + user profile
3. Hafta 3: Prompt/generation API + DB persistence
4. Hafta 4: Gercek Gemini entegrasyonu + prompt safety
5. Hafta 5: Frontend auth flow + protected pages
6. Hafta 6: CRUD + filtreleme + kalite iyilestirmeleri
7. Hafta 7: Monitoring, logging, error handling, test
8. Hafta 8: Deployment, smoke tests, demo polish

## MVP API Contract (Baslangic)

- `POST /mvp/auth/register`
- `POST /mvp/auth/login`
- `POST /mvp/ai/generate` (Auth gerekli)
- `POST /mvp/generations` (Auth gerekli)
- `GET /mvp/generations` (Auth gerekli)

## Deployment Hazirlik Kurallari

- Secretlar sadece `.env` ile alinacak, kodda hardcode yok
- Frontend sadece backend API URL'sini gorecek (`VITE_API_BASE_URL`)
- LLM API key sadece backend tarafinda tutulacak
- Her ortam icin ayri env (`dev`, `staging`, `prod`)
