from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import generate_latest

from app.db import database
from app.db import User

import time


app = FastAPI(title="FastAPI, Docker, and Traefik")

REQUEST_COUNT = Counter("request_count", "App Request Count")
IN_PROGRESS_REQUESTS = Gauge("in_progress_requests", "In Progress Requests")


@app.get("/")
async def read_root():
    REQUEST_COUNT.inc()
    return await User.objects.all()


@app.get("/metrics")
def metrics():
    IN_PROGRESS_REQUESTS.inc()
    data = generate_latest()
    IN_PROGRESS_REQUESTS.dec()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.on_event("startup")
async def startup():
    time.sleep(20)
    try:
        if not database.is_connected:
            await database.connect()

        # Check if users table exists
        sql_fetch_table_users = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users');"
        users_table_exists = await database.fetch_val(sql_fetch_table_users)

        # If users table doesn't exist, create it
        if not users_table_exists:
            sql_create_table = "CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR(128) UNIQUE NOT NULL, active BOOLEAN NOT NULL DEFAULT TRUE);"
            await database.execute(sql_create_table)

        # Now that the table exists, create dummy entries
        await User.objects.get_or_create(email="test100@test.com")
    except Exception as e:
        print(f"An error occurred during startup: {e}")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
