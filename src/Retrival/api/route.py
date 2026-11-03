from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.Auth.Dependancy import AccessTokenBearer
from src.Retrival.api.service import Response
from src.Retrival.api.schema import ChatRequest

from src.Retrival.api.schema import ChatRequest

retrieval = APIRouter(prefix="/chat")

@retrieval.post("/query",dependencies=[Depends(AccessTokenBearer())])
async def query(chat_request: ChatRequest):
    try:
        result = await Response(chat_request.text)
        return JSONResponse({"message": "Query successful", "result": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in query: {str(e)}")