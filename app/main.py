from fastapi import FastAPI
from app.router.users import router as users_router
from app.router.auth import router as auth_router
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:8000",
]

app = FastAPI()
app.include_router(users_router)
app.include_router(auth_router)

app.add_middleware(CORSMiddleware, allow_origins=origins)


@app.get("/")
async def main():
    return {"greetings": "Hello world"}
