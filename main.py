from contextlib import asynccontextmanager

from fastapi import FastAPI
from database import engine, metadata, database
from routers.user_router import router as user_router
from routers.class_router import router as class_router
from routers.student_router import router as student_router
from routers.ml_router import router as ml_router
from routers.main_router import router as main_router
from fastapi.middleware.cors import CORSMiddleware

from database import database, engine, metadata
from routers.class_router import router as class_router
from routers.meeting_router import router as meetings_router
from routers.student_router import router as student_router
from routers.user_router import router as user_router
from scheduler import start_scheduler

metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(application: FastAPI):
    await database.connect()
    start_scheduler()
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
app.include_router(student_router, prefix="/api/v1", tags=["students"])
app.include_router(meetings_router, prefix="/api/v1", tags=["meetings"])
app.include_router(ml_router, prefix="/api/v1", tags=["ml"])
app.include_router(main_router, prefix="/api/v1", tags=["main"])
