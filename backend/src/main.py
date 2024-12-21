from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from users.router import router as users_router


app = FastAPI()
app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://127.0.0.1:4200",
        "http://localhost:8000",
        "http://localhost:4200",
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

@app.get("/")
async def read_root():
    response = JSONResponse(content={"message": "Hello, World!"})
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self';"
    )
    return response

