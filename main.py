from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routers import write, read


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Bitly URL Shortener", lifespan=lifespan)

app.include_router(write.router)
app.include_router(read.router)
