from fastapi import FastAPI
from app.router.users import router as users_router

app = FastAPI()
app.include_router(users_router)


@app.get("/")
async def main():
    return {"greetings": "Hello world"}
