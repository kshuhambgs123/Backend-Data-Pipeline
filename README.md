# Backend Developer Technical Assessment: Data Pipeline

A full-stack data pipeline implementation featuring a Mock Data Server (Flask), an Ingestion Service (FastAPI), and a PostgreSQL database.

## 🚀 Project Overview 

This project demonstrates a robust data pipeline that:
1.  **Mock Server**: Provides customer data from a static JSON file via a paginated REST API.
2.  **Pipeline Service**: Fetches data from the mock server, handles automatic pagination, and upserts it into a PostgreSQL database using the `dlt` (Data Load Tool) library.
3.  **Data API**: Exposes the ingested data through a separate set of FastAPI endpoints with database-level pagination.

---

## 🏗️ Architecture

-   **Service 1: `mock-server` (Flask)**
    -   Port: `5000`
    -   Source: `data/customers.json`
    -   Tech: Flask, JSON-based storage.
-   **Service 2: `pipeline-service` (FastAPI)**
    -   Port: `8000`
    -   Logic: Fetches from `mock-server` paginated → Ingests via `dlt` (UPSERT mode) → Stores in Postgres.
    -   Tech: FastAPI, SQLAlchemy, `dlt`, `psycopg2`.
-   **Service 3: `postgres` (PostgreSQL 15)**
    -   Port: `5432`
    -   Database: `customer_db`

---

## 📋 Prerequisites

-   Docker Desktop (running)
-   Python 3.10+
-   `curl` (for testing)

---

## 🛠️ Project Setup Guide

### Step 1: Clone the Repository
```bash
git clone https://github.com/kshuhambgs123/Backend-Data-Pipeline.git
cd Backend-Data-Pipeline
```

### Step 2: Ensure Docker is Running
Verify that **Docker Desktop** is open and active on your machine.

### Step 3: Deployment (Choose ONE)

#### Option A: Docker Compose (Recommended)
This is the easiest way to start all 3 services at once:
```bash
chmod +x setup.sh
./setup.sh
```
*Note: This script will build all images, start the containers, and wait for the mock server to become healthy.*

#### Option B: Local Development Setup
If you prefer running the Python code directly on your host machine:
1. Create a virtual environment: `python3 -m venv venv && source venv/bin/activate`
2. Install requirements: `pip install -r mock-server/requirements.txt -r pipeline-service/requirements.txt`
3. Start the Postgres DB separately: `docker-compose up -d postgres`
4. Start Mock Server: `python mock-server/app.py`
5. Start Pipeline: `export DATABASE_URL=postgresql://postgres:password@localhost:5432/customer_db && export FLASK_API_URL=http://localhost:5000/api/customers && python pipeline-service/main.py`

---

## 📡 API Reference

### 1. Mock Server (Flask) - `localhost:5000`

**GET `/api/customers`**
Retrieve a paginated list of mock customers from the JSON store.
- **Params**: `page` (default 1), `limit` (default 10)
- **Sample Response**:
```json
{
  "data": [
    {
      "customer_id": "CUST001",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "balance": 1500.5
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 1
}
```

---

### 2. Pipeline Service (FastAPI) - `localhost:8000`

**POST `/api/ingest`**
Triggers the `dlt` pipeline to fetch data from Flask and upsert it into Postgres.
- **Expected Response**:
```json
{
  "status": "success",
  "records_processed": 25
}
```

**GET `/api/customers`**
Query the ingested data directly from the PostgreSQL database.
- **Params**: `page`, `limit`
- **Output**: Fully typed JSON matching the SQL schema.

**Interactive Docs**: Access `http://localhost:8000/docs` for the full OpenAPI 3.0 specification.

---

## 🧪 Testing the Flow

Once the services are running:

### Step 1: Verify Mock Server
```bash
curl "http://localhost:5000/api/customers?page=1&limit=5"
```

### Step 2: Trigger Ingestion (POST Request)
```bash
curl -X POST http://localhost:8000/api/ingest
```
*Expected Result: `{"status": "success", "records_processed": 25}`*

### Step 3: Verify Data in Postgres (via Pipeline Service)
```bash
curl "http://localhost:8000/api/customers?page=1&limit=5"
```

---

## 📁 Project Structure

```text
project-root/
├── docker-compose.yml       # Orchestration for all 3 services
├── setup.sh                 # Single script to build and start
├── .gitignore               # Standard exclusions
├── README.md               # Documentation
├── mock-server/             # Backend Flask Mock Service
│   ├── app.py
│   ├── data/customers.json  # Source of Truth
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/       # Ingestion & API Service
    ├── main.py
    ├── database.py          # SQLAlchemy connection setup
    ├── models/customer.py   # SQLAlchemy model definitions
    ├── services/ingestion.py # dlt-based ingestion logic
    ├── Dockerfile
    └── requirements.txt
```

---

## 🛠️ Troubleshooting (macOS Specific)

### 1. Port 5432 Conflict
If you have a local PostgreSQL server running, the Docker container might fail to bind to port `5432`.
- **Solution**: Stop your local Postgres or change the host port in `docker-compose.yml` (e.g., `"5433:5432"`).
- **Command to check**: `lsof -i :5432`

### 2. Port 5000 Conflict (AirPlay)
On newer macOS versions, "AirPlay Receiver" might occupy port 5000.
- **Solution**: Go to *System Settings > General > AirPlay & Handoff* and disable "AirPlay Receiver", or use the `docker-compose.yml` to remap the host port.

---

## ✨ Key Features

-   **🔄 Intelligent Upsert Logic**: Leverages the `dlt` (Data Load Tool) library with `write_disposition="merge"`. This ensures that existing customer records are updated rather than duplicated, maintaining a single source of truth.
-   **📈 Automated Pagination Ingestion**: The pipeline service features a custom generator that intelligently traverses paginated Flask endpoints until the entire upstream dataset is synchronized.
-   **🛡️ Production-Grade Containerization**: Fully orchestrated 3-service stack using Docker Compose. Includes automated health checks to ensure the database is ready before ingestion begins.
-   **💎 Schema Integrity & Normalization**: Uses SQLAlchemy ORM to enforce strict data schemas. Includes automated type mapping for complex fields like `DATE` and `TIMESTAMP` from raw JSON strings.
-   **🛠️ Developer-First Experience**: 
    -   **Zero-Config Setup**: A single `setup.sh` script to build and run the entire environment.
    -   **Live Documentation**: Interactive OpenAPI/Swagger UI at `/docs` for real-time API testing.
-   **🚀 High-Performance Data Loading**: Implements memory-efficient stream processing for data ingestion, ensuring stability even with larger datasets.

---
