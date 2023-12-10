import logging.config
import os
import random
import string
import time
from logging import INFO, DEBUG

import uvicorn
from fastapi import FastAPI, Depends, Request

from api.core.auth_handler import JWTBearer
from api.core.env_settings import settings
from api.routers import general, auth

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
app = FastAPI(
    title="API Logger test"
)

logger.info('API is starting up')

@app.post("/")
async def api(request: Request):
    logget.info(f"request.json()")
    logget.debug(f"request.json()")
    logget.trace(f"request.json()")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"message": "OK"})
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"req_id={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    logger.info(f"req_id={idem} completed_in={process_time:.2f}ms status_code={response.status_code}")

    return response

def run():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level=DEBUG)


if __name__ == "__main__":
    run()
