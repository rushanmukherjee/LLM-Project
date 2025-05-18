# Smart Grocery Assistant

An AI-powered grocery list manager that helps you keep track of your essential items and sends timely reminders.

## Features

- Create and manage multiple grocery lists
- Set reminders for essential items
- Smart suggestions based on your shopping patterns
- User authentication and personal lists
- Responsive web interface

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the frontend development server:
```bash
npm start
```

The application will be available at http://localhost:3000

## Tech Stack

- Backend: FastAPI (Python)
- Frontend: React with TypeScript
- Database: SQLite
- Authentication: JWT
- Scheduling: APScheduler 