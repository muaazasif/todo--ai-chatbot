import os
import sys

# Add the app directory to the Python path so we can import from backend
sys.path.insert(0, '/app')

# Import the app inside the main function to ensure path is set
def main():
    import uvicorn
    from backend.main import app

    port = int(os.environ.get("PORT", 8000))
    print(f"PORT environment variable value: {os.environ.get('PORT')}")
    print(f"Using port: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()