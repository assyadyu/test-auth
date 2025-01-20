from fastapi import (
    APIRouter,
    FastAPI,
)

from app.users.routers import user_router


def bind_routers(app: FastAPI):
    router = APIRouter(prefix="/api")
    router.include_router(user_router)
    app.include_router(router=router)
