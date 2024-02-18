from fastapi import FastAPI
from src.api.routers import router as page_router


app = FastAPI()
app.include_router(page_router)


