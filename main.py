from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, metadata, database

metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(application: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)