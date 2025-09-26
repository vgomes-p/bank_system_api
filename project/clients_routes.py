from fastapi import APIRouter

clients_router = APIRouter(prefix="/clients", tags=["clients"])


@clients_router.get("/")
async def home() -> dict:
    """
    This is the standard route for clients.
    All routes for clients needs authentication!
    """
    return {"message": "You access clients -> get data"}

