#!/bin/bash

# Exit on error
set -e

echo "Starting Backend Assessment Project..."

# Step 1: Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker Desktop is not running. Please start it and try again."
    exit 1
fi

# Step 2: Build and start services
echo "Building and starting services with Docker Compose..."
docker-compose up -d --build

# Step 3: Wait for services to be ready
echo "Waiting for services to initialize..."
until curl -s http://localhost:5000/api/health > /dev/null; do
  echo "Still waiting for Mock Server..."
  sleep 2
done

echo "Mock Server is UP!"

# Give a few more seconds for the pipeline service to initialize its tables
sleep 5

echo "--------------------------------------------------------"
echo "Project is ready!"
echo "Mock Server: http://localhost:5000/api/customers"
echo "FastAPI Pipeline: http://localhost:8000/docs"
echo "--------------------------------------------------------"
echo "To test the ingestion, run:"
echo "curl -X POST http://localhost:8000/api/ingest"
echo "--------------------------------------------------------"

# Show service statuses
docker-compose ps
