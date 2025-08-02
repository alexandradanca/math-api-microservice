from fastapi import FastAPI, HTTPException, Request, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from functools import lru_cache
import logging
from utils import setup_logging
from pydantic import BaseModel
from controllers.math_controller import MathController
from services.worker import MathWorker



setup_logging()
logger = logging.getLogger("mathapi")


app = FastAPI()
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")
app.mount("/img", StaticFiles(directory="frontend/img"), name="img")
import sys
print("\nTest live API: http://127.0.0.1:8000\n", file=sys.stderr)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "secret123"  # Change for production
def api_key_auth(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        logger.warning("Unauthorized access attempt.")
        raise HTTPException(status_code=401, detail="Invalid API Key")

controller = MathController()
worker = MathWorker()

# Serve static frontend
import os
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')

app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

# Serve favicon.ico
@app.get("/favicon.ico")
def favicon():
    return FileResponse(os.path.join(frontend_path, "favicon.ico"))

@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

class PowRequest(BaseModel):
    base: float
    exp: float

class NRequest(BaseModel):
    n: int


@lru_cache(maxsize=128)
def cached_pow(base, exp):
    return controller.process_request('pow', {'base': base, 'exp': exp}).result

@app.post("/pow")
def pow_endpoint(req: PowRequest, async_task: bool = False, x_api_key: str = Depends(api_key_auth)):
    logger.info(f"/pow called: {req.dict()} async={async_task}")
    if async_task:
        worker.add_task('pow', req.dict())
        return {"message": "Task added to background queue."}
    result = cached_pow(req.base, req.exp)
    return {"result": result}


@lru_cache(maxsize=128)
def cached_fibonacci(n):
    return controller.process_request('fibonacci', {'n': n}).result

@app.post("/fibonacci")
def fibonacci_endpoint(req: NRequest, async_task: bool = False, x_api_key: str = Depends(api_key_auth)):
    logger.info(f"/fibonacci called: {req.dict()} async={async_task}")
    if async_task:
        worker.add_task('fibonacci', req.dict())
        return {"message": "Task added to background queue."}
    result = cached_fibonacci(req.n)
    return {"result": result}


@lru_cache(maxsize=128)
def cached_factorial(n):
    return controller.process_request('factorial', {'n': n}).result

@app.post("/factorial")
def factorial_endpoint(req: NRequest, async_task: bool = False, x_api_key: str = Depends(api_key_auth)):
    logger.info(f"/factorial called: {req.dict()} async={async_task}")
    if async_task:
        worker.add_task('factorial', req.dict())
        return {"message": "Task added to background queue."}
    result = cached_factorial(req.n)
    return {"result": result}


@app.get("/history")
def history(x_api_key: str = Depends(api_key_auth)):
    logger.info("/history called")
    return controller.get_history()


@app.get("/results")
def results(x_api_key: str = Depends(api_key_auth)):
    logger.info("/results called")
    return [str(r) for r in worker.get_results()]

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
