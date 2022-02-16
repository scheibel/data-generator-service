
from fastapi import APIRouter, Response, BackgroundTasks, File, UploadFile
from fastapi import HTTPException, status, Depends, WebSocket
from fastapi.responses import FileResponse, StreamingResponse, PlainTextResponse

import random
import websockets

router = APIRouter()


def generate_header():
    x = "x"
    y = "y"
    z = "z"

    yield f"{x},{y},{z}\n"

def generate_n(n):
    for i in range(n):
        x = random.randrange(0, 256)
        y = random.randrange(0, 256)
        z = random.randrange(0, 256)
        yield f"{x},{y},{z}\n"

def generate_infinite(break_check):
    while not break_check():
        x = random.randrange(0, 256)
        y = random.randrange(0, 256)
        z = random.randrange(0, 256)
        yield f"{x},{y},{z}\n"

def generate_full_n(n):
    yield from generate_header()
    yield from generate_n(n)

def generate_full_infinite(break_check):
    yield from generate_header()
    yield from generate_infinite(break_check)


# ROOT

@router.get("/", tags=[""])
async def api_get_root():
    return {}


@router.post("/seed", tags=[""])
async def api_post_seed(seed: str):
    random.seed(seed)


@router.get("/csv/file/as/download", tags=["csv", "file", "download"])
async def api_get_csv_download():

    return FileResponse("./data/test.csv", filename="test.csv", media_type="text/csv")


@router.get("/csv/file/as/stream", tags=["csv", "file", "stream"])
async def api_get_csv_download():

    def file_streaming():
        with open("./data/test.csv", mode="r") as file_like:
            yield from file_like

    return StreamingResponse(file_streaming(), media_type="text/csv")


@router.get("/csv/generator_n/as/download", tags=["csv", "generator", "stream"])
async def api_get_csv_download(n: int = 100):
    content = ""
    for s in generate_full_n(n):
        content += s
    
    return PlainTextResponse(content, media_type="text/csv")


@router.get("/csv/generator_n/as/stream", tags=["csv", "generator", "stream"])
async def api_get_csv_download(n: int = 100):

    return StreamingResponse(generate_full_n(n), media_type="text/csv")


@router.websocket("/csv/generator_n/as/websocket")
async def api_get_csv_download(websocket: WebSocket, n: int = 100):
    await websocket.accept()
    
    try:
        for s in generate_full_n(n):
            await websocket.send_text(s)
        
        await websocket.close()
    except websockets.exceptions.ConnectionClosedError:
        pass


@router.get("/csv/generator_infinite/as/stream", tags=["csv", "generator", "stream"])
async def api_get_csv_download():
    def break_check():
        return False

    return StreamingResponse(generate_full_infinite(break_check), media_type="text/csv")


@router.websocket("/csv/generator_infinite/as/websocket")
async def api_get_csv_download(websocket: WebSocket):
    def break_check():
        return False
    
    await websocket.accept()
    
    try:
        for s in generate_full_infinite(break_check):
            await websocket.send_text(s)
        
        await websocket.close()
    except websockets.exceptions.ConnectionClosedError:
        pass
