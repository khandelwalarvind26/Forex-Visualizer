from app.db import get_db, Quote
from app.utils import logger, parse_period

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from datetime import datetime
import traceback

router = APIRouter()

@router.post("/")
async def forex_data(from_country: str, to_country: str, period: str, db: AsyncSession = Depends(get_db)):
    '''Fetch past period duration of forex exchange data between two countries'''

    try:
        current_time = datetime.now()
        limit_time = current_time - parse_period(period)

        query = select(Quote).filter(
            Quote.from_country == from_country,
            Quote.to_country == to_country,
            Quote.date >= limit_time,
            Quote.date <= current_time
        )
    
        result = await db.execute(query)
        quotes = result.fetchall()

        response = jsonable_encoder(quotes)
        return response

    except Exception as _:
        tb = traceback.format_exc()
        logger.error(tb)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

    finally:
        await db.close()

