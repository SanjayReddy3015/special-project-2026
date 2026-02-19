import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import community

# --- Advanced Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("WikiKisan")

# --- FastAPI Initialization ---
app = FastAPI(
    title="WikiKisan Advanced API",
    description="Scalable backend for the AI-powered WikiKisan Farmer platform.",
    version="2.0.0",
    docs_url="/api/docs",  # Custom docs URL
    redoc_url="/api/redoc"
)

# --- Middleware: Performance Logging ---
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Path: {request.url.path} | Time: {process_time:.4f}s")
    return response

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "An internal server error occurred."},
    )

# --- Router Integration ---
app.include_router(
    community.router, 
    prefix="/api/v1/community", 
    tags=["Community"]
)

# --- Health Check Endpoints ---
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": "development",
        "version": app.version
    }

if __name__ == "__main__":
    import uvicorn
    # Optimized for development with auto-reload
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
