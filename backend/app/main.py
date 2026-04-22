from fastapi import FastAPI

app = FastAPI(
    title="AI Travel Buddy API",
    description="Seyahat kararlarını kolaylaştıran AI asistanı",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "AI-Travel Buddy API is active! ✈️",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fastapi"}