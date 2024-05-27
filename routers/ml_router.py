import logging
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, Response
import cv2
import numpy as np
import base64

from services.ml_service import detect_faces

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post("/ml/", response_class=JSONResponse)
async def ml_endpoint(file: UploadFile = File(...)):
    try:        
        contents = await file.read()    
        nparr = np.frombuffer(contents, np.uint8)        
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        detected_people_names,_ = detect_faces(img)
                                        
        return JSONResponse(content={
            "detected_people_names": detected_people_names,            
        })

    except Exception as e:        
        return JSONResponse(status_code=500, content={"message": str(e)})
