from fastapi import APIRouter, Path, Query, status
from typing import Annotated
from contextlib import asynccontextmanager

"""Loging"""
from logging import info
import logging

"""FastAPI's dependecies and models"""
from ..dependecies.models import Teacher, Assignment, Subject
from ..dependecies.dependency import SessionDep

"""Imports for postgres db"""
from ...database.postgres.db import create_db_and_tables

"""Imports for mongodb"""
from ...database.mongodb.db import database, collection

router: APIRouter = APIRouter() 

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def db_lifespan(app:APIRouter):
    try:
        create_db_and_tables()
    except Exception as e:
        print(f"Error loading postgres {e}")
    
    app.db = database
    ping_response = await app.db.command("ping")
    
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        info("Connected to database cluster.")
    
    yield
    
    await app.client.close()
    
router: APIRouter = APIRouter(lifespan=db_lifespan)

# Example adding to postgres

@router.post("/heroes/")
def create_hero(hero: Teacher, session: SessionDep) -> Teacher:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

# Post calls for teachers
@router.post("/add/{exercise}/", status_code=status.HTTP_201_CREATED)
async def post_exercise(exercise: Annotated[str, Path(
                                           title="Adding exercise" 
                                            )]):
    pass

@router.post("/")
async def post_note():
    pass

#Post calls for schoolers

@router.post("/")
async def post_homework():
    pass

@router.post("/")
async def post_question():
    pass

# Post calls for admins

@router.post("/")
async def post_user():
    pass

@router.post("/")
async def post_news():
    pass