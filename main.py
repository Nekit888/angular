from fastapi import FastAPI
from interfaces.api import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Movies API")

app.include_router(router, prefix="/api")

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_orgins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

@app.get("/")   
def root():
    return {"message": "Movies API is running"}

#http://127.0.0.1:8000/docs