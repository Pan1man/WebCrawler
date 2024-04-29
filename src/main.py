import uvicorn
from fastapi import FastAPI
from src.api.routers import all_routers
from src.parser import Fetcher

app = FastAPI()
pars = Fetcher()

for router in all_routers:
    app.include_router(router)


def start_server():
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    start_server()

