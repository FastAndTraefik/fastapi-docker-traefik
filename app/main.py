from fastapi import FastAPI

from app.db import database
from app.db import User


app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/")
async def read_root():
    return await User.objects.all()


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
