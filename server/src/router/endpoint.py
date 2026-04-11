from fastapi import APIRouter

router = APIRouter()


@router.get("/senator/{senator}")
async def get_senator(senator: str):
    """Get information about a senator"""
    return {"senator": senator}
