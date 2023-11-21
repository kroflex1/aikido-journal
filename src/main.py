import uvicorn
from fastapi import FastAPI
from auth.router import router as auth_router
from src.auth import models
from src.database import engine

app = FastAPI()
# models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
