# flask-docker-setup

## Environment setup

1. Copy `.env.example` to `.env` (or create `.env`) and provide the values described below.
2. Build and run the project with Docker:
   ```bash
   docker-compose up --build
   ```

### Environment variables

- `SECRET_KEY` – Flask secret key used for signing session data. Defaults to `dev-secret-key`.
- `JWT_SECRET_KEY` – Secret used to sign JWT access tokens. Defaults to `SECRET_KEY` when not provided.
- `JWT_EXPIRATION_MINUTES` – Lifetime of generated JWTs in minutes. Defaults to `60`.
- `DATABASE_URI` – SQLAlchemy connection string. Defaults to `sqlite:///app.db`. For MySQL use a URI such as `mysql+mysqldb://user:password@db:3306/database_name`.

## Authentication API

- `POST /auth/signup`  
  Request body: `{"email": "user@example.com", "password": "securePassw0rd"}`  
  Registers a new user, storing a hashed password and returns a JWT access token.

- `POST /auth/login`  
  Request body: `{"email": "user@example.com", "password": "securePassw0rd"}`  
  Authenticates the user, updates `last_login_at`, and returns a JWT access token.
