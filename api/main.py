from api.routers.get import router_get
from api.routers.post import router_post
from api.routers.put import router_put
from api.routers.delete import router_delete
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from database.postgres.db import create_db_and_tables
from database.mongodb.db import client, database

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def app_lifespan(app:FastAPI):
    
    app.client = client
    app.db = database
    ping_response = await app.db.command("ping")
    
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        logger.info("Connected to database cluster.")
        
    try:
        create_db_and_tables()
        logger.info("Database tables created or verified.")
    except Exception as e:
        logger.error(f"Error loading postgres {e}")
    
    yield
    
    await app.client.close()
    
app: FastAPI = FastAPI(lifespan=app_lifespan)

app.include_router(router_get)
app.include_router(router_post)
app.include_router(router_put)
app.include_router(router_delete)