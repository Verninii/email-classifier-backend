from fastapi import FastAPI
from app.api.email_routes import router as email_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app = FastAPI(
    title="Email Classifier API",
    version="1.0.0",
)

origins = [
    "https://email-classifier-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"],            
)

@app.get("/")
def read_root():
    return {"message": "API de classificação de emails funcionando!"}

app.include_router(email_router)