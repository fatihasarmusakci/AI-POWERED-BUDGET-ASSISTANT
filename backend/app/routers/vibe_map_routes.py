from fastapi import APIRouter, Query

from app.models.schemas import MapPin, VibeMapResponse

router = APIRouter(prefix="/vibe-map", tags=["vibe-map"])


@router.get("", response_model=VibeMapResponse)
def get_vibe_map(
    city: str = Query(default="london"),
    layers: list[str] = Query(default=["quiet", "metro"]),
) -> VibeMapResponse:
    pins = [
        MapPin(id="pin-1", label="Soho Focus Cafe", layers=["quiet", "metro"]),
        MapPin(id="pin-2", label="Camden Night Strip", layers=["party", "metro"]),
        MapPin(id="pin-3", label="Canary Wharf Work Lounge", layers=["quiet"]),
    ]
    filtered_pins = [pin for pin in pins if any(layer in pin.layers for layer in layers)]
    return VibeMapResponse(city=city, layers=layers, pins=filtered_pins)
