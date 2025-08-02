import uvicorn
import os

HOST = os.getenv("API_HOST", "127.0.0.1")
PORT = int(os.getenv("API_PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("views.api:app", host=HOST, port=PORT, reload=True)
