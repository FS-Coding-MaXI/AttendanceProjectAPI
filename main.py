from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, metadata, database
from routers.user_router import router as user_router
from routers.class_router import router as class_router
from fastapi.middleware.cors import CORSMiddleware

metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(application: FastAPI):
    await database.connect()
    yield
    await database.disconnect()
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_methods=["*"],  
  allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(class_router, prefix="/api/v1", tags=["classes"])