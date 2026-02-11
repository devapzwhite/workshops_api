from fastapi import APIRouter

router = APIRouter(prefix="/workshops", tags=["workshops"])


@router.get("/")
def get_workshops():
    return {"workshop": "workshop"}
