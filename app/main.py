from fastapi import FastAPI
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from app.db import database, User


app = FastAPI(title="FastAPI, Docker, and Traefik")

REQUEST_COUNT = Counter('request_count', 'App Request Count')
IN_PROGRESS_REQUESTS = Gauge('in_progress_requests', 'In Progress Requests')


@app.get("/")
async def read_root():
    REQUESTS.inc()
    return await User.objects.all()

@app.get("/metrics")
def metrics():
    IN_PROGRESS_REQUESTS.inc()
    data = generate_latest()
    IN_PROGRESS_REQUESTS.dec()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await User.objects.get_or_create(email="test@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
