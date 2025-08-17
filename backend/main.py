import asyncio
from fastapi import FastAPI

from api import v1

app = FastAPI()
app.include_router(v1.users_router)

@app.get("/async")
async def async_endpoint():
    # await asyncio.sleep(1)  # имитация долгой операции
    return {"message": "Done after 1 sec"}