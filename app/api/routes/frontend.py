from app.utils import logger

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

import traceback

router = APIRouter()

# Route to serve static frontend HTML
@router.get("/")
async def get_frontend():
    '''Returns the frontend static HTML'''

    try:
        with open("app/static/index.html", "r") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)

    except Exception as _:
        tb = traceback.format_exc()
        logger.error(tb)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

