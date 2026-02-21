from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
from app.api.v1 import weather 

from app.utils.logger import get_logger
from app.config import settings

logger = get_logger(__name__)

app = FastAPI(
    title="Kadalvazhi API",
    description="BSmart Fishing Assistant API for Tamil Nadu & Kerala fishermen",
    version="0.1.0",
    debug=settings.debug,
    # WHY docs_url ?
    # - Auto-generated API documentation
    docs_url="/docs" if settings.debug else None, #hide in production
    redoc_url="/redoc" if settings.debug else None,
)

app.include_router(
    weather.router,
    prefix="/api/v1/weather",
    tags=["weather"]
)

logger.info("FastAPI app initialized")

# MIDDLEWARE - CORS (Cross-Origin Resource Sharing)
# WHY THIS IS CRITICAL ?
# Your frontend (localhost:?) needs to call backend (localhost:?)
# Browser blocks this by default (security)
# CORS middleware says "these origins are allowed"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS middleware configured")


#middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(
        f"Request started: {request.method} {request.url.path}"
    )
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"Request completed: {request.method} {request.url.path} {response.status_code} - Duration: {process_time:.4f}s"
        )
        return response
    except Exception as e:
        duration = time.time() - start_time 
        logger.error(
            f"Request failed: {request.method} {request.url.path}"
            f" Error:{e} - Duration:{duration:.4f}s"
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error",
                      "path":request.url.path   
                     },   
        )
logger.info("Request logging middleware configured")

# STARTUP & SHUTDOWN EVENTS
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")
    logger.info("=" * 60)
    logger.info(" KadalVazhi API Server Starting...")
    logger.info("=" * 60)
    logger.info(f"Environment: {'DEVELOPMENT' if settings.debug else 'PRODUCTION'}")
    logger.info(f"Model: {settings.model_name}")
    logger.info(f"OpenWeather API: {'Configured ✅' if settings.openweather_api_key else 'Missing ❌'}")
    logger.info(f"Groq API: {'Configured ✅' if settings.groq_api_key else 'Missing ❌'}")
    logger.info("=" * 60)
    logger.info("✅ Server started successfully")

    
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")
    logger.info("=" * 60)
    logger.info("🛑 KadalVazhi API Server Shutting Down...")
    logger.info("=" * 60)
    logger.info("✅ Server shut down successfully")
    
# ROOT ENDPOINTS
@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {
        "message": "KadalVazhi API is running",
        "docs": "/docs",
        "status": "Running",
        "redoc": "/redoc"if settings.debug else "disabled in production"
    }

@app.get("/health")
async def health_check():
    logger.debug("Health check called")
    return {
        "status": "ok",
        "service": "kadalvazhi-api",
        "version": "0.1.0",
        "status": "healthy",
        "timestamp": time.time(),
    }

logger.info("main.py loaded successfully")