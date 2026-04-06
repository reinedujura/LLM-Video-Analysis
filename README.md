# LLM Video Analytics

A full-stack application for analyzing videos and images using Google Gemini AI.

## Overview

**LLM Video Analytics** is a modern web application that combines:
- **Backend**: FastAPI with Google Gemini AI integration
- **Frontend**: React with Vite for responsive UI
- **Authentication**: JWT-based user authentication
- **Architecture**: Clean architecture with SOLID principles

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API key (from https://ai.google.dev)

### Backend Setup

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Edit .env and add your GEMINI_API_KEY and SECRET_KEY
python main.py
```

Backend will be available at: http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local

# Development server
npm run dev
```

Frontend will be available at: http://localhost:5173

## Features

### Core Features
- **Video/Image Upload**: Support for MP4, WebM, JPEG, PNG, WebP, GIF
- **AI Analysis**: Multiple analysis types with Gemini AI
  - Comprehensive analysis
  - Bullet-point summary
  - Detailed breakdown
  - Q&A format
  - Transcription (audio extraction)
  - Timecode paragraphs
- **Custom Prompts**: Override default analysis prompts
- **User Authentication**: Secure JWT-based auth
- **Rate Limiting**: Built-in API rate limiting
- **Error Handling**: Standardized error codes and messages

### Architecture & Design

- **SOLID principles** - Clean, maintainable code
- **Service layer pattern** - Separated concerns
- **Dependency injection** - Flexible, testable
- **Type hints** - Predictable Python
- **JWT authentication** - Secure, stateless auth
- **Rate limiting** - Prevent API abuse
- **Structured error handling** - Consistent responses

## Project Structure

```
LLM-video-analysis/
├── backend/
│   ├── app/
│   │   ├── api/              # Route handlers
│   │   ├── core/             # Config, security, auth
│   │   ├── services/         # Business logic
│   │   ├── schemas/          # Request/response validation
│   │   ├── exceptions/       # Custom exceptions
│   │   └── utils/            # Helper utilities
│   ├── main.py               # Entry point
│   ├── requirements.txt       # Dependencies
│   ├── .env.example          # Environment template
│   └── README.md             # Backend docs
│
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── context/          # Auth context
│   │   ├── hooks/            # Custom hooks
│   │   ├── services/         # API services
│   │   ├── styles/           # Global CSS
│   │   ├── utils/            # Utilities
│   │   ├── App.jsx           # Main component
│   │   └── main.jsx          # Entry point
│   ├── index.html            # HTML template
│   ├── package.json          # Dependencies
│   ├── vite.config.js        # Vite configuration
│   ├── .eslintrc.json        # ESLint config
│   ├── .prettierrc.json      # Prettier config
│   └── README.md             # Frontend docs
│
├── README.md                 # This file
└── ARCHITECTURE.md           # Detailed architecture docs
```

## API Documentation

Once the backend is running, view interactive API docs at:
http://localhost:8000/docs

### Key Endpoints

**Authentication**
```
POST /api/auth/login
{
  "username": "demo_user",
  "password": "demo_password"
}
```

**Analysis**
```
POST /api/analysis/analyze
- Requires: Bearer token in Authorization header
- Body: FormData with file and analysis_type
```

## Configuration

### Backend (.env)
- `SECRET_KEY` - JWT secret (required)
- `GEMINI_API_KEY` - Google Gemini API key (required)
- `GEMINI_MODEL` - Model to use (default: gemini-2.5-pro)
- `MAX_FILE_SIZE_BYTES` - Max upload size (default: 200MB)
- `CORS_ALLOWED_ORIGINS` - Frontend URLs
- `DEBUG` - Debug mode (production: False)

### Frontend (.env.local)
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)

## Development

### Code Quality

**Backend**
```bash
cd backend
black app/ --line-length 88
flake8 app/ --max-line-length=88
isort app/
```

**Frontend**
```bash
cd frontend
npm run lint
npm run format
```

### Testing

Backend testing structure is ready for pytest:
```bash
cd backend
pytest tests/
```

Frontend testing structure is ready for Vitest/Jest.

## Deployment

### Prerequisites
- Google Cloud Project (or similar hosting)
- Docker (optional but recommended)
- Environment variables configured

### Backend Deployment
1. Set `ENVIRONMENT=production` in .env
2. Set strong `SECRET_KEY` and other secrets
3. Deploy to Cloud Run, Heroku, or similar

### Frontend Deployment
1. Build: `npm run build`
2. Deploy `dist/` to Vercel, Netlify, or similar

## Demo Credentials

Default demo user for testing:
- **Username**: `demo_user`
- **Password**: `demo_password`

## Technologies

### Backend
- **FastAPI** 0.115.0 - Web framework
- **Google Gemini AI** - AI analysis
- **PyJWT** - JWT authentication
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **slowapi** - Rate limiting

### Frontend
- **React** 18.3.1 - UI framework
- **Vite** 7.3.1 - Build tool
- **ESLint** - Code linting
- **Prettier** - Code formatting

## Error Handling

All API errors follow standardized format:
```json
{
  "success": false,
  "error": {
    "code": 201,
    "message": "Input validation failed",
    "detail": "File size exceeds maximum allowed size of 200MB"
  }
}
```

Error codes:
- 100-199: Authentication errors
- 200-299: Validation errors
- 300-399: Resource errors
- 400-499: Service errors
- 500-599: System errors

## Security Considerations

- Always use environment variables for secrets
- Never commit `.env` files
- Keep API keys secure and rotate regularly
- Use HTTPS in production
- Implement rate limiting (included)
- Validate all inputs (included)
- Use strong JWT secrets
- Enable CORS only for trusted origins

## Contributing

When contributing, ensure:
1. Code follows the established standards
2. Type hints are complete
3. Docstrings are present
4. Tests are included
5. No secrets in commits

## License

MIT License

## Support

For issues or questions:
1. Check the backend README.md
2. Check the frontend README.md
3. Review API documentation at /docs
4. Check STANDARDS folder for technical guidelines

---

**Built with Standards**: This application demonstrates best practices from 22 comprehensive software engineering standards.
