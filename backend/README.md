# LLM Video Analysis - Backend

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your configuration

# Run development server
python main.py
# Or with uvicorn directly:
uvicorn app.main:app --reload
```

## Server

- **Development**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **OpenAPI**: http://localhost:8000/openapi.json

## Environment Variables

Required settings in `.env`:
- `SECRET_KEY` - JWT secret key (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- `GEMINI_API_KEY` - Google Gemini API key (from https://ai.google.dev)
- `CORS_ALLOWED_ORIGINS` - Allowed frontend URLs

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login with username/password

### Analysis
- `POST /api/analysis/analyze` - Analyze video or image file

### Health
- `GET /health` - Health check status

## Project Structure

```
backend/
  app/
    api/               # Route handlers
      auth_routes.py
      analysis_routes.py
      health_routes.py
    core/              # Core configuration
      config/
        settings.py    # Application settings
      security/
        jwt_manager.py # JWT token management
        password.py    # Password hashing
    exceptions/        # Exception classes
    schemas/           # Pydantic request/response schemas
    services/          # Business logic
      authentication_service.py
      video_analysis_service.py
    utils/             # Utility functions
      file_validator.py
      logging_config.py
    models/            # Data models (optional)
    repository/        # Data access layer (optional)
    main.py            # FastAPI app initialization
  main.py              # Entry point
  requirements.txt     # Dependencies
  .env.example         # Environment variables template
```

## Architecture

Following SOLID principles and clean architecture patterns:

- **Layered Architecture**: Separation of concerns with distinct layers
- **Service Layer Pattern**: Business logic isolated from HTTP handlers
- **Dependency Injection**: Services receive dependencies via constructor
- **Repository Pattern**: Data access abstraction
- **Exception Handling**: Standardized error codes and messages
- **Security**: JWT authentication, password hashing, secret management

## Code Standards

- **Python**: PEP 8 compliance with Black formatter
- **Type Hints**: Full type annotations on all functions
- **Docstrings**: Module, class, and function docstrings
- **Error Handling**: Custom exceptions with structured error responses
- **Logging**: Structured logging with context

## Development

### Format Code
```bash
black app/ --line-length 88
```

### Lint Code
```bash
flake8 app/ --max-line-length=88
isort app/
```

### Type Checking
```bash
mypy app/
```

## Security

- Secrets stored in environment variables (.env)
- JWT tokens with configurable expiration
- Password hashing with bcrypt
- CORS middleware for frontend integration
- Rate limiting on API endpoints
- Input validation on all endpoints
- No hardcoded credentials

## Deployment

See backend `.env.example` for production configuration.

For Google Cloud Run or other platforms, ensure:
1. `SECRET_KEY` is set to a strong random value
2. `GEMINI_API_KEY` is configured
3. `CORS_ALLOWED_ORIGINS` includes your frontend URL
4. Environment is set to `production`
