# The entry point (API Endpoints)
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import security
import engine

app = FastAPI(title="ChartifyAPI - Analytics as a Service")

# Helper to get DB session
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 1. REGISTER A DATABASE ---
@app.post("/sources/add")
def add_data_source(source: models.SourceCreate, db: Session = Depends(get_db)):
    """
    Customer sends their DB credentials. We encrypt and save them.
    We return an ID (e.g., source_id: 1) they use for future calls.
    """
    encrypted_pw = security.encrypt_password(source.password)
    
    new_source = models.DataSource(
        name=source.name,
        db_type=source.db_type,
        host=source.host,
        port=source.port,
        user=source.user,
        encrypted_password=encrypted_pw,
        database_name=source.database_name
    )
    db.add(new_source)
    db.commit()
    db.refresh(new_source)
    return {"message": "Source added successfully", "source_id": new_source.id}

# --- 2. GENERATE CHART DATA ---
@app.post("/analytics/generate")
def get_chart_data(req: models.AnalyticsRequest, db: Session = Depends(get_db)):
    """
    Customer sends: "Use source_id 1, give me Sum of Sales by Country"
    """
    # 1. Find the source info in our internal DB
    source = db.query(models.DataSource).filter(models.DataSource.id == req.source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Data Source not found")
    
    # 2. Call the Engine
    result = engine.generate_analytics(source, req)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

# uvicorn main:app --reload # Command to run the server in development