from fastapi import FastAPI
from src.routes import health, scan
from src.config.database import close_database_connection
import uvicorn
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Suraksha API",
    description="API for scanning and validating web applications for security vulnerabilities",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(scan.router, prefix="/api", tags=["scan"])


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application")
    await close_database_connection()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
