from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from users.router import router as users_router
from groups.router import router as group_router
from events.router import router as events_router
from forum.router import router as forum_router
from files.router import router as files_router

app = FastAPI()
app.include_router(users_router)
app.include_router(group_router, prefix="/groups")
app.include_router(events_router, prefix="/events")
app.include_router(forum_router)
app.include_router(files_router, prefix="/files")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:4201",
        "http://localhost:8000",
        "http://localhost:4200",
        "http://localhost:4201"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CspMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src *;"
        return response


app.add_middleware(CspMiddleware)


class COOPCOEPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
        response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
        return response


app.add_middleware(COOPCOEPMiddleware)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        return response


app.add_middleware(LoggingMiddleware)


@app.get("/")
async def read_root():
    response = JSONResponse(content={"message": "Hello, World!"})
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self';"
    )
    return response
