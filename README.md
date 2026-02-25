# 🚚 Trip Streaming Data Worker

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Streaming](https://img.shields.io/badge/Streaming-Real--Time-orange)
![Microsoft Fabric](https://img.shields.io/badge/Microsoft-Fabric-purple)

A real-time trip data streaming worker built with **FastAPI** that generates logistics trip events and streams them into **Microsoft Fabric Eventstream → Lakehouse** for real-time analytics using the **medallion architecture**.

---

# 🧭 Architecture

```
FastAPI Worker
      ↓
Microsoft Fabric Eventstream
      ↓
Bronze Lakehouse (trips_stream_data)
      ↓
Silver (clean)
      ↓
Gold (analytics)
      ↓
Power BI Real-Time Dashboard
```

---

# ✨ Features

* Real-time trip event generation
* REST API to start/stop streaming
* Configurable streaming duration
* Fabric-ready JSON schema
* Dockerized deployment
* Cloud deployable (Koyeb / Fly.io / Render / Azure)
* Thread-safe streaming control
* Realistic logistics dataset

---

# 📦 Tech Stack

* Python 3.11
* FastAPI
* Faker
* Docker
* Microsoft Fabric
* Eventstream
* Lakehouse (Delta)
* Power BI

---

# 🚀 API Endpoints

## Start streaming

```
POST /stream/start
```

## Start streaming for duration (seconds)

```
POST /stream/start?duration=60
```

## Stop streaming

```
POST /stream/stop
```

## Stream status

```
GET /stream/status
```

---

# 🐳 Docker

## Build image

```bash
docker build -t trip-streaming-data-worker .
```

## Run locally

```bash
docker run -p 8000:8000 --env-file .env trip-streaming-data-worker
```

API docs:

```
http://localhost:8000/docs
```

---

# ⚙️ Environment Variables

Create `.env` file:

```
EVENTHUB_CONNECTION_STRING=your_connection_string
EVENTHUB_NAME=your_eventhub_name
```

---

# ☁️ Deployment

This service can be deployed on any container platform:

* Koyeb
* Fly.io
* Render
* Azure Container Apps
* Railway

Example public image:

```
docker.io/akashowebdev/trip-streamerv1:latest
```

---

# 🧪 Example Usage

Start streaming for 30 seconds:

```bash
curl -X POST "http://localhost:8000/stream/start?duration=30"
```

Check status:

```bash
curl http://localhost:8000/stream/status
```

Stop streaming:

```bash
curl -X POST http://localhost:8000/stream/stop
```

---

# 📡 Microsoft Fabric Integration

Events are ingested into:

```
Azure Event Hub
   ↓
Fabric Eventstream
   ↓
Bronze Lakehouse (trips_stream_data)
```

Then processed via medallion architecture:

```
Bronze → Silver → Gold → Power BI
```

---

# 📁 Project Structure

```
trip-streaming-data-worker/
│
├─ app/
│   ├─ api/
│   ├─ core/
│   ├─ services/
│   └─ main.py
│
├─ Dockerfile
├─ requirements.txt
├─ run.py
├─ .env.example
└─ README.md
```

---

# 🎯 Use Cases

* Real-time logistics analytics demos
* Microsoft Fabric Eventstream testing
* Streaming pipeline simulations
* Data engineering portfolio projects
* Event-driven architecture demos
* Power BI real-time dashboards

---

# 👤 Author

**Akash Kumar**
Data & Backend Developer

GitHub: https://github.com/akash-dev-23

---

# 📜 License

MIT
