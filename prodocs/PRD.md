# PRD — VibeCheck (PlanGo)

## 1. Problem

Tatil planlayan kullanıcılar otel seçerken yüzlerce yorum, genel yıldız puanı ve pazarlama fotoğrafları arasında kayboluyor. Özellikle aileler ve önceliği net olan gezginler için “bu otel **benim** kriterlerime uygun mu?” sorusuna hızlı cevap bulmak zor.

## 2. Hedef Kitle

- Türkiye’de tatil planlayan aileler ve bireyler
- Temizlik, sessizlik, aile uyumu, Wi-Fi gibi spesifik kriterlere önem veren kullanıcılar
- Rezervasyon öncesi karar vermek isteyen, yorum okumaya zaman ayıramayan gezginler

## 3. Çözüm Özeti

VibeCheck, kullanıcının yazdığı tercihlere göre otelleri sıralar; otel yorumlarını yapay zeka ile kategori bazında analiz eder ve karar vermeden önce net bir profil sunar.

## 4. Temel Özellikler (MVP)

| # | Özellik | Açıklama |
|---|---------|----------|
| 1 | İl bazlı otel listeleme | 81 il seçimi, demo + canlı veri desteği |
| 2 | Tercih motoru | 3 adımlı metin girişi + persona seçimi |
| 3 | Otel bilgi paneli | Fotoğrafa bağımlı olmadan özet profil |
| 4 | AI yorum analizi | 10 kategoride skor (temizlik, sessizlik, aile vb.) |
| 5 | Kriter bazlı sıralama | Kullanıcı metnine göre otel uyum puanı |
| 6 | Rezervasyon yönlendirme | Google Maps üzerinden harici rezervasyon |
| 7 | Canlı deploy | Frontend Vercel, backend Render |

## 5. Başarı Kriterleri

- Kullanıcı 3 dakikada şehir seçip otel karşılaştırması yapabilmeli
- AI analiz kartı otel değişiminde güncellenmeli
- API anahtarları frontend’e sızmamalı
- Uygulama demo modunda internet olmadan da sunulabilmeli

## 6. Kapsam Dışı (v1)

- Uygulama içi ödeme
- Kullanıcı kayıt/giriş (v2 planında)
- Native mobil uygulama

## 7. Teknik Kısıtlar

- Monorepo: `frontend/` + `backend/` + `prodocs/`
- LLM çağrıları yalnızca backend üzerinden
- Gerçek API anahtarları GitHub’a commit edilmez
