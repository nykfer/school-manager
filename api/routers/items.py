from fastapi import APIRouter, Path, Query, status
from typing import Annotated, List
from contextlib import asynccontextmanager

"""Loging"""
from logging import info
import logging

"""FastAPI's dependecies and models"""
from ..dependecies.models import Teacher, Admin, Schooler, Assignment, SchoolerAssignmentSubmission, Subject, Class
from ..dependecies.dependency import SessionDep

"""Imports for postgres db"""
from ...database.postgres.db import create_db_and_tables
from sqlmodel import select

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
@router.post("/add/{assignment}/", status_code=status.HTTP_201_CREATED)
async def post_assing(assignment: Annotated[Assignment, Path(
                                           title="Adding assingment" 
                                            )],
                      session: SessionDep)->str:
    
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    
    return f"New assingment was added - {assignment}"


#Post calls for schoolers

@router.post("/submit/{assignment}/",status_code=status.HTTP_201_CREATED)
async def submit_assign(assignment: Annotated[SchoolerAssignmentSubmission, Path(
                                           title="Submit assingment" 
                                            )],
                      session: SessionDep)->str:
    
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    
    return f"Assignment submitted successful - {assignment}"

# Post calls for admins

@router.post("/add/{admin}/", status_code=status.HTTP_201_CREATED)
async def post_admin(admin: Annotated[Admin, Path(
                                           title="Add new admin" 
                                            )],
                      session: SessionDep)->str:
    session.add(admin)
    session.commit()
    session.refresh(admin)
    
    return f"Added new admin - {admin}"

@router.post("/add/{grade}/", status_code=status.HTTP_201_CREATED)
async def post_admin(grade: Annotated[Class, Path(
                                           title="Add new class" 
                                            )],
                      session: SessionDep)->str:
    session.add(grade)
    session.commit()
    session.refresh(grade)
    
    return f"Added new class - {grade}"

@router.post("/add/{subject}/", status_code=status.HTTP_201_CREATED)
async def post_admin(subject: Annotated[Subject, Path(
                                           title="Add new subject" 
                                            )],
                      session: SessionDep)->str:
    session.add(subject)
    session.commit()
    session.refresh(subject)
    
    return f"Added new subject - {subject}"

# Get calls for teachers

@router.get("/get/schoolers/list/")
async def get_schoolers(session:SessionDep,
                        name: Annotated[str | None, Query(description="Full schooler name")]=None,
                        gte: Annotated[int | None, Query(description="greate or equal then... Only for age")]=None,
                        gt: Annotated[int | None, Query(description="greate then... Only for age")]=None,
                        lte: Annotated[int | None, Query(description="less or equal then... Only for age")]=None,
                        lt: Annotated[int | None, Query(description="less then... Only for age")]=None,
                        e: Annotated[int | None, Query(description="equal smth (number). Only for age")]=None,
                        class_id: Annotated[int | None, Query(description="Id of schooler's class")]=None,
                        offset: int = 0,
                        limit: Annotated[int, Query(le=100)] = 0,)->List[Schooler]:
    
    statement = select(Schooler)
    
    if name != None:
        statement = statement.where(Schooler.name == name)
        
    if class_id != None:
        statement = statement.where(Schooler.class_id == class_id)
        
    if gte != None:
        statement = statement.where(Schooler.age >= gte)
        
    if gt != None:
        statement = statement.where(Schooler.age > gt)
        
    if lte != None:
        statement = statement.where(Schooler.age <= lte)
        
    if lt != None:
        statement = statement.where(Schooler.age < lt)
        
    if e != None:
        statement = statement.where(Schooler.age == e)
        
    schoolers = session.exec(statement).offset(offset).limit(limit).all()
    
    return schoolers

@router.get("/submitted/assignments/")
async def get_submitted_asign(session: SessionDep,
                              handed_late: Annotated[bool, Query(description="""Exclude or
                                                                 include assign that haded in late.
                                                                 True means include""")]=True)->List[SchoolerAssignmentSubmission]:
    pass