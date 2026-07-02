# Kọ́mi

Kọ́mi is a full-stack MVP for learning the Yoruba language.

## Project structure

- `backend/` - FastAPI backend
- `frontend/` - React + Vite frontend

## Getting started

### Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```
