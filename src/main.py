import uvicorn
from fastapi import FastAPI
from src.api.routers import router as page_router


app = FastAPI()
app.include_router(page_router)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)