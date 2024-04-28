import threading
import asyncio
import uvicorn
from fastapi import FastAPI
from src.api.routers import all_routers
from src.urlfrontier import url_frontier
from src.parser import Fetcher

app = FastAPI()
pars = Fetcher()

for router in all_routers:
    app.include_router(router)

async def start_parsing():
    while url_frontier.len() != 0:
        await pars.fetch(url_frontier)

def start_server():
    uvicorn.run(app, host='127.0.0.1', port=8000)

def run_parsing():
    asyncio.run(start_parsing())

if __name__ == '__main__':
    parsing_thread = threading.Thread(target=run_parsing)
    parsing_thread.start()
    start_server()
    parsing_thread.join()

