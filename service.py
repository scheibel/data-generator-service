from fastapi import FastAPI

from v0 import router as v0_router

app = FastAPI()

app.include_router(
    v0_router,
    # prefix="/v0",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("service:app", host="0.0.0.0", port=9000, log_level="info")
