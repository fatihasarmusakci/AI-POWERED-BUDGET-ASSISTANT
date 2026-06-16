# Teslim Kontrol Listesi — VibeCheck (PlanGo)

Bu dosya, Future Talent 2026 Bitirme Projesi teslim kriterlerine göre hazırlanmıştır.  
Eğitmen ve asistanlar en güncel commit üzerinden bu listeyi kullanarak kontrol yapabilir.

---

## 1. Repo Yapısı (Monorepo)

| Klasör / Dosya | Açıklama | Durum |
|----------------|----------|-------|
| `frontend/` | React + Vite arayüz kodu | ✅ |
| `backend/` | FastAPI REST API | ✅ |
| `prodocs/` | Yapay zeka ajanları ve teslim dokümanları | ✅ |
| `.gitignore` | Gereksiz dosyaların repoya girmesini engeller | ✅ |
| `README.md` | Onepager: ne yapar + nasıl deploy edilir | ✅ |
| `.env.example` | Gerçek API anahtarı olmadan env şablonu (kök) | ✅ |
| `frontend/.env.example` | Frontend env şablonu | ✅ |
| `backend/.env.example` | Backend env şablonu | ✅ |

---

## 2. Zorunlu Dokümanlar (`prodocs/`)

| Dosya | İçerik | Durum |
|-------|--------|-------|
| `PRD.md` | Problem, hedef kullanıcı, temel özellikler | ✅ |
| `tech-stack.md` | Teknolojiler, servis gerekçeleri, AI kullanımı | ✅ |
| `Plan.md` | PRD'den türetilen kullanıcı hikayeleri ve teknik adımlar | ✅ |
| `DesignSystem.md` | Renk paleti, tipografi, component kuralları | ✅ |
| `Progress.md` | Yapılan işler, kararlar ve hataların kaydı | ✅ |

Ek referans dosyaları: `architecture.md`, `api-reference.md`, `PROJECT_ARCHITECTURE_MVP.md`

---

## 3. Güvenlik

| Kural | Durum |
|-------|-------|
| `backend/.env` GitHub'da **yok** | ✅ |
| `frontend/.env` GitHub'da **yok** | ✅ |
| Gerçek API anahtarları commit edilmedi | ✅ |
| LLM API key yalnızca backend'de kullanılıyor | ✅ |
| `*.db` dosyaları repoda yok | ✅ |
| `__pycache__` / `node_modules` repoda yok | ✅ |

---

## 4. Deploy

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

- `GET /health` → `{"status":"ok"}`
- API Docs → `/docs`
- CORS → `allow_origins=["*"]` (Vercel ↔ Render)

---

## 5. Yerel Çalıştırma (Hızlı Test)

```bash
# Backend
cd backend && cp .env.example .env
# .env içine key'leri ekle, sonra:
uvicorn app.main:app --reload

# Frontend (ayrı terminal)
cd frontend && cp .env.example .env
npm install && npm run dev
```

Tarayıcı: `http://localhost:5173`  
API: `http://localhost:8000`

---

## 6. Demo Video Konuları (5 dk)

- [ ] Problem & hedef kitle
- [ ] Çözüm (tek cümle)
- [ ] Proje mimarisi (frontend / backend / AI katmanı)
- [ ] Canlı ürün demosu (AI analiz anı)
- [ ] Tech stack & AI kullanımı
- [ ] Rekabet farkı
- [ ] Gelecek planları & kapanış

---

## 7. Son Kontrol (Push Öncesi)

- [x] Tüm dosyalar `main` branch'te
- [x] Kökte dağınık doküman yok (hepsi `prodocs/` altında)
- [x] `.env` dosyaları ignore ediliyor
- [x] README güncel
- [ ] Canlı Vercel URL README'ye eklendi *(deploy sonrası)*
- [ ] Canlı Render URL README'ye eklendi *(deploy sonrası)*
- [ ] Demo video linki teslim formuna eklendi *(son adım)*

---

**Repo:** https://github.com/fatihasarmusakci/PlanGo  
**Son güncelleme:** 2026-06-16
