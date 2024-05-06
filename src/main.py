import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import all_routers
from src.parser import Fetcher
from config import SERVER_IP_PHONE, SERVER_IP_HOME

app = FastAPI()
pars = Fetcher()

for router in all_routers:
    app.include_router(router)

# 192.168.0.197

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://0.0.0.0",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start_server():
    uvicorn.run(app, host=SERVER_IP_HOME, port=8000)

if __name__ == '__main__':
    start_server()

git