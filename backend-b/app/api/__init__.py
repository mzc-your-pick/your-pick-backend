from fastapi import APIRouter
from .programs import router as programs_router
from .topics import router as topics_router
from .votes import router as votes_router
from .results import router as results_router
from .comments import router as comments_router

api_router = APIRouter()
api_router.include_router(programs_router, tags=["programs"])
api_router.include_router(topics_router, tags=["topics"])
api_router.include_router(votes_router, tags=["votes"])
api_router.include_router(results_router, tags=["results"])
api_router.include_router(comments_router, tags=["comments"])

__all__ = ["api_router"]
