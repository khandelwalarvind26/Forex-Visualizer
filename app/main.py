from app.api.routes import forex_data
from app.db import create_tables
from app.services import periodic_task
from contextlib import asynccontextmanager

from fastapi import FastAPI

# Wrapper to run async function
# @aiocron.crontab('0 6 * * *')  # First execution at 6:00 AM, then every 24 hours
# async def run_async_task():
#     await periodic_task()

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Create tables on startup'''

    # Startup logic
    await create_tables()

    # Run the function immediately and schedule it to run every hour
    # Run the function once at startup
    await periodic_task()
    # Start the scheduled task
    # run_async_task.start()
    
    yield  # The point at which the application runs


app = FastAPI(lifespan=lifespan)

app.include_router(forex_data.router, prefix="/api/forex-data")



