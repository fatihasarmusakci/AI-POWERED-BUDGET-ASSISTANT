# VibeCheck Travel MVP Prototype

Mobile-first React prototype for validating trust-based hotel decisions and retention loops in the London pilot.

## Included Flows
- Persona Engine (3-step onboarding).
- Truth Dashboard (50/50 official vs user photo compare + date labels).
- AI TL;DR, Smart-Score, and Honesty red-flag mock outputs.
- Interactive Vibe-Map layers (quiet, party, metro).
- Retention loops: Vibe-Check Game, Daily Insight, Staycation mode.
- Prototype analytics snapshot with Time-to-Action measurement.

## Run Locally
```bash
npm install
npm run dev
```

## Data Source Switching (Mock -> Live)
- Default mode is mock data for fast UI iteration.
- Create `.env` from `.env.example`.
- Use `VITE_DATA_SOURCE=live` to fetch backend data.
- Set `VITE_API_BASE_URL` to your FastAPI base URL.

## Build and Lint
```bash
npm run build
npm run lint
```

## Documentation
- `docs/mvp-scope.md`: scope lock and exclusions.
- `docs/design-system-wireflow.md`: design tokens and wireflow.
- `docs/retention-flows.md`: hook/retention behavior.
- `docs/usability-test-report.md`: two-round validation outcomes.
- `docs/functional-mvp-handoff.md`: next-phase service/API handoff.
