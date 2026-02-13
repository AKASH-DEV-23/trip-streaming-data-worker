from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Fabric Real-Time Trip Streamer")

app.include_router(router)
