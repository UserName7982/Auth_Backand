from fastapi import HTTPException
from ..retrival import modelAIResponse
from ..retrival import query_result

async def Response(text: str):
     try:
        Retrivedchunks = await query_result(text)
        RetivedContext = "\n".join([chunk["page_content"] for chunk in Retrivedchunks])
        answer = await modelAIResponse(text, RetivedContext)
        return answer
     except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in query_result: {str(e)}")