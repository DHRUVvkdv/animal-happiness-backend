"""
Main entry point for the Animal Happiness Backend API.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import uvicorn
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import boto3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get configuration from environment variables
DYNAMODB_TABLE_NAME_ANIMAL = os.getenv(
    "DYNAMODB_TABLE_NAME_ANIMAL", "animal-happiness-data"
)
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
PORT = int(os.getenv("PORT", "8001"))
HOST = os.getenv("HOST", "0.0.0.0")

try:
    # Import animal routes
    from animal_data_routes import router as animal_router

    # Import dependencies
    from api.dependencies import get_api_key

    # Initialize DynamoDB resource
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    animal_table = dynamodb.Table(DYNAMODB_TABLE_NAME_ANIMAL)

    # Initialize FastAPI app
    app = FastAPI(
        title="Animal Happiness API",
        description="API for animal data collection and retrieval",
        version="0.1.0",
    )

    # Include router
    app.include_router(animal_router)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Public route
    @app.get("/", tags=["Public"])
    async def root():
        """Root endpoint."""
        return {
            "message": "Welcome to the Animal Happiness API. Use the /animal/data endpoints for access."
        }

    # Health check route
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint."""
        logger.info("Health check endpoint called")
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "animal-happiness-api",
        }

    # Create Mangum handler for AWS Lambda
    handler = Mangum(app)

except Exception as e:
    # Log the exception if there's an error during startup
    logger.error(f"Error during application startup: {e}")
    raise

# Run the application (for development only, not used in Lambda)
if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
