# VibeCheck Backend (Functional MVP Scaffold)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run API
```bash
uvicorn app.main:app --reload
```

## Run Tests
```bash
pytest
```

## Implemented Endpoints
- `GET /health`
- `GET /hotels?city=london`
- `GET /hotels/{hotel_id}/truth`
- `GET /hotels/{hotel_id}/summary`
- `GET /vibe-map?city=london&layers=quiet&layers=metro`
- `POST /game/guess`
- `GET /insights/daily?city=london`
- `POST /staycation/rating`
