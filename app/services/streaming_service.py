import json
import threading
import time
from datetime import datetime, timezone
from azure.eventhub import EventData
from app.core.eventhub import producer
from app.services.trip_generator import generate_trip

stop_event = threading.Event()
streaming_thread = None
is_running = False
lock = threading.Lock()

def streaming_worker():
    global is_running

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚛 Streaming worker started...")

    try:
        while not stop_event.is_set():
            trip = generate_trip()

            batch = producer.create_batch()

            event = EventData(json.dumps(trip))
            event.content_type = "application/json"
            batch.add(event)

            producer.send_batch(batch)

            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📤 Sent TripID={trip['TripID']}")

            time.sleep(2)

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error sending event: {e}")

    finally:
        with lock:
            is_running = False

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🛑 Streaming worker stopped.")


def start_stream():
    global streaming_thread, is_running

    with lock:
        if is_running:
            return False

        stop_event.clear()
        streaming_thread = threading.Thread(target=streaming_worker, daemon=True)
        streaming_thread.start()
        is_running = True

    return True


def stop_stream():
    global is_running

    with lock:
        if not is_running:
            return False

        stop_event.set()
        is_running = False

    return True


def start_stream_for_duration(seconds: int):
    if not start_stream():
        return False

    def auto_stop():
        time.sleep(seconds)
        if not stop_event.is_set():
            stop_stream()
            print(f"⏰ Auto stopped after {seconds} sec")

    threading.Thread(target=auto_stop, daemon=True).start()
    return True

def get_stream_status():
    return {
        "streaming_active": is_running,
        "thread_alive": streaming_thread.is_alive() if streaming_thread else False
    }
