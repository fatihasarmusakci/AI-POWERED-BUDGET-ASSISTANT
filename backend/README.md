# VibeCheck AI Backend

FastAPI + SQLAlchemy (PostgreSQL veya yerel SQLite) + Celery + OpenAI ile **Smart-Scoring**, yorum NLP analizi, görsel dürüstlük skoru ve özet API’leri.

## Kurulum

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Üretim için PostgreSQL kullanın; `DATABASE_URL` ve eşleşen `SYNC_DATABASE_URL` ortam değişkenlerini ayarlayın (Celery worker aynı veritabanına yazabilmelidir).

```bash
export DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/vibecheck
export SYNC_DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/vibecheck
export OPENAI_API_KEY=sk-...
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

Yerel geliştirme için varsayılanlar SQLite tek dosyasıdır (`./vibecheck.db`).

## API’yi çalıştırma

```bash
uvicorn app.main:app --reload
```

## Celery worker

```bash
celery -A app.workers.celery_app worker --loglevel=INFO
```

Test veya Redis olmadan yerel çalıştırma için `CELERY_EAGER=true` kullanılabilir (görevler süreç içinde çalışır).

## Örnek veri (seed)

```bash
.venv/bin/python seed.py
```

Zorunlu yeniden yükleme: `SEED_FORCE=true .venv/bin/python seed.py`

## Testler

```bash
.venv/bin/python -m pytest
```

`conftest.py` test veritabanını ayırır ve `CELERY_EAGER=true` kullanır.

## Mimari

- **Routers**: HTTP katmanı (controller benzeri)
- **Repositories**: SQLAlchemy veri erişimi
- **Services**: NLP (`NLPService`), dinamik skor (`scoring_service`), görsel dürüstlük (`honesty_service`), özet (`SummarizationService`)
- **Workers**: Celery görevleri (`reviews.analyze_review`)
- **Core**: `Settings`, özel istisnalar, `ErrorHandlingMiddleware`, `register_exception_handlers`

## Önemli uç noktalar

| Metot | Yol | Açıklama |
|-------|-----|----------|
| GET | `/health` | Sağlık |
| GET | `/hotels?city=london` | Konum filtresiyle otel kartları (Smart skor + vibe etiketleri) |
| POST | `/users` | Kullanıcı + `persona_data` (ağırlıklar veya titizlik/sessizlik tercihi) |
| GET | `/users` | Kullanıcı listesi (demo id bulmak için) |
| GET | `/users/{user_id}` | Kullanıcı detayı |
| POST | `/reviews` | Ham yorum; Celery ile NLP analizi kuyruğa alınır |
| GET | `/hotels/{hotel_id}/smart-score?user_id=...&persist=false` | Persona ağırlıklı SmartScore |
| GET | `/hotels/{hotel_id}/visual-honesty` | Resmi foto sayısı vs olumsuz görsel yorumları |
| GET | `/hotels/{hotel_id}/summary` | 3 maddelik metin özet |
| GET | `/hotels/{hotel_id}/tldr` | 3 maddelik yapılandırılmış özet |
| GET | `/hotels/{hotel_id}/truth` | “Truth” karşılaştırması + kırmızı bayraklar |

Mevcut MVP uçları: `/vibe-map`, `/game/guess`, `/insights/daily`, `/staycation/rating`.
