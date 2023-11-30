import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import models as auth_models
from auth.router import router as auth_router
from child import models as child_models
from child.router import router as child_router
from group import models as group_models
from group.router import router as group_router
from parent.router import router as parent_router
from src import database

database.db.connect()
database.db.create_tables([auth_models.User])
database.db.create_tables([group_models.Group])
database.db.create_tables([child_models.Child])
database.db.close()

app = FastAPI()

app.include_router(auth_router)
app.include_router(group_router)
app.include_router(child_router)
app.include_router(parent_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
