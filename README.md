# Animal Happiness Backend

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white) ![DynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Overview

The Animal Happiness Backend is a serverless API that collects, stores, and queries data related to cow affective states from the Animal Happiness system. It provides endpoints for recording cow responses (optimistic or pessimistic) and retrieving historical data for analysis.

## Features

- **RESTful API**: FastAPI-based endpoints for data management
- **Serverless Architecture**: AWS Lambda for scalable, cost-effective operation
- **NoSQL Database**: DynamoDB for flexible data storage
- **Authentication**: API key protection for security
- **Efficient Querying**: Global Secondary Index (GSI) for time-based searches
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Technology Stack

- **Framework**: FastAPI
- **Deployment**: AWS Lambda via AWS CDK
- **Database**: Amazon DynamoDB
- **API Gateway**: AWS API Gateway
- **Authentication**: API Key (X-API-Key header)
- **Container**: Docker

## API Endpoints

- `POST /animal/data`: Create a new animal data entry
- `POST /animal/data/batch`: Batch upload animal data
- `GET /animal/data`: Get all animal data with pagination
- `GET /animal/data/cow/{cow_id}`: Get animal data by cow ID
- `GET /animal/data/{entry_id}`: Get animal data by entry ID
- `GET /animal/data/response/{response_type}`: Get animal data by response type

## Local Development

### Prerequisites

- Python 3.11+
- Docker
- AWS CLI configured

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/ahidvt/animal-happiness-backend.git
   cd animal-happiness-backend
   ```

2. Create a `.env` file in the image directory:

   ```bash
   cd image
   cp .env.example .env
   ```

3. Fill in the required environment variables in `.env`:

   ```
   API_KEY=your_api_key
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   DYNAMODB_TABLE_NAME_ANIMAL=animal-happiness-data
   ```

4. Build and run the Docker container:

   ```bash
   docker build -t idc-backend .
   docker run --rm -p 8000:8000 --entrypoint python --env-file .env idc-backend main.py
   ```

5. The API will be available at http://localhost:8000/docs

## AWS Deployment

### Prerequisites

- AWS CDK installed
- AWS CLI configured with appropriate permissions
- Node.js and npm

### Deployment Steps

1. Navigate to the infrastructure directory:

   ```bash
   cd animal-happiness-backend-infra
   ```

2. Install CDK dependencies:

   ```bash
   npm install
   ```

3. Create a `.env` file in the infrastructure directory with the same variables as the local `.env.example` file

4. Bootstrap CDK (if not already done):

   ```bash
   cdk bootstrap --region us-east-1 --profile idc
   ```

5. Deploy the stack:

   ```bash
   cdk deploy --profile idc
   ```

6. Note the output URL for API access
   **Note for IDC students**: The API URL is already provided in your Credentials folder.

## Database Schema

- **Table Name**: animal-happiness-data
- **Primary Key**: entry_id (UUID)
- **GSI**: source-time-index
  - Partition Key: source
  - Sort Key: time
- **Fields**:
  - entry_id: Unique identifier (UUID)
  - cow_id: Identifier for the cow
  - response_type: Either "optimistic" or "pessimistic"
  - time: ISO 8601 timestamp
  - source: Data origin (e.g., "Raspberry Pi" or "api")

## Contributors

Developed by Dhruv Varshney of the Animal Happiness Team at Virginia Tech as part of the Interdisciplinary Design Capstone (IDC) Spring 2025.

For questions, contact dhruvvarshney@vt.edu or message on LinkedIn: https://www.linkedin.com/in/dvar/
