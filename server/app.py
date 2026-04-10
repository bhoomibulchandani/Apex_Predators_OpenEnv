import uvicorn
from .environment import app

def main():
    """Entry point for the OpenEnv server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()