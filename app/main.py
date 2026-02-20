import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import community, weather, market
from app.database import connect_to_mongo, close_mongo_connection

# --- Advanced Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("WikiKisan")

# --- Lifespan Management (Startup/Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs before the app starts taking requests
    logger.info("🚀 Starting up WikiKisan Services...")
    await connect_to_mongo()
    yield
    # This code runs when the app is shutting down
    logger.info("🔌 Shutting down WikiKisan Services...")
    await close_mongo_connection()

# --- FastAPI Initialization ---
app = FastAPI(
    title="WikiKisan Advanced API",
    description="Scalable backend for the AI-powered WikiKisan Farmer platform.",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# --- Middleware: Performance Logging ---
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    logger.info(f"Path: {request.url.path} | Method: {request.method} | Time: {process_time:.4f}s")
    return response

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False, 
            "message": "An internal server error occurred.",
            "detail": str(exc) if app.debug else None
        },
    )

# --- Router Integration ---
app.include_router(community.router, prefix="/api/v1/community", tags=["Community"])
app.include_router(weather.router, prefix="/api/v1/weather", tags=["Weather"])
app.include_router(market.router, prefix="/api/v1/market", tags=["Market"])

# --- System Health Check ---
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
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
