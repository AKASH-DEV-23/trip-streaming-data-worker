import json
import threading
from datetime import datetime
import pandas as pd
from azure.eventhub import EventData

from app.core.eventhub import producer

stop_event = threading.Event()
streaming_thread = None
is_running = False
lock = threading.Lock()


# ---------------- LOAD EXCEL ----------------
def load_trips_from_excel(path: str):
    df = pd.read_excel(path)
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient="records")


# ---------------- NORMALIZE TO GENERATOR SCHEMA ----------------
def normalize_trip(row: dict):
    return {
        "TripID": row.get("TripID"),
        "ShipperID": row.get("ShipperID"),
        "CategoryID": row.get("CategoryID"),
        "Customer": row.get("Customer"),

        "ShipDate": str(row.get("ShipDate")),
        "OriginCity": row.get("OriginCity"),
        "OriginState": row.get("OriginState"),
        "ShipDays": row.get("ShipDays"),

        "DestinationCity": row.get("DestinationCity"),
        "DestinationState": row.get("DestinationState"),
        "DeliveryDate": str(row.get("DeliveryDate")),

        "TotalMiles": row.get("TotalMiles"),
        "LoadedMiles": row.get("LoadedMiles"),
        "ShippingCost": row.get("ShippingCost"),
        "Revenue": row.get("Revenue"),
        "Capacity": row.get("Capacity"),
        "TripType": row.get("TripType"),
        "CheckPoints": row.get("CheckPoints"),
        "Profit": row.get("Profit"),
        "Revenue Miles": row.get("Revenue Miles"),
        "Profit miles": row.get("Profit miles"),

        # ensure streaming timestamp exists
        "EventTime": datetime.utcnow().isoformat()
    }


# ---------------- WORKER ----------------
def streaming_worker_excel(path: str, batch_size: int = 300):
    global is_running

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⚡ Excel streaming started")

    try:
        trips = load_trips_from_excel(path)
        total = len(trips)
        sent = 0

        for i in range(0, total, batch_size):
            if stop_event.is_set():
                break

            batch = producer.create_batch()
            chunk = trips[i:i + batch_size]

            for row in chunk:
                trip = normalize_trip(row)

                event = EventData(json.dumps(trip, default=str))
                event.content_type = "application/json"
                batch.add(event)

            producer.send_batch(batch)

            sent += len(chunk)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📤 Sent {sent}/{total}")

        print(f"✅ Finished streaming {total} Excel rows")

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Excel streaming error: {e}")

    finally:
        with lock:
            is_running = False

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🛑 Excel streaming stopped")


# ---------------- START ----------------
def start_excel_stream(path: str = "app/data/Trips.xlsx", batch_size: int = 300):
    global streaming_thread, is_running

    with lock:
        if is_running:
            return False

        stop_event.clear()
        streaming_thread = threading.Thread(
            target=streaming_worker_excel,
            args=(path, batch_size),
            daemon=True
        )
        streaming_thread.start()
        is_running = True

    return True


# ---------------- STOP ----------------
def stop_excel_stream():
    global is_running

    with lock:
        if not is_running:
            return False

        stop_event.set()
        is_running = False

    return True


# ---------------- STATUS ----------------
def get_excel_stream_status():
    return {
        "excel_streaming_active": is_running,
        "thread_alive": streaming_thread.is_alive() if streaming_thread else False
    }