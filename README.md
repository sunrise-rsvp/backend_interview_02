# Backend Interview 02 - FastAPI Events API

A simplified FastAPI-based interview project for managing events with CRUD operations. This project follows a clean architecture pattern with repository-based data access and query separation, but without the complexity of command handlers and message buses.

## 🚀 Features

- **FastAPI** with async/await support
- **PostgreSQL** database with SQLAlchemy ORM
- **Alembic** database migrations
- **Docker Compose** for easy local development
- **Rate limiting** with slowapi
- **CORS** support for frontend integration
- **Pydantic** models for request/response validation
- **Soft delete** pattern for data safety

## 🏗️ Architecture

This project uses a simplified CQRS-like pattern:
- **Repository Pattern**: For create, update, delete operations
- **Query Pattern**: For all read operations  
- **Separation of Concerns**: Clear separation between inputs, outputs, and business logic
- **No Command Handlers**: Direct repository/query usage in views for simplicity

## 📋 Prerequisites

- **Docker & Docker Compose**

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd backend_interview_02
```

### 2. Start the Application (Docker Compose - Recommended)
```bash
# Start all services (database + API)
docker-compose up -d

# The API will be available at http://localhost:8003
```

That's it! Docker Compose handles everything including:
- PostgreSQL database setup
- Python environment and dependencies
- Database migrations
- FastAPI server startup

### Alternative: Local Development Setup
*Only needed if you want to run the API locally outside Docker*

#### Prerequisites for Local Development
- **Python 3.10+**

#### Setup Steps
```bash
# 1. Set up Python Virtual Environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# 2. Environment Configuration
cp .env.local .env

# 3. Start Database Only
docker-compose up -d interview-db

# 4. Run Database Migrations
alembic upgrade head

# 5. Start the API Server
uvicorn main:app --host 0.0.0.0 --port 8600 --reload
```

## 📋 Interview Tasks (Todo)

Here are the tasks to implement:

### 🟢 Task 1: Event Count Endpoint
**Goal**: Add a simple endpoint to get the total count of active events.
- Create `GET /events/count/` endpoint
- Return JSON: `{"count": 42}`

### 🟡 Task 2: Date Range Filtering
**Goal**: Add date range filtering to the events list endpoint.
- Extend `GET /events/` with `start_after` and `end_before` query parameters
- Filter events where `start_date >= start_after` and `end_date <= end_before`

### 🟡 Task 3: Event Categories
**Goal**: Add a category system for events.
- Create `Category` model (id, name, description)
- Add `category_id` foreign key to Event model
- Create category CRUD endpoints
- Include category data in event responses
- Add database migration

### 🔴 Task 4: Event Attendees
**Goal**: Add attendee management with many-to-many relationships.
- Create `Attendee` model (id, name, email, phone)
- Create `EventAttendee` join table with registration_date
- Add attendee management endpoints
- Implement attendee limits per event
- Add validation for email uniqueness per event

### 🔴 Task 5: Background Tasks & Notifications
**Goal**: Add asynchronous email notifications for event changes.
- Install Celery for background tasks
- Create email notification system
- Send notifications when events are created/updated/cancelled
- Add Redis for task queue
- Implement retry logic for failed notifications

### 🔴 Task 6: Caching & Performance
**Goal**: Add caching layer for improved performance.
- Install Redis for caching
- Cache event list responses for 5 minutes
- Cache individual event details for 10 minutes
- Implement cache invalidation on updates
- Add cache hit/miss metrics

## 🐳 Docker Usage

### Full Docker Setup
```bash
# Start all services (database + API)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Database Only
```bash
# Start only the database
docker-compose up -d interview-db
```
