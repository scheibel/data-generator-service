from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_key="X-DATA-GENERATOR-KEY", header_value="e5f7b5ea3fea53df2266a64ade09b75a7f3273d0fb1dce11edd90a422728a06e"):
        super().__init__(app)
        self.header_key = header_key
        self.header_value = header_value
    
    async def dispatch(self, request, call_next):
        rate_unlimited = (self.header_key in request.headers) and (request.headers[self.header_key] == self.header_value)
        request.scope['rate_unlimited'] = rate_unlimited
        return await call_next(request)

from v0 import router as v0_router

app = FastAPI()

app.include_router(
    v0_router,
    # prefix="/v0",
)

app.add_middleware(RateLimitMiddleware)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("service:app", host="0.0.0.0", port=9000, log_level="info")
