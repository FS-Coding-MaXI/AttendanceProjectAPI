import logging
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
import cv2
import numpy as np
import base64

from services.ml_service import detect_faces

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post("/ml/", response_class=Response)
async def ml_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    (detected_people_names, converted_image) = detect_faces(img)

    _, encoded_img = cv2.imencode(".PNG", converted_image)

    encoded_img: bytes = base64.b64encode(encoded_img)

    return Response(
        content=encoded_img,
        media_type="image/png",
        headers={"Detected-names": ";".join(detected_people_names)},
    )
