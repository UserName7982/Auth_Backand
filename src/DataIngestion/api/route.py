from typing import List
from ..VectorIngestion import add_to_db
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from .service import upload_files
from src.Auth.routes import AccessTokenBearer

ingestion=APIRouter(prefix="/app")
@ingestion.post("/upload",dependencies=[Depends(AccessTokenBearer())])
async def upload_file(files: List[UploadFile] = File(...)):
    path=await upload_files(files)
    add_to_db(path)
    return JSONResponse({"message": "File uploaded successfully", "files": path})