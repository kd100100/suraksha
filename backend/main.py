from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import health, scan
from src.config.database import close_database_connection
import uvicorn
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Get host and port from environment variables or use defaults
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

app = FastAPI(
    title="Suraksha API",
    description="API for scanning and validating web applications for security vulnerabilities",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

logger = logging.getLogger(__name__)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(scan.router, prefix="/api", tags=["scan"])


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application")
    logger.info(f"Server running on http://{HOST}:{PORT}")
    logger.info(f"Swagger UI available at http://{HOST}:{PORT}/api/docs")
    logger.info(f"ReDoc available at http://{HOST}:{PORT}/api/redoc")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application")
    await close_database_connection()

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
