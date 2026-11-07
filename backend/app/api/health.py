from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "GetClient backend"}


@router.get("/system-status")
async def system_status() -> dict[str, bool | str]:
    return {
        "app": "GetClient",
        "database_connected": False,
        "message_generation_ready": True,
    }
