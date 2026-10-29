import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="KidSpeak AI Service",
    version="1.0.0",
    description="AI Service for KidSpeak - Speech Recognition and Pronunciation Assessment",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "KidSpeak AI Service",
        "device": os.getenv("DEVICE", "cpu"),
        "sample_rate": int(os.getenv("SAMPLE_RATE", "16000")),
        "weights_dir": os.getenv("MODEL_WEIGHTS_DIR", "models/weights"),
        "docs_url": "/docs",
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "device": os.getenv("DEVICE", "cpu"),
    }
