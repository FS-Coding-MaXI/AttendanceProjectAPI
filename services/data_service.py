import logging
from fastapi import FastAPI, HTTPException
from typing import Dict
import os
import datetime

app = FastAPI()

IMAGES_FOLDER = "./images"

logging.basicConfig(level=logging.DEBUG)

def getPhotosByMonth() -> Dict[str, int]:
    try:
        photo_counts_by_month = {}

        for student_folder in os.listdir(IMAGES_FOLDER):
            student_path = os.path.join(IMAGES_FOLDER, student_folder)
            if os.path.isdir(student_path):
                for file in os.listdir(student_path):
                    file_path = os.path.join(student_path, file)
                    modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    month = modified_time.strftime("%B")

                    if month not in photo_counts_by_month:
                        photo_counts_by_month[month] = 1
                    else:
                        photo_counts_by_month[month] += 1

        return photo_counts_by_month
    
    except Exception as e:
        logging.error(f"Error reading images folder: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read images folder: {str(e)}")

