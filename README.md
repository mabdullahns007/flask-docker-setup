# Flask Car Data API

A Flask-based RESTful API for managing car data, featuring JWT authentication, background task processing with Celery, and a fully dockerized development environment.

## Features

- **JWT Authentication**: Secure user registration and login.
- **Car Data Management**: CRUD operations for Car Makes, Models, and Years.
- **Pagination**: Built-in pagination for list endpoints.
- **Background Tasks**: Celery integration for handling asynchronous jobs (e.g., data synchronization).
- **Dockerized Architecture**: Simplified setup using Docker and Docker Compose.
- **Database Migrations**: Managed with Flask-Migrate (Alembic).

## Tech Stack

- **Backend**: Flask
- **Database**: MySQL 8.0
- **Task Queue**: Celery with Redis
- **Containerization**: Docker & Docker Compose

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd flaskMigrate
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the root directory (refer to `.env.example` if available, or ensure the following variables are set):
   ```env
   SECRET_KEY=your_secret_key
   DATABASE_URI=mysql+mysqldb://root:rootpassword@db:3306/flaskdb
   REDIS_URL=redis://redis:6379/0
   ```
   *Note: Default MySQL credentials in `docker-compose.yml` are `root` / `rootpassword`.*

3. **Build and Start the Containers**:
   ```bash
   docker-compose up --build
   ```
   This will start the Flask app, MySQL database, Redis, Celery worker, and Celery beat.

4. **Run Database Migrations**:
   Once the containers are running, apply the migrations to set up the database schema:
   ```bash
   docker-compose exec web flask db upgrade
   ```

## API Documentation

### Authentication
- `POST /auth/signup`: Register a new user.
- `POST /auth/login`: Login and receive a JWT access token.

### Car Management
- `GET /cars/makes`: List all car makes (supports `page` and `per_page` query params).
- `POST /cars/makes`: Create a new car make.
- `GET /cars/makes/<id>`: Get details of a specific make.
- `PUT /cars/makes/<id>`: Update a car make.
- `DELETE /cars/makes/<id>`: Delete a car make.

*Similar endpoints exist for Models and Years:*
- `/cars/models`
- `/cars/years`

## Background Tasks

The application uses Celery to handle background tasks. The worker and beat services are automatically started by Docker Compose.

- **Worker**: Processes queued tasks.
- **Beat**: Schedules periodic tasks (configuration in `celery_app.py`).

## Project Structure

```text
├── app/
│   ├── models/          # SQLAlchemy Models
│   ├── routes/          # API Blueprints
│   ├── tasks/           # Celery task definitions
│   └── constants.py     # Application constants
├── migrations/          # Alembic migration files
├── celery_app.py        # Celery initialization
├── docker-compose.yml   # Multi-container setup
└── Dockerfile           # Flask app image definition
```
