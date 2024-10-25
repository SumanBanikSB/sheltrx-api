from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request  
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .routes import user_routes
from app.database import db

client = AsyncIOMotorClient(settings.mongo_uri)
db = client['users']


# limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
# app.state.limiter = limiter

app.include_router(user_routes.router, prefix="/users", tags=["Users"])

# @app.get("/")
# @limiter.limit("5/minute")
# async def index():
#     return {"message": "Welcome"}

# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=["yourdomain.com", "sub.yourdomain.com"]
# )

# @app.get("/")
# async def index(request: Request):
#     return {"message": "Hello, world!"}

@app.middleware("http")
async def set_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response





# from fastapi import FastAPI
# from motor.motor_asyncio import AsyncIOMotorClient

# app = FastAPI()

# # MongoDB URI and database name
# MONGODB_URI = "mongodb+srv://suman33banik:2lWwnZaWwd1HVSzs@cluster0.fmet2.mongodb.net/"  # Replace with your MongoDB URI
# DATABASE_NAME = "test_db"

# # Initialize the MongoDB client
# client = AsyncIOMotorClient(MONGODB_URI)
# db = client[DATABASE_NAME]

# @app.on_event("startup")
# async def startup_db():
#     # Check database connection by creating a collection and inserting a document
#     sample_collection = db["sample_collection"]
    
#     # Define a sample document
#     sample_data = {"name": "John Doe", "email": "johndoe@example.com", "role": "user"}
    
#     # Insert the sample document
#     result = await sample_collection.insert_one(sample_data)
#     print(f"Inserted document ID: {result.inserted_id}")

# @app.get("/")
# async def root():
#     return {"message": "MongoDB connection and insertion test"}
