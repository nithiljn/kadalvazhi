from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
from app.api.v1 import weather
from app.utils.logger import get_logger
from app.config import settings

logger = get_logger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown lifecycle.
    
    WHY LIFESPAN:
    - Replaces deprecated @app.on_event("startup/shutdown")
    - Keeps startup & shutdown logic in ONE place
    - Variables shared between startup and shutdown
    - Guaranteed cleanup even if errors occur
    
    STRUCTURE:
    - Code BEFORE yield = startup logic
    - yield = app runs here (handles requests)
    - Code AFTER yield = shutdown logic
    """
    
    logger.info("KadalVazhi API Server Starting...")
    logger.info(
        f"Environment: {'DEVELOPMENT' if settings.debug else 'PRODUCTION'}"
    )
    logger.info(f"Model: {settings.model_name}")
    logger.info(
        f"OpenWeather API: "
        f"{'Configured ✅' if settings.openweather_api_key else 'Missing ❌'}"
    )
    logger.info(
        f"Groq API: "
        f"{'Configured ✅' if settings.groq_api_key else 'Missing ❌'}"
    )
    logger.info("=" * 60)
    logger.info("✅ Server started successfully")
    
    # Future additions here:
    # await init_db()           ← Database connection
    # await init_redis()        ← Cache connection
    # await load_ml_models()    ← AI model loading
    
    # =====================================================================
    yield  # ← APP RUNS HERE (handles all requests)
    # =====================================================================
    
    # =====================================================================
    # SHUTDOWN (runs after last request)
    # =====================================================================
    
    logger.info("=" * 60)
    logger.info("🛑 KadalVazhi API Server Shutting Down...")
    logger.info("=" * 60)
    
    # Future cleanup here:
    # await close_db()          ← Close database
    # await close_redis()       ← Close cache
    # await cleanup_ml_models() ← Free memory
    
    logger.info("✅ Server shut down gracefully")
    logger.info("=" * 60)

# ============================================================================
# CREATE FASTAPI APP (with lifespan!)
# ============================================================================

app = FastAPI(
    title="KadalVazhi API",
    description="Smart Fishing Assistant API for Tamil Nadu & Kerala fishermen",
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,  # ← PASS LIFESPAN HERE!
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

logger.info("FastAPI app initialized")

# ============================================================================
# MIDDLEWARE - CORS
# ============================================================================

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

# ============================================================================
# MIDDLEWARE - REQUEST LOGGING
# ============================================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log every HTTP request with timing info
    
    CAPTURES:
    - Method + URL path
    - Response status code
    - Request duration
    - Errors if any
    """
    start_time = time.time()
    
    logger.info(f"Request started: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        logger.info(
            f"Request completed: {request.method} {request.url.path} "
            f"{response.status_code} - Duration: {duration:.4f}s"
        )
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            f"Request failed: {request.method} {request.url.path} "
            f"Error: {e} - Duration: {duration:.4f}s"
        )
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal Server Error",
                "path": request.url.path
            }
        )

logger.info("Request logging middleware configured")

# ============================================================================
# INCLUDE ROUTERS
# ============================================================================

app.include_router(
    weather.router,
    prefix="/api/v1/weather",
    tags=["weather"]
)

logger.info("Weather router included")

# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - API info"""
    logger.debug("Root endpoint called")
    return {
        "message": "KadalVazhi API is running",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs" if settings.debug else "disabled in production",
        "redoc": "/redoc" if settings.debug else "disabled in production"
    }

@app.get("/health")
async def health_check():
    """Health check for monitoring tools"""
    logger.debug("Health check called")
    return {
        "status": "healthy",
        "service": "kadalvazhi-api",
        "version": "0.1.0",
        "timestamp": time.time()
    }

logger.info("main.py loaded successfully")