# PRD: ParaNerede? (AI-Powered Budget Assistant) 
**Sürüm:** 1.0 (MVP)  
**Durum:** Hazır / Geliştirme Aşamasında  
**Rol:** Kıdemli Ürün Uzmanı & CPO Vizyonu

## 1. Ürün Vizyonu ve Değer Önerisi
* **Vizyon:** Ekonomik belirsizlik dönemlerinde kullanıcıya saniyeler içinde mali kontrol hissi veren en hızlı asistan olmak.
* **Temel Değer:** "10 saniyede harcamanı kaydet, ay sonu sürprizlerinden kurtul."

## 2. Hedef Metrikler (KPIs)
* **Time-to-Log (T2L):** Harcama giriş süresinin 8 saniyenin altında tutulması.
* **Retention (D7):** Kullanıcıların %40'ının 7. günde uygulamayı aktif kullanması.
* **Data Accuracy:** AI tarafından ayrıştırılan verilerin %95 doğruluk payı.

## 3. Kullanıcı Hikayeleri (User Stories)

| ID | Kullanıcı Hikayesi | Kabul Kriterleri (Acceptance Criteria) |
| :--- | :--- | :--- |
| **US.01** | Bir kullanıcı olarak kopyaladığım banka SMS'inin otomatik algılanmasını istiyorum. | 1. Uygulama açıldığında Clipboard kontrol edilir. <br> 2. SMS kalıbı uygunsa onay modalı çıkar. |
| **US.02** | Bir kullanıcı olarak fiş fotoğrafı çekerek harcama girmek istiyorum. | 1. OCR + GPT-4o-mini entegrasyonu ile veri çekilir. <br> 2. Tutar, kategori ve işyeri otomatik atanır. |
| **US.03** | Bir kullanıcı olarak "Güvenli Limitimi" anlık görmek istiyorum. | 1. Maaş günü ve sabit giderlere göre günlük bütçe hesaplanır. <br> 2. Her harcamada bu limit real-time güncellenir. |

## 4. Teknik Gereklilikler & Mimari

### 4.1. Teknoloji Stack
- **Frontend:** React Native (Expo) - Hızlı prototipleme ve Cross-platform desteği.
- **Veritabanı:** WatermelonDB (SQLite tabanlı) - Local-first ve yüksek performanslı gözlemleme.
- **AI Engine:** OpenAI `gpt-4o-mini` - Hız ve maliyet optimizasyonu için.
- **State Management:** Zustand - Hafif ve hızlı state yönetimi.

### 4.2. Veri Modeli (Schema)
```sql
Table transactions {
  id: uuid [primary key]
  amount: decimal (cents) // 100.50 TL -> 10050
  category: enum (Food, Transport, Rent, Health, etc.)
  merchant: string
  source: enum (SMS, VISION, MANUAL)
  created_at: timestamp
}

Table user_config {
  id: uuid
  monthly_income: decimal
  fixed_expenses: decimal
  payday: integer (1-31)
}

4.3. AI Veri İşleme Akışı
Girdi: Ham SMS metni veya base64 formatında sıkıştırılmış fiş görseli.

İşlem: gpt-4o-mini modeline gönderilen sistem promptu ile JSON çıktısı zorlaması.

Çıktı Formatı:

JSON

{
  "amount": 245.50,
  "merchant": "MIGROS",
  "category": "Market",
  "confidence_score": 0.98
}
5. Fonksiyonel Detaylar & UX Kuralları
5.1. "Safe-to-Spend" Algoritması
Sistemin kalbi olan algoritma her işlemde şu formülü çalıştırır:
Günlük Limit = (Net Gelir - Sabit Giderler - Ay İçindeki Toplam Harcama) / Maaşa Kalan Gün Sayısı

5.2. Gamification (Retention)
Daily Streak: Her gün en az 1 kayıt giren kullanıcıya "Ateş" (Streak) ikonu gösterilir.

Lock System: Haftalık harcama analizi raporu, sadece 7 günlük streak yapan kullanıcılara açılır.

5.3. Hata Yönetimi (Edge Cases)
Offline Mod: İnternet yoksa fiş tarama işlemi kuyruğa alınır (Queue), manuel giriş engellenmez.

Duplicate Check: Son 10 dakika içinde girilen aynı tutarlı harcamalar için "Mükerrer olabilir" uyarısı verilir.

6. Uygulama Yol Haritası (Roadmap)
Hafta 1: Temel CRUD işlemleri ve Local DB kurulumu.

Hafta 2: AI Entegrasyonu (Vision + SMS Analiz).

Hafta 3: Dashboard tasarımı ve Safe-to-Spend algoritması.

Hafta 4: Bildirimler, Gamification ve Test (Beta Launch).

7. Geliştirici İçin Başlangıç Komutu (Cursor Prompt)
"React Native + WatermelonDB kullanarak local-first bir bütçe uygulaması iskeleti oluştur. Ana sayfada 'Safe-to-Spend' hesaplamasını gösteren bir kart olsun. Pano (Clipboard) dinleyicisi ekle; içinde 'TL' ve 'Harcama' geçen bir metin bulursan bunu analiz edip kullanıcıya onaylatacak bir BottomSheet aç. UI için modern, minimalist ve koyu tema tercih et."
### **Nasıl Kullanılır?**
1.  Yukarıdaki metni kopyalayın.
2.  `.md` uzantılı bir dosya olarak kaydedin (Örn: `PARA_NEREDE_PRD.md`).
3.  Projenin ana klasörüne veya dokümantasyon klasörüne ekleyin.

Bu döküman, hem iş biriminin beklentilerini hem de yazılımcının ihtiyaç duyduğu teknik derinliği bir araya getirerek projenin **"unicorn hızıyla"** ilerlemesini sağlayacaktır. Başka bir detay eklememi ister misin?
