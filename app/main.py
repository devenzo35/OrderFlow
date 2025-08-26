from fastapi import FastAPI, Request
from app.router.v1.users import router as v1_users_router
from app.router.v1.user_auth import router as v1_auth_router
from app.router.v1.movements import router as v1_movements_router
from app.router.v1.categories import router as v1_categories_router
from app.router.v1.exports import router as v1_reports_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler


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

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

app.add_middleware(CORSMiddleware, allow_origins=origins)


@app.get("/")
@limiter.limit("10/minute")  # type: ignore
async def main(request: Request) -> dict[str, str | list[str]]:
    return {"Message": "Welcome to Order Flow API", "Available versions": ["/api/v1"]}
