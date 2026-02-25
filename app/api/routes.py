from fastapi import APIRouter, Query
from datetime import datetime
import app.services.streaming_service as streaming_service

router = APIRouter(prefix="/stream", tags=["Streaming"])


@router.get("/status")
def stream_status():
    status = streaming_service.get_stream_status()
    return {
        **status,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/start")
def start_stream(duration: int | None = Query(None, description="Duration in seconds")):
    if duration:
        if not streaming_service.start_stream_for_duration(duration):
            return {"status": "already_running"}
        return {"status": "started", "duration_sec": duration}

    if not streaming_service.start_stream():
        return {"status": "already_running"}

    return {"status": "started"}


@router.post("/stop")
def stop_stream():
    if not streaming_service.stop_stream():
        return {"status": "not_running"}

    return {"status": "stopped"}


