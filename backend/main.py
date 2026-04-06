# Backend root entry point
# Run: python -m uvicorn app.main:app --reload

import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
