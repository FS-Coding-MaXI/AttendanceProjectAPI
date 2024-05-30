import logging
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import cv2
import numpy as np

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db


from services.ml_service import detect_faces
from repositories.student_repository import get_student_classes
from repositories.meeting_repository import get_current_meeting_by_class_id, update_meeting_student_attendance

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post("/ml/", response_class=JSONResponse)
async def ml_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:        
        contents = await file.read()    
        nparr = np.frombuffer(contents, np.uint8)        
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        detected_people = detect_faces(img)

        for id, _, role in detected_people:
            if role == "teacher":
                continue
            student_classes = get_student_classes(db, id)
            for student_class in student_classes:
                ongoing_meeting = get_current_meeting_by_class_id(student_class["id"])
                if ongoing_meeting:
                    update_meeting_student_attendance(id, ongoing_meeting["id"], True)

        response_json = [
            {"id": id, "name": name, "role": role}
            for id, name, role in detected_people
        ]

        return JSONResponse(content={"detected_people": response_json})

    except Exception as e:        
        return JSONResponse(status_code=500, content={"message": str(e)})
