from __future__ import annotations

import json
import logging
from typing import Any

from openai import OpenAI

from app.core.config import settings
from app.schemas.api import NLPScoresPayload

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """Sen bir otel yorumu analisti asistanısın. Verilen metni analiz et ve SADECE geçerli bir JSON nesnesi döndür.
Alanlar (tam olarak bu isimlerle, tamsayı 1-10):
- temizlik_skoru, sessizlik_skoru, hizmet_skoru, konum_skoru
- temizlik_insight, sessizlik_insight, hizmet_insight, konum_insight: Türkçe tek kısa cümle (içgörü)
- gorsel_sikayet_negatif: boolean — oda/manzara/fotoğrafla uyuşmayan veya kötü görünüm şikayeti var mı
- gorsel_sikayet_ozeti: string veya null — varsa tek kısa ifade
Başka metin veya markdown kullanma."""


class NLPService:
    """OpenAI tabanlı yorum analizi — DB'den bağımsız."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self._model = model or settings.openai_model
        self._client: OpenAI | None
        key = api_key if api_key is not None else settings.openai_api_key
        self._client = OpenAI(api_key=key) if key else None

    def analyze_review_text(self, raw_text: str) -> dict[str, Any]:
        if self._client is None:
            return self._mock_analysis(raw_text)

        try:
            completion = self._client.chat.completions.create(
                model=self._model,
                temperature=0.2,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Yorum metni:\n{raw_text[:12_000]}",
                    },
                ],
                response_format={"type": "json_object"},
            )
            content = completion.choices[0].message.content or "{}"
            data = json.loads(content)
            payload = NLPScoresPayload.model_validate(data)
            return payload.model_dump()
        except Exception as exc:  # noqa: BLE001
            logger.warning("OpenAI NLP failed, falling back to heuristic: %s", exc)
            return self._mock_analysis(raw_text)

    def _mock_analysis(self, raw_text: str) -> dict[str, Any]:
        text = raw_text.lower()
        noise_hit = any(w in text for w in ("gürültü", "ses", "noise", "thin walls", "thin wall"))
        clean_hit = any(w in text for w in ("temiz", "clean", "kirli", "dirty", "küf"))
        visual_bad = any(
            w in text
            for w in (
                "fotoğraf",
                "photo",
                "görünüm",
                "oda küçük",
                "bathroom mold",
                "küf",
                "penceresiz",
            )
        )
        base = 7
        temizlik = max(1, min(10, base + (2 if "temiz" in text or "clean" in text else (-2 if "kirli" in text else 0))))
        sessizlik = max(1, min(10, base + (-3 if noise_hit else 1)))
        hizmet = max(1, min(10, base + (1 if "personel" in text or "staff" in text else 0)))
        konum = max(1, min(10, base + (1 if "merkez" in text or "central" in text else 0)))
        return {
            "temizlik_skoru": temizlik,
            "sessizlik_skoru": sessizlik,
            "hizmet_skoru": hizmet,
            "konum_skoru": konum,
            "temizlik_insight": "Heuristik: temizlik ipuçları metinden çıkarıldı."
            if clean_hit
            else "Heuristik: belirgin temizlik sinyali yok.",
            "sessizlik_insight": "Heuristik: gürültü veya sessizlik ipuçları değerlendirildi.",
            "hizmet_insight": "Heuristik: hizmete dair genel izlenim.",
            "konum_insight": "Heuristik: konuma dair genel izlenim.",
            "gorsel_sikayet_negatif": bool(visual_bad),
            "gorsel_sikayet_ozeti": "Görsel / oda beklentisi ile ilgili olumsuz ifadeler."
            if visual_bad
            else None,
        }


def extract_negative_visual_flags(sentiment: dict[str, Any] | None) -> bool:
    if not sentiment:
        return False
    if sentiment.get("gorsel_sikayet_negatif") is True:
        return True
    snippet = sentiment.get("gorsel_sikayet_ozeti")
    return isinstance(snippet, str) and len(snippet.strip()) > 0
