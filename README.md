# AI Tutor Training Platform

An AI-powered platform for training high school tutors through practice sessions with simulated student personas.

https://ai-learner-simulation-production.up.railway.app/

## Tech Stack

- **Frontend**: React 19 + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python 3.9+
- **AI**: Claude Haiku (conversations) + Claude Sonnet (scoring)
- **Deployment**: Railway

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+

### Backend Setup

1. Create a virtual environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

4. Run the backend:

```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Run the development server:

```bash
npm run dev
```

The application will be available at http://localhost:3000

## Project Structure

```
ai-learner-simulation/
├── frontend/           # React application
├── backend/           # FastAPI server
├── static/            # Production build output
└── railway.toml       # Deployment configuration
```

## API Endpoints

- `POST /api/sessions/start` - Start a new tutoring session
- `POST /api/sessions/{id}/message` - Send a message in a session
- `POST /api/sessions/{id}/end` - End a session and get scoring
- `GET /api/users/{name}/progress` - Get user progress data

## Deployment

The application is configured for Railway deployment. Push to your repository and Railway will automatically build and deploy.
