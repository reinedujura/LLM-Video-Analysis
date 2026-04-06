# LLM-video-analysis - Getting Started

Welcome! This folder contains a video analysis application powered by Google Gemini AI with a React frontend and FastAPI backend.

## 📁 What's Inside

```
LLM-video-analysis/
├── backend/              # FastAPI backend
├── frontend/             # React frontend
├── README.md             # Complete project documentation
└── .gitignore           # Git ignore rules
```

## 🚀 Quick Start (5 minutes)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Add your Gemini API key in .env
# GEMINI_API_KEY=your_key_here
# SECRET_KEY=your_secret_key

# Run the server
python main.py
```

Server runs at: http://localhost:8000

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local

# Run development server
npm run dev
```

Frontend runs at: http://localhost:5173

### 3. Try It Out

1. Go to http://localhost:5173
2. Login with: `demo_user` / `demo_password`
3. Upload a video or image
4. Select analysis type (comprehensive, bullets, etc.)
5. Click "Analyze Media"
6. See AI-powered analysis results!

## 📚 Documentation

- **[README.md](README.md)** - Full project overview
- **[backend/README.md](backend/README.md)** - Backend setup & docs
- **[frontend/README.md](frontend/README.md)** - Frontend setup & docs

## 🏗️ Architecture Highlights

### Clean Layered Architecture
```
Frontend (React)
    ↓
API Routes (FastAPI)
    ↓
Services (Business Logic)
    ↓
Repository/Utils (Data Access)
```

### Key Features

✅ **Layered Architecture** - Clean separation of concerns (routes → services → utilities)
✅ **SOLID Principles** - Single responsibility, open/closed principle
✅ **Security Standards** - Secrets management, bcrypt password hashing, JWT authentication
✅ **Error Handling** - Standardized error codes and messages
✅ **Type Safety** - Full type hints, Pydantic validation
✅ **Configuration** - Environment-based configuration, no hardcoded values
✅ **Logging** - Structured logging with context
✅ **Code Quality** - Black, ESLint, PEP 8 compliance

## 🔑 Environment Variables

### Backend (.env)
```
SECRET_KEY=your_random_secret_key
GEMINI_API_KEY=your_api_key
DEBUG=False
```

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000
```

See `.env.example` files for all options.

## 📊 Project Structure

### Backend
```
app/
  api/              # Route handlers
  core/             # Config & security
  services/         # Business logic
  schemas/          # Request/response models
  exceptions/       # Custom exceptions
  utils/            # Helper functions
```

### Frontend
```
src/
  components/       # React components
  context/          # State (Auth)
  hooks/            # Custom hooks
  services/         # API calls
  utils/            # Validation, helpers
  styles/           # CSS
```

## 🚢 First Deployment

### Prerequisites
- Google Gemini API key (free)
- Strong `SECRET_KEY` (generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

### Steps
1. Set all environment variables
2. Backend: `python main.py` or deploy to Cloud Run
3. Frontend: `npm run build` and deploy `dist/` to Vercel/Netlify
4. Update `CORS_ALLOWED_ORIGINS` in backend

## 🧪 Testing

The application is ready for comprehensive testing:

**Backend Tests**:
```bash
cd backend
pytest tests/
```

**Frontend Tests**:
```bash
cd frontend
npm test
```

(Test files not included - add with your testing framework)

## 📖 Architecture & Design

This application follows professional software engineering practices including:

- Clean layered architecture (routes → services → utilities)
- Dependency injection and service layer pattern
- Comprehensive error handling with standardized codes
- Environment-based configuration management
- Security best practices (password hashing, JWT tokens, CORS)
- Type safety with type hints and validation
- Structured logging throughout

## 🐛 Troubleshooting

### Backend won't start
- Check Python 3.10+ installed: `python --version`
- Check virtual environment activated
- Check requirements installed: `pip install -r requirements.txt`
- Check .env file exists and has GEMINI_API_KEY

### Frontend won't connect to backend
- Check backend is running on http://localhost:8000
- Check frontend .env.local has correct VITE_API_URL
- Check browser console for CORS errors

### Login fails
- Demo user: `demo_user` / `demo_password`
- Check backend logs for errors
- Ensure SECRET_KEY is set in .env

## 📝 Code Example

### Adding a New Feature

1. **Define request/response** in `backend/app/schemas/`:
```python
class NewFeatureRequest(BaseModel):
    param: str
```

2. **Create service** in `backend/app/services/`:
```python
class NewFeatureService:
    async def process(self, param: str) -> str:
        # Business logic
```

3. **Add route** in `backend/app/api/`:
```python
@router.post("/api/feature")
async def endpoint(request: NewFeatureRequest):
    service = NewFeatureService()
    return await service.process(request.param)
```

4. **Call from frontend**:
```javascript
const response = await ApiService.request("/api/feature", {
  method: "POST",
  body: JSON.stringify({ param: value }),
});
```

## 🤝 Contributing

When making changes:
1. Follow the existing code style (ESLint + Prettier)
2. Add type hints and docstrings
3. Keep error handling consistent
4. Update documentation
5. No secrets in commits

## 📞 Support

- Backend issues → Check `backend/README.md`
- Frontend issues → Check `frontend/README.md`
- API questions → Check http://localhost:8000/docs
- Standards → Check original `STANDARDS/` folder

## ✨ Next Steps

1. **Try the app** - Login and analyze a video
2. **Read the code** - Understand the architecture
3. **Explore standards** - Review STANDARDS folder
4. **Add tests** - Implement unit/integration tests
5. **Deploy** - Take it to production safely

---

**Happy coding!** 🎉

This application demonstrates professional software engineering practices and is ready for academic study, production deployment, or further enhancement.
