from fastapi import APIRouter, Request

router = APIRouter(prefix="/logs")


@router.get("/health", status_code=200)
def get_api_health(request: Request):
    return {"status": "API is healthy."}


@router.get("/jweifjwiefj", status_code=200)
def jweifjwiefj(request: Request):
    return {"jweifjwiefj": "huehuehuehuehue"}