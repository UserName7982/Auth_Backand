from typing import List
from ..VectorIngestion import add_to_db
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from .service import get_All_Documents, get_docs, upload_files, delete_doc
from src.Auth.routes import AccessTokenBearer
from src.Auth.Dependancy import RoleChecker
from src.Auth.Services import UserService, getSession
from ..api.schema import docs

role=RoleChecker(role=["admin"])

admin=APIRouter(prefix="/admin")

@admin.post("/upload",dependencies=[Depends(AccessTokenBearer()), Depends(role)])
async def upload_file(files: List[UploadFile] = File(...) ,user_service:UserService=Depends(getSession)):
    path=await upload_files(files, user_service)
    add_to_db(path)
    return JSONResponse({"message": "File uploaded successfully", "files": path})

@admin.delete("/docs/{doc_id}",dependencies=[Depends(AccessTokenBearer()), Depends(role)],response_model=docs)
async def delete_docs(doc_id:str, user_service: UserService = Depends(getSession)):
    return await delete_doc(user_service, doc_id)


@admin.get("/docs/{doc_id}",dependencies=[Depends(AccessTokenBearer()), Depends(role)],response_model=docs)
async def get_doc(doc_id:str,user_service:UserService=Depends(getSession)):
    return await get_docs(doc_id,user_service)

@admin.get("/docs",dependencies=[Depends(AccessTokenBearer()), Depends(role)],response_model=List[docs])
async def get_all_docs(user_service: UserService = Depends(getSession)):
    documents = await get_All_Documents(user_service)
    return [docs(id=Docs.id,filename=Docs.name) for Docs in documents]

# @admin.post("/reindex",dependencies=[Depends(AccessTokenBearer()), Depends(role)])
# async def reindex():
#     pass