from api.routers.items import router
from fastapi import FastAPI

app = FastAPI()

app.include_router(router)

