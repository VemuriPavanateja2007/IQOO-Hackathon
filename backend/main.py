import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import settings
from backend.database import engine, Base
from backend.routers import auth, profile, activity, medications, appointments, recommendations, risk, ai_chat

# Create database tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="VitalMind AI - Antigravity Adaptation Health Platform for Microgravity Environments"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(activity.router)
app.include_router(medications.router)
app.include_router(appointments.router)
app.include_router(recommendations.router)
app.include_router(risk.router)
app.include_router(ai_chat.router)

# Mount Frontend Static Directory
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "online", "message": "VitalMind AI Backend Operational. API documentation at /docs"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "station": settings.STATION_NAME,
        "version": settings.VERSION
    }
