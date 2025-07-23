from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
import uvicorn 
app = FastAPI(
    title="User Management API",
    description="A complete user management system with authentication and authorization",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "User Management API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)