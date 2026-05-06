# Functional MVP Handoff Pack

## Proposed Service Split
- `ingest-service`: Booking/Places data pulls and normalization.
- `scoring-service`: semantic signal extraction and score normalization (1-10).
- `summary-service`: GPT-4o-mini weekly hotel summaries with cache.
- `profile-service`: persona preferences and privacy-safe session context.
- `moderation-service`: red-flag heuristics for same-IP and text similarity.

## API Contract Draft (High-Level)
- `GET /hotels?city=london`: list with Smart Score, district tags, retention hints.
- `GET /hotels/:id/truth`: official vs user media metadata + date deltas.
- `GET /hotels/:id/summary`: cached TL;DR + review sample count.
- `GET /vibe-map?city=london&layers=quiet,metro`: map overlays.
- `POST /game/guess`: user game label for real/manipulated signal.
- `GET /insights/daily?city=london`: daily insight payload.
- `POST /staycation/rating`: coworking/brunch score inputs.

## Data and Privacy Requirements
- Persona data stored as pseudonymous profile IDs.
- GDPR: retention policy, delete endpoint, explicit consent flags.
- Audit fields for derived scores and model prompt versions.

## MVP Backlog (Next Phase)
1. Integrate Booking and Google Places ingestion.
2. Build weekly caching scheduler for hotel summaries.
3. Implement Honesty Filter v1 heuristics and admin red-flag view.
4. Add analytics warehouse pipeline for KPI tracking.
5. Prepare load testing scenario for 5,000 concurrent users.
