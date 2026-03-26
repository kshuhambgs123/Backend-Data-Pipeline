import dlt
import requests
import os

from datetime import datetime

FLASK_API_URL = os.getenv("FLASK_API_URL", "http://mock-server:5000/api/customers")

@dlt.resource(name="customers", write_disposition="merge", primary_key="customer_id")
def fetch_customers():
    page = 1
    limit = 10
    
    while True:
        try:
            response = requests.get(f"{FLASK_API_URL}?page={page}&limit={limit}")
            if response.status_code != 200:
                break
                
            json_data = response.json()
            data = json_data.get("data", [])
            
            if not data:
                break
                
            # Process records to ensure proper types
            for record in data:
                if "date_of_birth" in record and record["date_of_birth"]:
                    # In python 3.10+, fromisoformat can handle YYYY-MM-DD
                    record["date_of_birth"] = datetime.fromisoformat(record["date_of_birth"]).date()
                if "created_at" in record and record["created_at"]:
                    record["created_at"] = datetime.fromisoformat(record["created_at"].replace("Z", "+00:00"))
            
            # Yield individual records instead of batches to be safe
            yield from data
            page += 1
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

def run_ingestion():
    pipeline = dlt.pipeline(
        pipeline_name="customer_pipeline",
        destination="postgres",
        dataset_name="public",
        credentials=os.getenv("DATABASE_URL")
    )
    
    # Track the count
    records = list(fetch_customers())
    total_processed = len(records)
    
    pipeline.run(records, table_name="customers")
    
    return total_processed
