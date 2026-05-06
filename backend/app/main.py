from fastapi import FastAPI

from app.models.schemas import HealthResponse
from app.routers.engagement_routes import router as engagement_router
from app.routers.hotels_routes import router as hotels_router
from app.routers.vibe_map_routes import router as vibe_map_router

app = FastAPI(
    title="VibeCheck API",
    description="Functional MVP API scaffold for VibeCheck Travel.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="vibecheck-api")


app.include_router(hotels_router)
app.include_router(vibe_map_router)
app.include_router(engagement_router)
