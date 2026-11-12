import os
from typing import List
import uuid
from src.Auth.Services import UserService
from src.config import configs
from fastapi import HTTPException, UploadFile
from src.DB.Models import document
from ..api.schema import docs

BASE_PATH = configs.BASE_PATH+"/docs"

async def upload_files(files: List[UploadFile], user_service:UserService):
    paths: List[dict] = []
    os.makedirs(BASE_PATH, exist_ok=True)
    try:
        for file in files:
            assert file.filename is not None
            if not file.filename.lower().endswith(('.pdf', '.txt')):
                raise HTTPException(status_code=400, detail={"message": "Invalid file type. Only PDF and TXT files are allowed."})
            file_location = f"{BASE_PATH}/{file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(await file.read())
            paths.append({"filename": file.filename, "path": file_location})
            
        for path in paths:
            if not os.path.exists(path["path"]):
                raise HTTPException(status_code=500, detail={"message": f"File {path['filename']} was not saved successfully."})
            try:
                uid = str(uuid.uuid4())
                doc = document(id=uid, name=path["filename"], path=path["path"])
                await user_service.addDocs(doc)
                path["id"] = uid
            except Exception as e:
                raise HTTPException(status_code=500, detail={"message": f"Failed to save document {path['filename']} to the database.", "error": str(e)})

    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": "File upload failed", "error": str(e)})
    return paths

async def get_All_Documents(user_service: UserService):
        try:
            documents = await user_service.getDocs()
            return documents
        except Exception as e:
            raise HTTPException(status_code=500, detail={"message": "Failed to retrieve documents", "error": str(e)})

async def delete_doc(user_service: UserService, doc_id: str):
    try:
        document= await user_service.deleteDoc(doc_id)
        return docs(id=document.id,filename=document.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": "Failed to delete document", "error": str(e)})

async def get_docs(doc_id: str, user_service: UserService):
    try:
        document= await user_service.getDocById(doc_id)
        if document is None:
                    raise HTTPException(
                        status_code=400,
                        detail="Document not found"
                    )
        return docs(id=document.id,filename=document.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": "Failed to retrieve document", "error": str(e)})