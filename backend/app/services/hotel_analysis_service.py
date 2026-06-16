from __future__ import annotations

import json
import logging
from typing import Any

import google.generativeai as genai

from app.core.config import settings

logger = logging.getLogger(__name__)

# ============================================================================
# PROMPT TEMPLATES (Gerçek API bağlandığında kullanılacak taslaklar)
# ============================================================================

# System Prompt: LLM'in rolünü ve görevini tanımlar
_SYSTEM_PROMPT = """Sen bir otel yorumu analizi uzmanısın. Verilen otel yorumlarını analiz ederek aşağıdaki kriterlere göre yapılandırılmış bir JSON döndür.

Görevin:
1. Temizlik durumunu 1-5 arası puanla (1: çok kötü, 5: mükemmel)
2. Otelin çocuk parkı/oyun alanı olup olmadığını tespit et (boolean)
3. Otelin sessizlik durumunu 1-5 arası puanla (1: çok gürültülü, 5: çok sessiz)
4. Personel/servis kalitesini 1-5 arası puanla
5. Konum avantajını 1-5 arası puanla
6. Wi-Fi kalitesi/güvenilirliğini 1-5 arası puanla
7. Kahvaltı kalitesini 1-5 arası puanla
8. Aile/çocuk dostu uygunluğu 1-5 arası puanla
9. Eğlence/aktivite imkanlarını 1-5 arası puanla
10. Oda konforunu/rahatlığını 1-5 arası puanla
11. Fiyat/performans değerini 1-5 arası puanla
12. Yorumlardaki olumlu özellikleri pros listesine ekle
13. Yorumlardaki olumsuz özellikleri cons listesine ekle

Çıktı formatı (tam olarak bu JSON yapısı):
{
  "cleaning_score": 1-5 arası integer,
  "has_playground": boolean,
  "quietness_score": 1-5 arası integer,
  "service_score": 1-5 arası integer,
  "location_score": 1-5 arası integer,
  "wifi_score": 1-5 arası integer,
  "breakfast_score": 1-5 arası integer,
  "family_friendly_score": 1-5 arası integer,
  "entertainment_score": 1-5 arası integer,
  "room_comfort_score": 1-5 arası integer,
  "value_for_money_score": 1-5 arası integer,
  "pros": ["öne çıkan olumlu özellik 1", "öne çıkan olumlu özellik 2", ...],
  "cons": ["olumsuz özellik 1", "olumsuz özellik 2", ...]
}

Kurallar:
- Sadece geçerli JSON döndür, başka metin ekleme
- cleaning_score, quietness_score ve tüm score alanları mutlaka 1-5 arası integer olmalı
- pros ve cons listeleri boş olabilir ama en az 3-5 madde eklemeye çalış
- has_playground: çocuk parkı, oyun alanı, kids club vb. varsa true
- Türkçe veya İngilizce yorumları analiz edebilmelisin
"""

# User Prompt Template: Kullanıcı yorumlarını LLM'e gönderirken kullanılacak
_USER_PROMPT_TEMPLATE = """Aşağıdaki otel yorumlarını analiz et:

{reviews_text}

Yukarıdaki yorumlara göre JSON formatında analiz sonucunu döndür."""


# ============================================================================
# HOTEL ANALYSIS SERVICE
# ============================================================================

class HotelAnalysisService:
    """Otel yorum analizi servisi - Google Gemini API kullanır."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        """
        Servisi başlat.

        Args:
            api_key: Google Gemini API key (None ise mock mod çalışır)
            model: Kullanılacak model (None ise settings'ten alır)
        """
        self._model = model or settings.gemini_model
        key = api_key if api_key is not None else settings.gemini_api_key
        # API key yoksa mock mod çalışır
        self._use_mock = key is None
        if not self._use_mock:
            genai.configure(api_key=key)
            self._model_client = genai.GenerativeModel(self._model)
        else:
            logger.info("No Gemini API key provided, using mock mode")

    def analyze_reviews(self, reviews: list[str], preferences: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Otel yorumlarını analiz et.

        Args:
            reviews: Ham otel yorumları listesi (text array)

        Returns:
            {
                "cleaning_score": 1-5,
                "has_playground": boolean,
                "quietness_score": 1-5,
                "pros": ["string", ...],
                "cons": ["string", ...]
            }
        """
        if self._use_mock:
            logger.info("Using mock mode for hotel analysis (no API key)")
            return self._mock_analyze_reviews(reviews, preferences)

        # Gerçek API çağrısı (API key varsa)
        return self._real_api_analyze_reviews(reviews, preferences)

    def _real_api_analyze_reviews(self, reviews: list[str], preferences: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Gerçek Google Gemini API çağrısı.
        """
        try:
            # Yorumları tek metne birleştir
            pref_text = ""
            if preferences:
                pref_text = f"\nKullanıcı tercihleri: {json.dumps(preferences, ensure_ascii=False)}\n"
            reviews_text = pref_text + "\n---\n".join(reviews)

            # Gemini API çağrısı
            response = self._model_client.generate_content(
                [
                    {"role": "user", "parts": [{"text": _SYSTEM_PROMPT}]},
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": _USER_PROMPT_TEMPLATE.format(
                                    reviews_text=reviews_text[:12_000]
                                )
                            }
                        ],
                    },
                ],
                generation_config=genai.GenerationConfig(
                    temperature=0.2,
                    response_mime_type="application/json",
                ),
            )

            content = response.text or "{}"
            data = json.loads(content)

            # Veri validasyonu
            result = {
                "cleaning_score": self._validate_score(data.get("cleaning_score", 3)),
                "has_playground": bool(data.get("has_playground", False)),
                "quietness_score": self._validate_score(data.get("quietness_score", 3)),
                "service_score": self._validate_score(data.get("service_score", 3)),
                "location_score": self._validate_score(data.get("location_score", 3)),
                "wifi_score": self._validate_score(data.get("wifi_score", 3)),
                "breakfast_score": self._validate_score(data.get("breakfast_score", 3)),
                "family_friendly_score": self._validate_score(data.get("family_friendly_score", 3)),
                "entertainment_score": self._validate_score(data.get("entertainment_score", 3)),
                "room_comfort_score": self._validate_score(data.get("room_comfort_score", 3)),
                "value_for_money_score": self._validate_score(data.get("value_for_money_score", 3)),
                "pros": self._validate_list(data.get("pros", [])),
                "cons": self._validate_list(data.get("cons", [])),
            }

            return result

        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini API failed, falling back to mock: %s", exc)
            return self._mock_analyze_reviews(reviews, preferences)

    def _mock_analyze_reviews(self, reviews: list[str], preferences: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Mock analiz fonksiyonu - Gerçek API olmadığında çalışır.
        
        Hardcoded JSON döner ama gerçek bir analiz yapıyormuş gibi davranır.
        İleride API key alındığında sadece bu fonksiyon yerine _real_api_analyze_reviews
        çağrılacak.
        """
        # Tüm yorumları birleştir ve analiz et
        all_text = " ".join(reviews).lower()
        
        # Heuristik analiz (basit keyword matching)
        cleaning_keywords = ["temiz", "clean", "kirli", "dirty", "küf", "mold", "hygiene"]
        playground_keywords = ["çocuk parkı", "playground", "oyun alanı", "kids club", "children", "kids"]
        quiet_keywords = ["sessiz", "quiet", "gürültü", "noise", "loud", "sakin", "peaceful"]
        
        # Temizlik skoru hesapla
        clean_positive = sum(1 for kw in ["temiz", "clean", "hygiene"] if kw in all_text)
        clean_negative = sum(1 for kw in ["kirli", "dirty", "küf", "mold"] if kw in all_text)
        cleaning_score = max(1, min(5, 3 + clean_positive - clean_negative))
        
        # Playground var mı?
        has_playground = any(kw in all_text for kw in playground_keywords)
        
        # Sessizlik skoru hesapla
        quiet_positive = sum(1 for kw in ["sessiz", "quiet", "sakin", "peaceful"] if kw in all_text)
        quiet_negative = sum(1 for kw in ["gürültü", "noise", "loud"] if kw in all_text)
        quietness_score = max(1, min(5, 3 + quiet_positive - quiet_negative))

        # Ek skorlar (10 özellik)
        service_positive = sum(
            1 for kw in ["personel", "staff", "helpful", "friendly", "welcoming", "yardımsever"] if kw in all_text
        )
        service_negative = sum(1 for kw in ["kaba", "ilgisiz", "unfriendly", "rude"] if kw in all_text)
        service_score = max(1, min(5, 3 + service_positive - service_negative))

        location_positive = sum(
            1 for kw in ["konum", "location", "merkez", "central", "near", "walkable"] if kw in all_text
        )
        location_negative = sum(1 for kw in ["uzak", "far", "noisy area", "zor"] if kw in all_text)
        location_score = max(1, min(5, 3 + location_positive - location_negative))

        wifi_positive = sum(1 for kw in ["wifi", "wi-fi", "internet", "signal", "fast", "stabil", "strong"] if kw in all_text)
        wifi_negative = sum(1 for kw in ["yavaş", "slow", "çalışmıyor", "not working", "kopuyor", "drops"] if kw in all_text)
        wifi_score = max(1, min(5, 3 + wifi_positive - wifi_negative))

        breakfast_positive = sum(1 for kw in ["kahvaltı", "breakfast", "buffet", "breads", "eggs"] if kw in all_text)
        breakfast_negative = sum(1 for kw in ["kötü kahvaltı", "worst breakfast", "soğuk", "bayat", "cold", "stale"] if kw in all_text)
        breakfast_score = max(1, min(5, 3 + breakfast_positive - breakfast_negative))

        family_positive = sum(
            1
            for kw in [
                "çocuk",
                "children",
                "kids",
                "kids club",
                "oyun alanı",
                "playground",
                "family",
                "aile",
                "bebek",
            ]
            if kw in all_text
        )
        family_negative = sum(1 for kw in ["çocuk yok", "no kids", "kid not", "çocuk için uygun değil", "not family"] if kw in all_text)
        family_friendly_score = max(1, min(5, 3 + family_positive + (1 if has_playground else 0) - family_negative))

        entertainment_positive = sum(
            1
            for kw in [
                "pool",
                "havuz",
                "spa",
                "gym",
                "fitness",
                "entertainment",
                "activity",
                "etkinlik",
                "animasyon",
                "kids club",
            ]
            if kw in all_text
        )
        entertainment_negative = sum(1 for kw in ["sıkıcı", "boring", "hiç etkinlik", "no activities", "kapalı", "closed"] if kw in all_text)
        entertainment_score = max(1, min(5, 3 + entertainment_positive - entertainment_negative))

        room_positive = sum(
            1
            for kw in [
                "rahat",
                "comfortable",
                "konfor",
                "yatak",
                "bed",
                "temiz yatak",
                "spacious",
                "ferah",
            ]
            if kw in all_text
        )
        room_negative = sum(1 for kw in ["rahatsız", "uncomfortable", "yatak rahatsız", "küçük", "small", "sıcak", "cold"] if kw in all_text)
        room_comfort_score = max(1, min(5, 3 + room_positive - room_negative))

        value_positive = sum(1 for kw in ["fiyat", "price", "uygun", "affordable", "value", "değer", "good value"] if kw in all_text)
        value_negative = sum(1 for kw in ["pahalı", "expensive", "overpriced", "para etmiyor", "not worth"] if kw in all_text)
        value_for_money_score = max(1, min(5, 3 + value_positive - value_negative))
        
        # Kullanıcı tercihleriyle ağırlıklandırma
        if isinstance(preferences, dict):
            priority = str(preferences.get("priority") or "")
            non_negotiable = str(preferences.get("non_negotiable") or "")
            travel_style = str(preferences.get("travel_style") or "")

            if "Uyku" in priority:
                quietness_score = min(5, quietness_score + 1)
            if "Eğlence" in priority:
                entertainment_score = min(5, entertainment_score + 1)
            if "Temizlik" in non_negotiable:
                cleaning_score = min(5, cleaning_score + 1)
            if "Çocuk" in non_negotiable or "Aile" in travel_style:
                family_friendly_score = min(5, family_friendly_score + 1)

        # Pros ve Cons çıkar
        pros = []
        cons = []
        
        # Olumlu özellikler
        if "temiz" in all_text or "clean" in all_text:
            pros.append("Temizlik konusunda olumlu")
        if "personel" in all_text or "staff" in all_text:
            pros.append("Personel ilgili ve yardımsever")
        if "konum" in all_text or "location" in all_text or "merkez" in all_text:
            pros.append("İyi konum")
        if "fiyat" in all_text or "price" in all_text or "uygun" in all_text:
            pros.append("Fiyat/performans uygun")
        if has_playground:
            pros.append("Çocuklar için oyun alanı mevcut")
        if "kahvaltı" in all_text or "breakfast" in all_text:
            pros.append("Kahvalti iyi")
        
        # Olumsuz özellikler
        if "kirli" in all_text or "dirty" in all_text:
            cons.append("Temizlik sorunları var")
        if "gürültü" in all_text or "noise" in all_text or "loud" in all_text:
            cons.append("Gürültü problemi")
        if "personel" in all_text and ("kaba" in all_text or "ilgisiz" in all_text):
            cons.append("Personel ilgisiz")
        if "yatak" in all_text and ("rahat değil" in all_text or "uncomfortable" in all_text):
            cons.append("Yataklar rahat değil")
        if "wifi" in all_text and ("yavaş" in all_text or "slow" in all_text or "çalışmıyor" in all_text):
            cons.append("WiFi sorunları")
        
        # Eğer pros/cons boşsa varsayılan değerler ekle
        if not pros:
            pros = ["Genel olarak olumlu yorumlar"]
        if not cons:
            cons = ["Belirgin olumsuzluk yok"]
        
        return {
            "cleaning_score": cleaning_score,
            "has_playground": has_playground,
            "quietness_score": quietness_score,
            "service_score": service_score,
            "location_score": location_score,
            "wifi_score": wifi_score,
            "breakfast_score": breakfast_score,
            "family_friendly_score": family_friendly_score,
            "entertainment_score": entertainment_score,
            "room_comfort_score": room_comfort_score,
            "value_for_money_score": value_for_money_score,
            "pros": pros,
            "cons": cons,
        }

    def _validate_score(self, value: Any) -> int:
        """Skor değerini 1-5 arasına validate et."""
        try:
            score = int(value)
            return max(1, min(5, score))
        except (ValueError, TypeError):
            return 3  # Varsayılan orta değer

    def _validate_list(self, value: Any) -> list[str]:
        """Liste değerini validate et."""
        if isinstance(value, list):
            return [str(item) for item in value if item]
        return []


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_hotel_analysis_service(api_key: str | None = None) -> HotelAnalysisService:
    """
    Factory function - HotelAnalysisService örneği oluşturur.

    Args:
        api_key: Google Gemini API key (None ise mock mod çalışır)

    Returns:
        HotelAnalysisService instance
    """
    return HotelAnalysisService(api_key=api_key)
