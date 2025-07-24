from fastapi import FastAPI
from app.router.users import router as users_router
from app.router.auth import router as auth_router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
async def main():
    return {"greetings": "Hello world"}
