import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.data_service import getPhotosByMonth


router = APIRouter()

@router.get("/data")
async def get_data():
    try:
        photoData = getPhotosByMonth()
        return JSONResponse(content=photoData)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
