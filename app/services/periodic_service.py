from app.db import Quote, get_db
from app.core import settings
from app.utils import logger
from .scraper import Scraper

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, delete

from datetime import timedelta, datetime
import traceback

async def periodic_task():
    '''Function to be called every period to fetch data'''
    
    try:
        logger.info(f"Starting periodic fetching task")

        # Current time at which the task is executed
        current_timestamp = datetime.now()

        # Check db for latest available timestamp
        latest_timestamp = None

        async for db in get_db():
            result = await db.execute(select(func.max(Quote.date)))
            latest_timestamp = result.scalar()

        # If there is no entry in db, fetch all entries for past year
        if latest_timestamp is None:
            latest_timestamp = current_timestamp - timedelta(days=375)

        latest_timestamp = latest_timestamp + timedelta(days=1)
        logger.info(f"Latest timestamp is: {latest_timestamp.date()}")

        # If the latest date already exists in db return
        if(latest_timestamp.date() >= current_timestamp.date()):
            logger.info("Latest data already present")
            return
        
        # Fetch all the entries betweem latest_timestamp and current_timestamp
        scraper = Scraper()

        for (from_country, to_country) in settings.COUNTRY_COMBINATIONS:

            logger.info(f"Scraping {from_country} to {to_country}")
            scraper.scrape(from_country, to_country, latest_timestamp, current_timestamp)

            logger.info("Saving")
            await scraper.save()


        # Delete all older quote entries from db
        logger.info("Deleting older entries")
        old_timestamp = current_timestamp - timedelta(days=376)

        async for db in get_db():
            query = delete(Quote).where(Quote.date <= old_timestamp)
            await db.execute(query)
            await db.commit()
        
    except Exception as _:
        tb = traceback.format_exc()
        logger.info(tb)

    finally:
        logger.info("Done periodic task")