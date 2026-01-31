import time
from fastapi import Request
from src.logger import logger

async def add_process_time_header(request:Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    log_dict={
        "path": request.url.path,
        "method": request.method,
        "latency": process_time
    }
    logger.info(log_dict,extra=log_dict)
    response.headers["X-Process-Time"] = str(process_time)
    return response