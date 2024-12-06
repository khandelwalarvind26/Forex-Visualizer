from app.api.routes import forex_data, frontend
from app.db import create_tables
from app.services import periodic_task
from app.utils import logger, run_async_in_thread

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from contextlib import asynccontextmanager
import aiocron

# Wrapper to run async function
@aiocron.crontab('0 0 * * *')  # Execute in every 24 hours at 00:00am
async def run_async_task():
    '''CronJob'''

    logger.info("Starting periodic task in a separate thread")
    run_async_in_thread(periodic_task())  # Pass the coroutine


# Fuctions to run on startup
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

# Serve the static files (e.g., HTML, JS, CSS) from the "static" directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routes
app.include_router(forex_data.router, prefix="/api/forex-data")
app.include_router(frontend.router)