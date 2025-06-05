# Competitor Insights Assistant

## Overview
AI-powered business profile comparison tool for restaurants and local businesses.

## Technology Stack
- **Backend:** Django 5.2+ + Django REST Framework
- **Frontend:** Vue 3 + Vite + TypeScript
- **Styling:** Tailwind CSS + PrimeVue
- **Database:** SQLite for development

## Features
- User Input:
  - Business name or website URL
  - Style of AI-powered report
- Comparison Report:
  - Comparison of business profile data
  - AI-powered analysis
  - Visualization of comparison results

**Note:** Now the competitor business data is not fetched from the external API. Instead, example data is used (`/backend/providers/mock_data.json`).
User's business data is mock data generated randomly.

## Quick Start

### Option 1: Docker Compose

```bash
docker-compose up --build
```

Visit http://localhost:5173

### Option 2: Manual Setup

1. backend

```bash
cd backend

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

2. frontend

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173

## API Endpoints

- `POST /api/v1/comparisons/` - Generate comparison report

## Skipped Features
- **External APIs (Serper.dev etc.):** Due to cost and time limits, mock data is used instead
- **Nearby/Similar business selection:** Requires external API integration
- **No of Image metrics:** Not available in current data sources

## Future Improvements
- **Performance:** Add Redis + Celery for async tasks (e.g., report generation)
- **AI integration:** Improve AI prompts for better analysis
- **UI/UX:** Better visualizations and user interface
- **Real business search:** Integrate with Google Places or similar APIs
- **Better business profile data presentation:** More comprehensive, accurate and detailed business profile data presentation, which will be helpful for AI analysis
