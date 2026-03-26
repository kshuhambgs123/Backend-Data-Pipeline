import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import engine, SessionLocal, init_db, get_db
from models.customer import Customer
from services.ingestion import run_ingestion
from sqlalchemy import select, func

app = FastAPI(title="Data Pipeline Service", version="1.0.0")

@app.on_event("startup")
def startup_event():
    # In some production environments migrations (like Alembic) are used.
    # For this assignment, we use init_db() to create tables if they don't exist.
    init_db()

@app.post("/api/ingest")
def ingest():
    try:
        processed_count = run_ingestion()
        return {"status": "success", "records_processed": processed_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
def list_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    
    total = db.query(func.count(Customer.customer_id)).scalar()
    customers = db.query(Customer).offset(offset).limit(limit).all()
    
    return {
        "data": customers,
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{id}")
def get_customer(id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == id).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    return customer

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
