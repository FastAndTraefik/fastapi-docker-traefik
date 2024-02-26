from fastapi import FastAPI

from app.db import database, User


app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/")
async def read_root():
    users = await User.objects.all()
    return {"users": users, "message": "Hello"}


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    
    # Check if users table exists
    async with database:
        users_table_exists = await database.fetch_val("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
    
    # If users table doesn't exist, create it
    if not users_table_exists:
        async with database:
            await database.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR(128) UNIQUE NOT NULL, active BOOLEAN NOT NULL DEFAULT TRUE)")
    
    # Now that the table exists, create dummy entries
    await User.objects.get_or_create(email="test@test.com")
    await User.objects.get_or_create(email="test2@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
