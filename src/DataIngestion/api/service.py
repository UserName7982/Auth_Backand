import os
from typing import List
from src.config import configs
from fastapi import HTTPException, UploadFile

BASE_PATH = configs.BASE_PATH+"/docs"

async def upload_files(files: List[UploadFile]):
    paths: List[dict] = []
    os.makedirs(BASE_PATH, exist_ok=True)
    try:
        for file in files:
            file_location = f"{BASE_PATH}/{file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(await file.read())
            paths.append({"filename": file.filename, "path": file_location})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": "File upload failed", "error": str(e)})
    return paths