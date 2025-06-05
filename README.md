# Competitor Insights Assistant

## Overview
AI-powered business profile comparison tool for restaurants and local businesses.

## Technology Stack
- **Backend:** Django 5.2+ + Django REST Framework
- **Frontend:** Vue 3 + Vite + TypeScript
- **Styling:** Tailwind CSS + PrimeVue
- **Database:** SQLite for development

## MVP Scope
- Business profile input interface
- AI-powered recommendations
- Basic comparison visualization

## Architecture
- **Backend:** Django REST API handling business logic and AI integration
- **Frontend:** Vue.js SPA providing user interface and data visualization

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

## Skipped Features
- **External APIs (Serper.dev etc.):** Due to cost and time limits, it was not used in the MVP. Currently,
the example data uses the same structure as the Serper.dev API response.

- **Nearby or similar business selection:** Skipped due to extternal API integration is not implemented yet and time constraints.

- **Number of images metrics missing:** This metric is not available in the Serper.dev API response data. Maybe some other data source can be used to get this metric. Now mock data is used.

## Future Improvements
- **Performance:** Add Redis + Celery for asynchronous task handling and caching.
- **AI integration:** Improve AI prompt for better analysis.
- **UI/UX:** Improve user interface and report visualization.
- **Business Search:** Add real business search functionality.
- **Better business profile data presentation:** More comprehensive, accurate and detailed business profile data presentation, which will be helpful for AI analysis.
