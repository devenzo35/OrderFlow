from fastapi import FastAPI
from app.router.v1.users import router as v1_users_router
from app.router.v1.user_auth import router as v1_auth_router
from app.router.v1.movements import router as v1_movements_router
from app.router.v1.categories import router as v1_categories_router
from app.router.v1.exports import router as v1_reports_router
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:8000",
]

app = FastAPI()
app.include_router(v1_users_router)
app.include_router(v1_auth_router)
app.include_router(v1_movements_router)
app.include_router(v1_reports_router)
app.include_router(v1_categories_router)
app.include_router(v1_reports_router)

app.add_middleware(CORSMiddleware, allow_origins=origins)


@app.get("/")
async def main() -> dict[str, str | list[str]]:
    return {"Message": "Welcome to Order Flow API", "Available versions": ["/api/v1"]}
