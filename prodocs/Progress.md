# Progress — Velo / VibeCheck

Proje geliştirme günlüğü: yapılan işler, kararlar ve karşılaşılan hatalar.

---

## 2026-06-16 — Repo teslim düzeni

### Yapılanlar
- Zorunlu dokümanlar `prodocs/` altına taşındı: PRD, tech-stack, Plan, DesignSystem, Progress
- `prodocs/PRD.md` oluşturuldu
- Kök `.env.example` eklendi
- `.gitignore` genişletildi (`*.db`, `__pycache__`, `node_modules`, `.env`)
- `README.md` teslim formatına göre güncellendi (monorepo + deploy onepager)
- `prodocs/TESLIM-KONTROL.md` eklendi (jüri kontrol listesi)
- CORS fix: `allow_origins=["*"]` (Vercel ↔ Render)

### Kararlar
- Dokümanlar kökte değil `prodocs/` içinde tutulacak (jüri brief uyumu)
- SQLite dosyaları repodan çıkarıldı (local dev artifact)

---

## 2026-06-14 — Teslim hazırlığı

### Yapılanlar
- Gemini API entegrasyonu `hotel_analysis_service.py` içinde 6 kriterli formata geri getirildi
- API key yoksa heuristic fallback korundu
- CORS middleware eklendi (`CORS_ORIGINS` env)
- `HotelAnalysisCard` hardcoded localhost yerine `VITE_API_BASE_URL` kullanıyor
- `render.yaml` (backend) ve `vercel.json` (frontend) deploy config eklendi
- Kök dokümanlar oluşturuldu: README, PRD, tech-stack, Plan, DesignSystem, Progress
- `prodocs/` AI referans klasörü eklendi
- Backend test: `test_hotel_analysis_endpoint` eklendi (4 test geçti)
- Frontend build düzeltildi (`vite-env.d.ts`)

### Kararlar
- **Gemini** otel toplu analizi için; **OpenAI** tekil NLP/özet için (maliyet/hız)
- Render'da `CELERY_EAGER=true` — Redis olmadan demo deploy
- SQLite Render demo için yeterli; prod için PostgreSQL önerilir

### Hatalar / Çözümler
| Hata | Çözüm |
|------|-------|
| `hotel_analysis_service` mock'a kilitlenmişti | Servis yeniden yazıldı, `_use_mock` sadece key yoksa |
| Frontend `localhost:8000` hardcoded | `hotelAnalysisService.ts` + env |
| `npm run build` TS hataları | `src/vite-env.d.ts` eklendi |
| `App.tsx` geçersiz `reviews` prop | Prop kaldırıldı, kart kendi state'ini yönetiyor |

### Bekleyen
- [ ] Render + Vercel canlı deploy (kullanıcı API key ile)
- [ ] README'deki canlı URL'lerin güncellenmesi
- [ ] Demo video çekimi

---

## 2026-06-14 (önceki commit) — Gemini entegrasyon commit

- Commit: `238f98a` — Otel yorumları FastAPI + React + Gemini
- Sonrasında servis güvenli moda alınmıştı (mock only) — bugün düzeltildi

---

## 2026-06-XX — End-to-end entegrasyon

- Commit: `4bdfc13` — Frontend ve AI backend birleştirildi
- Mock/live veri kaynağı switch (`VITE_DATA_SOURCE`)

---

## 2026-06-XX — İlk kurulum

- Commit: `d203b86` — LLM + Frontend iskelet
- FastAPI routers, React prototype, seed data

---

## Usability Test Özeti

2 tur prototype testi (`frontend/docs/usability-test-report.md`):
- Truth Dashboard tarih etiketleri güven artırıyor
- Persona filtreleri karar hızını iyileştiriyor
- Velo analiz kartı “yorum okuma yükünü” azaltıyor

---

## Bilinen Limitasyonlar

1. VibeCheck prototype verisi çoğunlukla mock
2. Render free tier cold start (~30–60 sn)
3. `google.generativeai` paketi deprecated — ileride `google.genai` migrasyonu
4. Celery prod için Redis gerekir (demo'da eager mode)
