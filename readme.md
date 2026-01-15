# Resume Job Match Engine

## Setup
1. Backend: `pip install -r requirements.txt && uvicorn app.main:app --reload`
2. Frontend: `npm install && npm start`

## API Endpoints
- `POST /resume/parse` - Parse resume PDF
- `POST /jobs/parse` - Parse job descriptions
- `POST /match` - Match resume against jobs