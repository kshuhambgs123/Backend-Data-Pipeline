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

## 📡 API Endpoints

### 1. Flask Mock Server (`localhost:5000`)
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/health` | GET | Health check status |
| `/api/customers` | GET | Paginated customers from JSON file (`page`, `limit`) |
| `/api/customers/{id}` | GET | Fetch a single customer by ID |

### 2. FastAPI Pipeline Service (`localhost:8000`)
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/ingest` | POST | Trigger the data ingestion pipeline (Mock → Postgres) |
| `/api/customers` | GET | Paginated customers from PostgreSQL database |
| `/api/customers/{id}` | GET | Fetch a single customer from database by ID |
| `/docs` | GET | **Interactive OpenAPI (Swagger) Documentation** |

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

## ✨ Features Highlight
- **Upsert Logic**: Uses `dlt` with `write_disposition="merge"` to ensure customer data is updated if it already exists in the database.
- **Auto-Pagination**: The ingestion service automatically loops through all pages of the Mock Server until all data is retrieved.
- **Error Handling**: Comprehensive 404 and 500 error management across both services.
- **Database Normalization**: SQLAlchemy models define strict schemas for data integrity.
