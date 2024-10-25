from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from routes import user_routes


client = AsyncIOMotorClient(settings.mongo_uri)
db = client['users']


limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter

app.include_router(user_routes.router, prefix="/users", tags=["Users"])

@app.get("/")
@limiter.limit("5/minute")
async def index():
    return {"message": "Welcome"}

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "sub.yourdomain.com"]
)


@app.middleware("http")
async def set_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
