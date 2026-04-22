# 🚀 Product Requirements Document (PRD): AI-Travel Buddy
**Proje Kodu:** TRVL-AI-MVP-001  
**Versiyon:** 1.0 (MVP)  
**Doküman Sahibi:** Ürün Uzmanı (CPO)  
**Tarih:** 22 Nisan 2026  
**Durum:** Hazır (Development Ready)

---

## 1. Executive Summary (Yönetici Özeti)
### 1.1. Problem
Seyahat planlayan kullanıcılar, yüzlerce çelişkili otel yorumu arasında kaybolmakta ("Choice Paralysis"). Geleneksel puanlama sistemleri (4.5/5 gibi) güncelliğini yitirmiş veya manipüle edilmiş olabiliyor.
### 1.2. Çözüm
AI-Travel Buddy, son 6 aydaki kullanıcı yorumlarını doğal dil işleme (NLP) ile analiz ederek; Temizlik, Çocuk, Yemek ve Gürültü gibi kritik kategorilerde objektif ve dinamik skorlar üretir. 
### 1.3. Hedef (North Star)
Kullanıcının karar verme süresini %50 azaltmak ve "Günün İpucu" özelliği ile seyahat dışı dönemlerde de etkileşim (retention) yaratmak.

---

## 2. Kullanıcı Senaryoları (User Stories)
| ID | User Role | Requirement | Benefit |
| :--- | :--- | :--- | :--- |
| **US.1** | Gezgin | Otel yorumlarının özetini görmek isterim | Saatlerce okuma yapmadan hızlı karar verebilmek için. |
| **US.2** | Ebeveyn | "Çocuk dostu" skorunu görmek isterim | Çocuğumla konforlu bir tatil geçireceğimden emin olmak için. |
| **US.3** | Tekrar Eden Kullanıcı | Her gün yeni bir seyahat ipucu/fırsatı almak isterim | Uygulamayı sadece tatil planlarken değil, her gün kullanmak için. |

---

## 3. MVP Özellik Seti (Must-Have)

### 3.1. AI Analiz & Skorlama Motoru (Core)
* **Veri Ingestion:** Google Places/TripAdvisor üzerinden çekilen son 50 yorumun analizi.
* **Dinamik Puanlama:** Son 6 ayın verisine %70 ağırlık veren ağırlıklı ortalama algoritması.
* **AI Özet Kartları:** LLM tarafından üretilen 3 maddelik "Neden Bu Otel?" özeti.
* **Duygu Doğrulama:** Puanların altında kanıt olarak gösterilen 140 karakterlik gerçek yorum snippet'ları.

### 3.2. Günlük Etkileşim Modülü (Retention)
* **Günün Fırsat Analizi:** Belirli bölgelerdeki Fiyat/Performans lideri otellerin listelenmesi.
* **AI Seyahat Hackleri:** Günlük mikro-bilgiler (Örn: "Uçakta en iyi uyku için hangi koltuk seçilmeli?").

---

## 4. Teknik Mimari ve Gereklilikler

### 4.1. Teknoloji Stack
* **AI:** GPT-4o (Derin analiz) & Claude 3 Haiku (Hızlı/Ekonomik özetler).
* **Backend:** Python 3.10+ (FastAPI).
* **Frontend:** Flutter (Cross-platform iOS/Android).
* **Database:** PostgreSQL (User data) + Pinecone (Vector Search).
* **Infrastructure:** Redis (7 günlük analiz önbelleği için).

### 4.2. API Tanımları
* **Endpoint:** `GET /v1/analysis/{hotel_id}`
* **Latency Target:** < 5 saniye (P95).
* **Caching:** Aynı otel için 7 gün boyunca cache'lenmiş sonuç döndürülecek.

---

## 5. Kabul Kriterleri (Acceptance Criteria)
* **AC.1:** Sistem, 50 yorumu 5 saniyeden kısa sürede analiz edip kategorize etmeli.
* **AC.2:** AI özetleri, orijinal metinle %95 oranında semantik doğruluk sağlamalı (Halüsinasyon kontrolü).
* **AC.3:** Kullanıcı ilgi alanı seçtiğinde (örn: Sessizlik), liste buna göre re-rank edilmeli.

---

## 6. Başarı Metrikleri (KPIs)
1.  **Retention:** DAU/MAU oranının %10+ olması.
2.  **Trust Score:** Kullanıcıların AI özetlerini "Faydalı" işaretleme oranının %80+ olması.
3.  **Speed to Insight:** Kullanıcının analiz ekranında geçirdiği sürenin 30 saniyenin altında olması (Hızlı bilgi tüketimi).

---

## 7. Kapsam Dışı (Out of Scope - Phase 2)
* Doğrudan otel rezervasyonu ve ödeme işlemleri.
* Uçak bileti ve araç kiralama modülleri.
* Social Feed (Kullanıcıların birbirini takip etmesi).

---

## 8. Kritik Riskler ve Önlemler
* **Risk:** Yüksek API Maliyetleri. 
* **Önlem:** Popüler lokasyonların analizlerini Redis üzerinde agresif şekilde cache'lemek.
* **Risk:** Yanlış/Eski Yorum Analizi.
* **Önlem:** Analiz algoritmasında "Recency Bias" (Güncellik önceliği) kullanarak eski veriyi filtrelemek.

---
*Bu doküman "AI-Travel Buddy" projesinin teknik ve ürün temelini oluşturur. Değişiklikler için CPO onayı gereklidir.*
