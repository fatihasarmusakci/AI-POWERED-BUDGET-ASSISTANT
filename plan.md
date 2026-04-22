# 🌍 AI-Travel Buddy — Proje Planlama Dokümanı

> **Versiyon:** 1.0.0 | **Tarih:** 2026-04-22  
> **Stack:** FastAPI · Flutter · PostgreSQL · Redis · Pinecone · Claude/GPT-4o

---

## 📋 İçindekiler

1. [Proje Özeti](#proje-özeti)
2. [Mimari Genel Bakış](#mimari)
3. [Klasör Yapısı](#klasör-yapısı)
4. [Veritabanı Şeması](#veritabanı-şeması)
5. [API Endpoint Planı](#api-endpoint-planı)
6. [Kurulum Adımları](#kurulum-adımları)
7. [Ortam Değişkenleri (.env)](#ortam-değişkenleri)
8. [Geliştirme Yol Haritası](#geliştirme-yol-haritası)

---

## Proje Özeti

AI-Travel Buddy; kullanıcıların otel yorumlarını AI ile analiz ederek karar yorgunluğunu azaltan, kişiselleştirilmiş seyahat tavsiyesi sunan bir mobil + API uygulamasıdır.

**Temel Özellikler:**
- Otel yorumlarını `temizlik / çocuk uyumu / yemek / gürültü` kategorilerinde AI ile skorlama
- Son 6 aya ağırlıklı (%70) recency bias puanlama algoritması
- Yorumları kaynak `source_id` ile eşleştiren hallucination-guard mekanizması
- Tüm AI yanıtları Redis'te 7 gün cache'leme
- Kullanıcı dostu, seyahat temalı hata mesajları

---

## Mimari

```
┌─────────────────────────────────────────────────────────┐
│                     Flutter App                         │
│              (iOS · Android · Web)                      │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTPS / REST
┌───────────────────────▼─────────────────────────────────┐
│                  FastAPI Backend                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Routers  │  │Services  │  │Controllers│             │
│  └────┬─────┘  └────┬─────┘  └─────┬────┘             │
│       └─────────────┴──────────────┘                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Core Layer                         │   │
│  │  Auth · Cache(Redis) · DB(SQLAlchemy) · AI      │   │
│  └─────────────────────────────────────────────────┘   │
└─────┬──────────────┬──────────────┬────────────────────┘
      │              │              │
┌─────▼───┐   ┌──────▼──────┐  ┌───▼──────────┐
│PostgreSQL│   │    Redis    │  │   Pinecone   │
│  (ORM)  │   │  (7d Cache) │  │ (Vector DB)  │
└─────────┘   └─────────────┘  └──────────────┘
                                       │
                              ┌────────▼────────┐
                              │  LLM Provider   │
                              │ Claude / GPT-4o │
                              └─────────────────┘
```

---

## Klasör Yapısı

```
ai-travel-buddy/
│
├── backend/                          # FastAPI uygulaması
│   ├── app/
│   │   ├── main.py                   # Uygulama giriş noktası, lifespan
│   │   ├── config.py                 # Pydantic Settings (.env okur)
│   │   │
│   │   ├── api/                      # Route tanımları
│   │   │   ├── v1/
│   │   │   │   ├── hotels.py         # Otel endpoint'leri
│   │   │   │   ├── reviews.py        # Yorum endpoint'leri
│   │   │   │   ├── ai_analysis.py    # AI analiz endpoint'leri
│   │   │   │   ├── auth.py           # Auth endpoint'leri
│   │   │   │   └── search.py         # Arama endpoint'leri
│   │   │   └── router.py             # Ana router birleştirici
│   │   │
│   │   ├── controllers/              # Request/Response işleme katmanı
│   │   │   ├── hotel_controller.py
│   │   │   ├── review_controller.py
│   │   │   └── ai_controller.py
│   │   │
│   │   ├── services/                 # İş mantığı katmanı
│   │   │   ├── hotel_service.py
│   │   │   ├── review_service.py
│   │   │   ├── ai_service.py         # LLM çağrıları (LangChain/Anthropic)
│   │   │   ├── scoring_service.py    # Recency bias puanlama algoritması
│   │   │   ├── cache_service.py      # Redis cache yönetimi
│   │   │   └── vector_service.py     # Pinecone vektör işlemleri
│   │   │
│   │   ├── models/                   # SQLAlchemy ORM modelleri
│   │   │   ├── user.py
│   │   │   ├── hotel.py
│   │   │   ├── review.py
│   │   │   ├── ai_analysis.py
│   │   │   └── base.py
│   │   │
│   │   ├── schemas/                  # Pydantic şemaları (I/O)
│   │   │   ├── hotel.py
│   │   │   ├── review.py
│   │   │   ├── ai_analysis.py
│   │   │   └── common.py
│   │   │
│   │   ├── core/                     # Altyapı & ortak araçlar
│   │   │   ├── database.py           # Async DB bağlantısı
│   │   │   ├── redis.py              # Redis bağlantısı
│   │   │   ├── security.py           # JWT / OAuth
│   │   │   ├── exceptions.py         # Custom exception sınıfları
│   │   │   └── middleware.py         # Logging, error handling
│   │   │
│   │   └── utils/
│   │       ├── scoring.py            # Recency bias matematiksel fonksiyonlar
│   │       ├── hallucination_guard.py # source_id eşleştirme
│   │       └── travel_messages.py    # Seyahat temalı hata mesajları
│   │
│   ├── alembic/                      # DB migration'ları
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   │
│   ├── .env.example
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── frontend/                         # Flutter uygulaması
│   ├── lib/
│   │   ├── main.dart
│   │   ├── core/
│   │   │   ├── theme/
│   │   │   ├── constants/
│   │   │   └── network/              # Dio HTTP client
│   │   ├── features/
│   │   │   ├── hotels/
│   │   │   │   ├── data/
│   │   │   │   ├── domain/
│   │   │   │   └── presentation/
│   │   │   ├── reviews/
│   │   │   ├── ai_analysis/
│   │   │   └── auth/
│   │   └── shared/                   # Atomic design widget'ları
│   │       ├── atoms/
│   │       ├── molecules/
│   │       └── organisms/
│   ├── pubspec.yaml
│   └── Dockerfile
│
├── docker-compose.yml                # Tüm servisler
├── plan.md                           # Bu dosya
└── README.md
```

---

## Veritabanı Şeması

### PostgreSQL Tabloları

```sql
-- Kullanıcılar
users
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid()
  email         VARCHAR(255) UNIQUE NOT NULL
  full_name     VARCHAR(255)
  hashed_password TEXT
  is_active     BOOLEAN DEFAULT true
  created_at    TIMESTAMPTZ DEFAULT now()

-- Oteller
hotels
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid()
  name          VARCHAR(500) NOT NULL
  city          VARCHAR(255)
  country       VARCHAR(255)
  address       TEXT
  star_rating   SMALLINT
  latitude      DECIMAL(9,6)
  longitude     DECIMAL(9,6)
  pinecone_id   VARCHAR(255)        -- Vektör DB referansı
  created_at    TIMESTAMPTZ DEFAULT now()
  updated_at    TIMESTAMPTZ DEFAULT now()

-- Yorumlar
reviews
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid()
  hotel_id      UUID REFERENCES hotels(id) ON DELETE CASCADE
  source        VARCHAR(100)       -- 'booking', 'tripadvisor', 'google'
  source_review_id VARCHAR(255)    -- Kaynak sistemdeki orijinal ID
  author_name   VARCHAR(255)
  rating        DECIMAL(3,1)
  review_text   TEXT NOT NULL
  review_date   TIMESTAMPTZ NOT NULL
  language      VARCHAR(10) DEFAULT 'tr'
  created_at    TIMESTAMPTZ DEFAULT now()
  INDEX idx_reviews_hotel_id (hotel_id)
  INDEX idx_reviews_date (review_date)

-- Yorum Kategorileri (analiz sonuçları)
review_categories
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid()
  review_id     UUID REFERENCES reviews(id) ON DELETE CASCADE
  cleanliness   DECIMAL(4,2)       -- 0.00 - 10.00 skoru
  child_friendly DECIMAL(4,2)
  food          DECIMAL(4,2)
  noise         DECIMAL(4,2)       -- Düşük = gürültülü (ters skala)
  sentiment     VARCHAR(20)        -- 'positive', 'negative', 'neutral'
  analyzed_at   TIMESTAMPTZ DEFAULT now()

-- AI Analizleri (cache + kayıt)
ai_analyses
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid()
  hotel_id      UUID REFERENCES hotels(id) ON DELETE CASCADE
  analysis_type VARCHAR(100)       -- 'summary', 'scoring', 'comparison'
  prompt_hash   VARCHAR(64)        -- Cache key için SHA256
  result_json   JSONB NOT NULL     -- AI çıktısı
  source_ids    UUID[]             -- Hallucination guard: kaynak yorum ID'leri
  model_used    VARCHAR(100)       -- 'claude-3-5-sonnet', 'gpt-4o'
  tokens_used   INTEGER
  cached_until  TIMESTAMPTZ        -- Redis TTL senkronizasyonu
  created_at    TIMESTAMPTZ DEFAULT now()

-- Otel Skor Kartları (hesaplanmış, cache'lenmiş)
hotel_scores
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid()
  hotel_id      UUID REFERENCES hotels(id) ON DELETE CASCADE UNIQUE
  overall_score DECIMAL(4,2)
  cleanliness_score   DECIMAL(4,2)
  child_score         DECIMAL(4,2)
  food_score          DECIMAL(4,2)
  noise_score         DECIMAL(4,2)
  review_count        INTEGER
  recent_review_count INTEGER       -- Son 6 ay
  last_calculated     TIMESTAMPTZ DEFAULT now()

-- Kullanıcı Favorileri
user_favorites
  user_id       UUID REFERENCES users(id) ON DELETE CASCADE
  hotel_id      UUID REFERENCES hotels(id) ON DELETE CASCADE
  created_at    TIMESTAMPTZ DEFAULT now()
  PRIMARY KEY (user_id, hotel_id)
```

---

## API Endpoint Planı

```
/api/v1/

# Kimlik Doğrulama
POST   /auth/register
POST   /auth/login
POST   /auth/refresh
DELETE /auth/logout

# Oteller
GET    /hotels                  # Şehir/ülke filtreli liste
GET    /hotels/{hotel_id}       # Otel detayı + skor kartı
GET    /hotels/{hotel_id}/score # Hesaplanmış skor kartı
POST   /hotels                  # Yeni otel ekle (admin)

# Yorumlar
GET    /hotels/{hotel_id}/reviews       # Sayfalı yorum listesi
POST   /hotels/{hotel_id}/reviews       # Yorum ekle
GET    /reviews/{review_id}

# AI Analiz
GET    /hotels/{hotel_id}/ai-summary    # AI özet (Redis cached)
GET    /hotels/{hotel_id}/ai-score      # Kategorik AI skorlama
POST   /hotels/{hotel_id}/ai-compare    # Otel karşılaştırma

# Arama
GET    /search/hotels           # Metin + vektör hibrit arama
GET    /search/suggestions      # Otomatik tamamlama

# Favoriler
GET    /users/me/favorites
POST   /users/me/favorites/{hotel_id}
DELETE /users/me/favorites/{hotel_id}
```

---

## Kurulum Adımları

### 1. Ön Gereksinimler

```bash
# Python 3.11+
python --version

# Node.js (npm için, opsiyonel araçlar)
node --version

# Docker & Docker Compose
docker --version
docker compose version

# Flutter 3.x (frontend için)
flutter --version
```

### 2. Backend Kurulumu

```bash
# Repoyu klonla
git clone https://github.com/yourname/ai-travel-buddy.git
cd ai-travel-buddy/backend

# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyasını oluştur
cp .env.example .env
# .env dosyasını kendi değerlerinle düzenle

# Veritabanı migration'larını çalıştır
alembic upgrade head

# Geliştirme sunucusunu başlat
uvicorn app.main:app --reload --port 8000
```

### 3. Docker ile Çalıştırma (Önerilen)

```bash
# Tüm servisleri başlat (PostgreSQL + Redis + FastAPI)
cd ai-travel-buddy
docker compose up -d

# Logları izle
docker compose logs -f api

# Sadece veritabanlarını başlat
docker compose up -d postgres redis
```

### 4. Flutter Frontend Kurulumu

```bash
cd ai-travel-buddy/frontend

# Bağımlılıkları yükle
flutter pub get

# Android emülatör veya fiziksel cihazda çalıştır
flutter run

# Web için
flutter run -d chrome
```

### 5. Geliştirme Ortamı Kontrol

```bash
# API sağlık kontrolü
curl http://localhost:8000/health

# Swagger UI
open http://localhost:8000/docs

# ReDoc
open http://localhost:8000/redoc
```

---

## Ortam Değişkenleri

`.env.example` içeriği:

```env
# Uygulama
APP_NAME="AI Travel Buddy"
APP_ENV=development
DEBUG=true
SECRET_KEY=your-super-secret-jwt-key-change-in-production

# PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ai_travel_buddy

# Redis
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_DAYS=7

# AI Sağlayıcıları (ASLA kod içine yazma!)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
DEFAULT_AI_MODEL=claude-3-5-sonnet-20241022

# Pinecone
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=hotels-reviews

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Scoring
RECENCY_WEIGHT_RECENT=0.70   # Son 6 ay
RECENCY_WEIGHT_OLD=0.30       # 6 aydan eski
RECENCY_MONTHS_THRESHOLD=6
```

---

## Geliştirme Yol Haritası

### 🏗️ Faz 1 — Temel Altyapı (1-2 Hafta)
- [x] Proje planı ve mimari tasarım
- [ ] PostgreSQL şeması + Alembic migration'ları
- [ ] FastAPI iskelet yapısı (main, config, router)
- [ ] Redis bağlantısı ve cache servisi
- [ ] JWT auth sistemi
- [ ] Docker Compose ortamı

### 🔍 Faz 2 — Veri Katmanı (2-3 Hafta)
- [ ] Otel ve yorum CRUD endpoint'leri
- [ ] Recency bias puanlama algoritması
- [ ] Yorum kategori analizi (temizlik/çocuk/yemek/gürültü)
- [ ] Pinecone vektör entegrasyonu

### 🤖 Faz 3 — AI Özellikleri (2-3 Hafta)
- [ ] AI özet servisi (LangChain + Claude)
- [ ] Hallucination guard (source_id eşleştirme)
- [ ] AI skor kartı üretimi
- [ ] Redis caching + 7 günlük TTL
- [ ] Otel karşılaştırma endpoint'i

### 📱 Faz 4 — Flutter Frontend (3-4 Hafta)
- [ ] Atomic design widget sistemi
- [ ] Otel arama & listeleme ekranı
- [ ] Skor kartı bileşeni (AI powered)
- [ ] Yorum detay & kaynak gösterimi
- [ ] Favori listesi

### 🚀 Faz 5 — Production Hazırlık (1-2 Hafta)
- [ ] Unit & integration testler
- [ ] CI/CD pipeline
- [ ] Monitoring (Sentry / Prometheus)
- [ ] API rate limiting
- [ ] Güvenlik denetimi

---

## Teknik Notlar

### Recency Bias Algoritması
```
final_score = (son_6_ay_yorumlar * 0.70) + (eski_yorumlar * 0.30)
```
Matematiksel detaylar: `backend/app/utils/scoring.py`

### Hallucination Guard Kuralı
Her AI özeti üretilirken:
1. Kullanılan yorum ID'leri `source_ids[]` dizisine kaydedilir
2. AI çıktısındaki her claim, en az bir `source_id`'ye bağlı olmalıdır
3. Kaynaksız claim → kullanıcıya gösterilmez

### Seyahat Temalı Hata Mesajları
```python
# Kötü ✗
"500 Internal Server Error"

# İyi ✓  
"AI rehberimiz şu an biraz meşgul, lütfen manuel yorumlara göz atın ✈️"
"Bağlantımız biraz türbülansta, kısa süre sonra tekrar deneyin 🌤️"
```

---

*Bu doküman yaşayan bir belgedir. Her sprint'te güncellenir.*