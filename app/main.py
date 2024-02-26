from fastapi import FastAPI
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from app.db import database
from app.db import User


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
    try:
        if not database.is_connected:
            await database.connect()

        # Check if users table exists
        async with database:
            sql_fetch_table_users = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users');"
            users_table_exists = await database.fetch_val(sql_fetch_table_users)
        # If users table doesn't exist, create it
        if not users_table_exists:
            async with database:
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
