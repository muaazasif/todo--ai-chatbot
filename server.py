import os
import uvicorn
from backend.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"PORT environment variable value: {os.environ.get('PORT')}")
    print(f"Using port: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)