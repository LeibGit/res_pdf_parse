from fastapi import FastAPI
from .routers.resume_router import router

app = FastAPI()

app.include_router(router=router)