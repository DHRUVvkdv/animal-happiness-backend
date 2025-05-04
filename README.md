docker build -t idc-backend .
docker run --rm -p 8000:8000 --entrypoint python --env-file .env idc-backend main.py
cdk bootstrap --region us-east-1 --profile idc
cdk deploy --profile idc

# Animal Happiness Backend

A FastAPI-based backend application for animal data collection and retrieval.

## Overview

The Animal Happiness Backend provides a REST API to collect, store, and query data related to animal behaviors and responses. It uses a serverless architecture with FastAPI, DynamoDB, and AWS Lambda compatibility.

## Features

- REST API for animal data management
- Time-series data storage and retrieval
- Filtering by animal ID, response type, and time range
- Batch data upload capabilities
- Pagination support for large datasets
- API key authentication for security

## Local Development

### Prerequisites

- Python 3.11+
- Docker (optional)
- AWS account (for DynamoDB)
- AWS CLI configured (for local DynamoDB access)

### Setup

1. Clone the repository:

   ```
   git clone <repository-url>
   cd animal-happiness-backend
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```
   Update the values in the `.env` file as needed.

### Running Locally

#### Method 1: Direct Python Execution

```
cd src
python main.py
```

The API will be available at http://localhost:8001

#### Method 2: Using Docker

```
docker build -t animal-happiness-backend .
docker run --rm -p 8001:8001 -v $(pwd)/.env:/var/task/.env animal-happiness-backend
```

### API Documentation

Once the server is running, access the OpenAPI documentation at http://localhost:8001/docs

### Key Endpoints

- `POST /animal/data` - Create a new animal data entry
- `POST /animal/data/batch` - Batch upload animal data
- `GET /animal/data` - Get all animal data with pagination
- `GET /animal/data/cow/{cow_id}` - Get animal data by cow ID
- `GET /animal/data/{entry_id}` - Get animal data by entry ID
- `GET /animal/data/response/{response_type}` - Get animal data by response type

## DynamoDB Setup

For local development, the application will attempt to create the required DynamoDB table automatically. For production deployment, it's recommended to create the table using infrastructure as code (e.g., AWS CDK, CloudFormation, or Terraform).

### Table Structure

- **Table Name**: animal-happiness-data (configurable via environment variable)
- **Primary Key**: entry_id (String)
- **GSI**: source-time-index
  - Partition Key: source (String)
  - Sort Key: time (String)

## AWS Deployment

The application is designed to be deployed as an AWS Lambda function with API Gateway integration using AWS CDK or similar tools.

### Lambda Deployment

```
# Example deployment using AWS CDK (requires additional setup)
cdk deploy --profile your-profile-name
```

## Sample Request

```bash
curl -X 'POST' \
  'http://localhost:8000/animal/data' \
  -H 'accept: application/json' \
  -H 'X-API-Key: your-api-key-here' \
  -H 'Content-Type: application/json' \
  -d '{
  "cow_id": "cow123",
  "response_type": "happy",
  "time": "2025-05-03T12:34:56.789Z",
  "source": "api"
}'
```
