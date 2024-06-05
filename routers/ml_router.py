import logging
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import cv2
import numpy as np

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db


from schemas.user_schema import UserPublic
from services.meeting_service import fetch_meeting_by_current_time
from services.ml_service import detect_faces
from repositories.student_repository import get_student_classes
from repositories.meeting_repository import get_current_meeting_by_class_id, update_meeting_student_attendance
from services.user_service import get_current_user

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post("/ml/", response_class=JSONResponse)
async def ml_endpoint(file: UploadFile = File(...), current_user: UserPublic = Depends(get_current_user)):
    contents = await file.read()    
    nparr = np.frombuffer(contents, np.uint8)        
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    detected_people = detect_faces(img)
    logging.debug(f"Detected people: {detected_people}")

    response_json = [
    {"id": id, "name": name, "role": role}
    for id, name, role in detected_people
    ]
    for id, _, role in detected_people:
        if role == "teacher":
            continue              
        try:  
            ongoing_meeting = fetch_meeting_by_current_time(current_user.id)
        except:
            return JSONResponse(content={"detected_people": response_json})
        logging.debug(f"Ongoing meeting: {ongoing_meeting}")
        if ongoing_meeting:
            update_meeting_student_attendance(id, ongoing_meeting["id"], True)    

    return JSONResponse(content={"detected_people": response_json})
