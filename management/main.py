import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from management.logger import logger
from management.users.router import router as router_users
from management.healthcheck.router import router as router_healthcheck
from management.auth.router import router as router_auth
from management.settings import DevAppSettings, BaseAppSettings, TestAppSettings

load_dotenv()

app = FastAPI()

app.include_router(router_healthcheck)
app.include_router(router_auth)
app.include_router(router_users)

current_environment = os.getenv('CURRENT_DEVELOPMENT')

settings_ = {"development": DevAppSettings, "testing": TestAppSettings}
settings = settings_[current_environment]() if current_environment else BaseAppSettings()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response
