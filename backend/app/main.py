from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from backend.app.api.auth import router as auth_router
    from backend.app.api.businesses import router as businesses_router
    from backend.app.api.health import router as health_router
    from backend.app.api.organizations import router as organizations_router
    from backend.app.config import settings
except ModuleNotFoundError:  # pragma: no cover - supports running from backend/ directly
    from app.api.auth import router as auth_router
    from app.api.businesses import router as businesses_router
    from app.api.health import router as health_router
    from app.api.organizations import router as organizations_router
    from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="AI-powered outbound prospecting and lead generation platform",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(businesses_router)
app.include_router(organizations_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"app": settings.app_name, "status": "running"}
