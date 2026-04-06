# LLM Video Analysis - Frontend

## Setup

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Run development server
npm run dev
```

## Scripts

- `npm run dev` - Start development server (localhost:5173)
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Environment Variables

Set in `.env.local`:
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)

## Project Structure

```
src/
  components/    # React components
  context/       # React context (auth)
  hooks/         # Custom React hooks
  services/      # API services
  styles/        # CSS styles
  utils/         # Utility functions
  App.jsx        # Main app component
  config.js      # Configuration
  main.jsx       # Entry point
```

## Code Standards

- ESLint configuration in `.eslintrc.json`
- Prettier formatting in `.prettierrc.json`
- React best practices followed
- All components use functional components with hooks
