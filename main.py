import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import create_db
from app.core.error_handles import register_error_handlers
from app.routes import routes
from fastapi.middleware.cors import CORSMiddleware
import colorama

colorama.init(autoreset=True)

@asynccontextmanager
async def init_db(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=init_db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prefix="/api", router=routes)
register_error_handlers(app)


# All routes
if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)