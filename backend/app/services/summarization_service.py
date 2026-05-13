from __future__ import annotations

import json
import logging
from typing import Any, Sequence

from openai import OpenAI

from app.core.config import settings
from app.models.orm import Review

logger = logging.getLogger(__name__)


class SummarizationService:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self._model = model or settings.openai_model
        key = api_key if api_key is not None else settings.openai_api_key
        self._client = OpenAI(api_key=key) if key else None

    def build_three_bullets(self, reviews: Sequence[Review]) -> tuple[list[str], str | None]:
        analyzed = [r for r in reviews if r.sentiment_scores]
        if not analyzed:
            return [
                "Henüz analiz edilmiş yorum yok.",
                "Yorum gönderildiğinde Smart-Scoring ve özet üretilecek.",
                "API: POST /reviews ile yorum ekleyebilirsiniz.",
            ], None

        payload = [
            {
                "text": r.raw_text[:800],
                "scores": {k: r.sentiment_scores.get(k) for k in ("temizlik_skoru", "sessizlik_skoru", "hizmet_skoru", "konum_skoru") if r.sentiment_scores},
                "insights": {k: r.sentiment_scores.get(k) for k in ("temizlik_insight", "sessizlik_insight", "hizmet_insight", "konum_insight") if r.sentiment_scores},
            }
            for r in analyzed[:40]
        ]

        if self._client is None:
            return self._mock_bullets(analyzed), "heuristic"

        try:
            completion = self._client.chat.completions.create(
                model=self._model,
                temperature=0.3,
                messages=[
                    {
                        "role": "system",
                        "content": "Otel yorum özetleyicisisin. Türkçe tam 3 madde, her biri tek cümle, madde işareti yok, JSON: {\"bullets\": [\"...\",\"...\",\"...\"]}",
                    },
                    {"role": "user", "content": json.dumps(payload, ensure_ascii=False)[:14_000]},
                ],
                response_format={"type": "json_object"},
            )
            data = json.loads(completion.choices[0].message.content or "{}")
            bullets = data.get("bullets") or []
            if isinstance(bullets, list) and len(bullets) >= 3:
                return [str(b) for b in bullets[:3]], self._model
        except Exception as exc:  # noqa: BLE001
            logger.warning("OpenAI summarization failed: %s", exc)
        return self._mock_bullets(analyzed), "heuristic"

    def _mock_bullets(self, analyzed: list[Review]) -> list[str]:
        scores: dict[str, list[float]] = {"t": [], "s": [], "h": [], "k": []}
        for r in analyzed:
            s = r.sentiment_scores or {}
            for key, bucket in (
                ("temizlik_skoru", "t"),
                ("sessizlik_skoru", "s"),
                ("hizmet_skoru", "h"),
                ("konum_skoru", "k"),
            ):
                v = s.get(key)
                if isinstance(v, (int, float)):
                    scores[bucket].append(float(v))
        def avg(xs: list[float]) -> float:
            return sum(xs) / len(xs) if xs else 5.0

        return [
            f"Temizlik ortalaması yaklaşık {avg(scores['t']):.1f}/10 — metin içgörülerine göre genel izlenim.",
            f"Sessizlik ortalaması yaklaşık {avg(scores['s']):.1f}/10 — gürültü veya sakinlik vurguları bir arada.",
            f"Hizmet {avg(scores['h']):.1f}/10, konum {avg(scores['k']):.1f}/10; toplam {len(analyzed)} analiz edilmiş yorum kullanıldı.",
        ]
