from app.api.routes import forex_data
from app.db import create_tables
from app.services import periodic_task
from contextlib import asynccontextmanager

from fastapi import FastAPI
import aiocron

# Wrapper to run async function
@aiocron.crontab('0 0 * * *')  # Execute in every 24 hours at 00:00am
async def run_async_task():
    '''CronJob'''

    await periodic_task()

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Create tables and run cron job on startup'''

    # Startup logic
    await create_tables()

    # Run the function once at startup
    await periodic_task()
    # Start the scheduled task
    run_async_task.start()
    
    yield  # The point at which the application runs


app = FastAPI(lifespan=lifespan)

app.include_router(forex_data.router, prefix="/api/forex-data")



