from __future__ import annotations

from typing import Any

from app.schemas.api import PersonaWeights


def _coerce_weights(persona_data: dict[str, Any]) -> dict[str, float]:
    if not isinstance(persona_data, dict):
        persona_data = {}
    raw_weights = persona_data.get("weights")
    if isinstance(raw_weights, dict):
        defaults = PersonaWeights().model_dump()
        merged_in: dict[str, float] = {**defaults}
        for key in ("temizlik", "sessizlik", "hizmet", "konum"):
            if key in raw_weights:
                merged_in[key] = float(raw_weights[key])
        merged = PersonaWeights.model_validate(merged_in).model_dump()
    else:
        titizlik = float(persona_data.get("titizlik") or 0.5)
        quiet_pref = float(persona_data.get("sessizlik_tercihi") or 0.0)
        if quiet_pref >= 0.5:
            sessiz = 0.6
            rest = 0.4
        else:
            sessiz = 0.25 + 0.35 * quiet_pref
            rest = max(0.05, 1.0 - sessiz)
        temiz = rest * (0.35 + 0.25 * titizlik)
        hizmet = rest * 0.35
        konum = max(0.0, rest - temiz - hizmet)
        merged = {"temizlik": temiz, "sessizlik": sessiz, "hizmet": hizmet, "konum": konum}
    total = sum(merged.values())
    if total <= 0:
        merged = PersonaWeights().model_dump()
        total = sum(merged.values())
    return {k: merged[k] / total for k in ("temizlik", "sessizlik", "hizmet", "konum")}


def average_category_scores(analyses: list[dict[str, Any]]) -> dict[str, float]:
    keys = ("temizlik_skoru", "sessizlik_skoru", "hizmet_skoru", "konum_skoru")
    acc = {k: 0.0 for k in keys}
    n = 0
    for row in analyses:
        if not row:
            continue
        n += 1
        for k in keys:
            v = row.get(k)
            if isinstance(v, (int, float)):
                acc[k] += float(v)
    if n == 0:
        return {k: 5.0 for k in keys}
    return {k: acc[k] / n for k in keys}


def compute_smart_score_value(
    persona_data: dict[str, Any],
    category_averages: dict[str, float],
) -> tuple[float, dict[str, Any]]:
    weights = _coerce_weights(persona_data)
    temiz = category_averages["temizlik_skoru"]
    sessiz = category_averages["sessizlik_skoru"]
    hizmet = category_averages["hizmet_skoru"]
    konum = category_averages["konum_skoru"]
    gurultu_skoru = 11.0 - sessiz

    weighted = (
        weights["temizlik"] * temiz
        + weights["sessizlik"] * sessiz
        + weights["hizmet"] * hizmet
        + weights["konum"] * konum
    )
    score_value = round(max(1.0, min(10.0, weighted)), 2)
    breakdown = {
        "temizlik_skoru": round(temiz, 2),
        "gurultu_skoru": round(gurultu_skoru, 2),
        "hizmet_skoru": round(hizmet, 2),
        "konum_skoru": round(konum, 2),
        "weights_used": weights,
    }
    return score_value, breakdown


def derive_persona_label(persona_data: dict[str, Any]) -> str:
    w = _coerce_weights(persona_data)
    dominant = max(w, key=lambda k: w[k])
    if dominant == "sessizlik" and w["sessizlik"] >= 0.45:
        return "quiet_seeker"
    if dominant == "temizlik" and w["temizlik"] >= 0.35:
        return "meticulous_guest"
    return "balanced_traveler"
