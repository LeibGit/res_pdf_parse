from fastapi import FastAPI
from routers.resume_router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://res-pdf-parse.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


app.include_router(router)