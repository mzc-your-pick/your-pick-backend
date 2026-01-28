from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .api import api_router
from .utils.rate_limit import limiter
from .config import settings

# FastAPI 앱 생성
app = FastAPI(
    title="Survival Vote API",
    description="서바이벌 프로그램 대중 투표 API (백엔드 B)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Survival Vote API",
        version="1.0.0",
        description="서바이벌 프로그램 대중 투표 API (백엔드 B)",
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.3"
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Rate Limiter 설정
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 전역 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "INTERNAL_ERROR",
            "message": "서버 오류가 발생했습니다" if not settings.DEBUG else str(exc)
        }
    )


# 라우터 등록
app.include_router(api_router, prefix="/api/v1")


# 헬스체크
@app.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "backend-b",
        "version": "1.0.0"
    }


# 루트
@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Survival Vote API (Backend B)",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
