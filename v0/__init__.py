
from fastapi import APIRouter, Response, BackgroundTasks, File, UploadFile
from fastapi import HTTPException, status, Depends
from fastapi.responses import FileResponse, StreamingResponse

router = APIRouter()


# ROOT

@router.get("/", tags=[""])
async def api_get_root():
    return {}
