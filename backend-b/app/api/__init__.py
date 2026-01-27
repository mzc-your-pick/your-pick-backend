from fastapi import APIRouter
from .votes import router as votes_router
from .results import router as results_router

api_router = APIRouter()
api_router.include_router(votes_router, tags=["votes"])
api_router.include_router(results_router, tags=["results"])

__all__ = ["api_router"]
