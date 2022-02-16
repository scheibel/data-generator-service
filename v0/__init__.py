
import os
import distutils

from fastapi import APIRouter, Request, Response, BackgroundTasks, File, UploadFile
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


try:
    global_rate_unlimited = distutils.util.strtobool(os.environ.get('DATA_GENERATOR_SERVICE_RATE_UNLIMITED', ''))
except:
    global_rate_unlimited = False

def is_rate_unlimited(request: Request):
    return global_rate_unlimited or \
        ("rate_unlimited" in request.scope) and request.scope["rate_unlimited"]


# ROOT

@router.get("/", tags=[""])
async def api_get_root():
    return {}


@router.post("/seed", tags=[""])
async def api_post_seed(seed: str):
    random.seed(seed)


@router.get("/csv/file/as/download", tags=["csv", "file", "download"])
async def api_get_csv_file_download():

    return FileResponse("./data/test.csv", filename="test.csv", media_type="text/csv")


@router.get("/csv/file/as/stream", tags=["csv", "file", "stream"])
async def api_get_csv_file_stream():

    def file_streaming():
        with open("./data/test.csv", mode="r") as file_like:
            yield from file_like

    return StreamingResponse(file_streaming(), media_type="text/csv")


@router.websocket("/csv/file/as/websocket")
async def api_get_csv_file_websocket(websocket: WebSocket):
    await websocket.accept()

    def file_streaming():
        with open("./data/test.csv", mode="r") as file_like:
            yield from file_like
    
    try:
        for s in file_streaming():
            await websocket.send_text(s)
        
        await websocket.close()
    except websockets.exceptions.ConnectionClosedError:
        pass


@router.get("/csv/generator_n/as/download", tags=["csv", "generator", "download"])
async def api_get_csv_generator_n_download(n: int = 100):
    content = ""
    for s in generate_full_n(n):
        content += s
    
    return PlainTextResponse(content, media_type="text/csv")


@router.get("/csv/generator_n/as/stream", tags=["csv", "generator", "stream"])
async def api_get_csv_generator_n_stream(n: int = 100):

    return StreamingResponse(generate_full_n(n), media_type="text/csv")


@router.websocket("/csv/generator_n/as/websocket")
async def api_get_csv_generator_n_websocket(websocket: WebSocket, n: int = 100):
    await websocket.accept()
    
    try:
        for s in generate_full_n(n):
            await websocket.send_text(s)
        
        await websocket.close()
    except websockets.exceptions.ConnectionClosedError:
        pass


@router.get("/csv/generator_infinite/as/stream", tags=["csv", "generator", "stream"])
async def api_get_csv_generator_infinite_stream(request: Request):
    rate_unlimited = is_rate_unlimited(request)
    n = 0

    def break_check():
        nonlocal rate_unlimited
        nonlocal n

        if rate_unlimited:
            return False
        
        n += 1
        return n > 100

    return StreamingResponse(generate_full_infinite(break_check), media_type="text/csv")


@router.websocket("/csv/generator_infinite/as/websocket")
async def api_get_csv_generator_infinite_websocket(websocket: WebSocket):
    rate_unlimited = is_rate_unlimited(websocket)
    n = 0

    def break_check():
        nonlocal rate_unlimited
        nonlocal n

        if rate_unlimited:
            return False
        
        n += 1
        return n > 100
    
    await websocket.accept()

    try:
        for s in generate_full_infinite(break_check):
            await websocket.send_text(s)
        
        await websocket.close()
    except websockets.exceptions.ConnectionClosedError:
        pass
