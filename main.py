import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import TeaBlend, Testimonial, Subscriber

app = FastAPI(title="Cozy Herbal Tea API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cozy Herbal Tea API"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# API models for requests
class SubscribeIn(BaseModel):
    email: str
    name: Optional[str] = None
    interests: Optional[List[str]] = None

# Tea Blends
@app.get("/api/blends")
def list_blends(limit: int = 20):
    docs = get_documents("teablend", {}, limit)
    # Convert ObjectId and datetimes to strings for JSON friendliness
    safe_docs = []
    for d in docs:
        d["_id"] = str(d.get("_id"))
        for k, v in list(d.items()):
            if hasattr(v, "isoformat"):
                d[k] = v.isoformat()
        safe_docs.append(d)
    return safe_docs

@app.post("/api/blends", status_code=201)
def create_blend(blend: TeaBlend):
    try:
        new_id = create_document("teablend", blend)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Testimonials
@app.get("/api/testimonials")
def list_testimonials(limit: int = 10):
    docs = get_documents("testimonial", {}, limit)
    safe_docs = []
    for d in docs:
        d["_id"] = str(d.get("_id"))
        for k, v in list(d.items()):
            if hasattr(v, "isoformat"):
                d[k] = v.isoformat()
        safe_docs.append(d)
    return safe_docs

@app.post("/api/testimonials", status_code=201)
def create_testimonial(item: Testimonial):
    try:
        new_id = create_document("testimonial", item)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Newsletter subscriptions
@app.post("/api/subscribe", status_code=201)
def subscribe(data: SubscribeIn):
    sub = Subscriber(email=data.email, name=data.name or None, interests=data.interests or [])
    try:
        new_id = create_document("subscriber", sub)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Schema endpoint (optional helper)
@app.get("/schema")
def get_schema_info():
    return {
        "collections": [
            "teablend",
            "testimonial",
            "subscriber"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
