from fastapi import FastAPI

from app.db import database, User


app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/")
async def read_root():
    return await User.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
# Create missing tables
    async with database:
        if not await database.fetch_val("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')"):
            await database.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR(128) UNIQUE NOT NULL, active BOOLEAN NOT NULL DEFAULT TRUE)")
# create a dummy entry
    await User.objects.get_or_create(email="test@test.com")
    # await User.objects.get_or_create(email="test2@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
