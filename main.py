
from fastapi.concurrency import asynccontextmanager

from database import Base, engine
from fastapi import  FastAPI

from routers import posts, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔥 Startup
    print("Hello from aiblogapi!")
    Base.metadata.create_all(bind=engine)

    yield

    # 🔥 Shutdown (optional)
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(posts.Router,prefix="/posts",tags=["posts"])
app.include_router(users.Router,prefix="/users",tags=["users"])

