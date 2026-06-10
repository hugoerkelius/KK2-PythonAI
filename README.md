# KK2 - One Piece TCG Bot

FastAPI-applikation som svarar på frågor om One Piece Trading Card Game med hjälp av en LLM och kortdata från OPTCG API.

## Krav

- Python 3.14+
- uv
- HuggingFace-token (gratis på https://huggingface.co/settings/tokens)

## Installation

```bash
uv sync
```

Skapa en `.env`-fil i projektets rot:
HF_TOKEN=din_token_här
MODEL_ID=HuggingFaceTB/SmolLM2-1.7B-Instruct
MAX_NEW_TOKENS=200
MAX_UPLOAD_BYTES=10485760

## Användning

Starta servern:
```bash
uv run uvicorn app.main:app --reload
```

Ladda kortdata:
```bash
# Från OPTCG API
curl http://localhost:8000/data/load_api

# Från lokal CSV
curl -X POST http://localhost:8000/data/upload -F "file=@data/cards.csv"
```

Ställ en fråga:
```bash
curl -X POST http://localhost:8000/ai/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Vilket kort är dyrast?\"}"
```

## Spara data lokalt

Kör en gång för att spara kortdata till disk utan att servern behöver köra:
```bash
uv run python -m app.data.data
```

## Tester

```bash
uv run pytest app/tests/ -v
```

## Endpoints

| Method | Endpoint | Beskrivning |
|---|---|---|
| GET | /health | Hälsokontroll |
| GET | /data/load_api | Ladda data från OPTCG API |
| POST | /data/upload | Ladda upp CSV-fil |
| GET | /data/stats | Statistik om laddad data |
| POST | /ai/ask | Ställ en fråga om kortdata |