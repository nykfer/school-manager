from fastapi import APIRouter, Path, Query, status
from typing import Annotated, List, Dict
from contextlib import asynccontextmanager
from datetime import date

"""Loging"""
from logging import info
import logging

"""FastAPI's dependecies and models"""
from ..dependecies.models import Teacher, Admin, Schooler, Assignment, SchoolerAssignmentSubmission, Subject, Class
from ..dependecies.dependency import SessionDep, Learners

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

"""Create a new assignment and add it to the database."""
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

"""Submit a schooler's assignment to the database."""
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

"""Add a new admin to the database."""
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

"""Add a new teacher to the database."""
@router.post("/add/{teacher}/", status_code=status.HTTP_201_CREATED)
async def post_admin(teacher: Annotated[Teacher, Path(
                                           title="Add new Teacher" 
                                            )],
                      session: SessionDep)->str:
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    
    return f"Added new admin - {teacher}"

"""Add a new schooler to the database."""
@router.post("/add/{schooler}/", status_code=status.HTTP_201_CREATED)
async def post_admin(schooler: Annotated[Admin, Path(
                                           title="Add new schooler" 
                                            )],
                      session: SessionDep)->str:
    session.add(schooler)
    session.commit()
    session.refresh(schooler)
    
    return f"Added new admin - {schooler}"

"""Add a new class to the database."""
@router.post("/add/{grade}/", status_code=status.HTTP_201_CREATED)
async def post_admin(grade: Annotated[Class, Path(
                                           title="Add new class" 
                                            )],
                      session: SessionDep)->str:
    session.add(grade)
    session.commit()
    session.refresh(grade)
    
    return f"Added new class - {grade}"

"""Add a new subject to the database."""
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
"""Get a list of learners (schoolers or theachers) with optional filters for name, age, class, and pagination."""
@router.get("/get/learners/list/{learner}")
async def get_schoolers(session:SessionDep,
                        learner: Annotated[Learners, Path(description="schooler or teacher")],
                        name: Annotated[str | None, Query(description="Full schooler name")]=None,
                        gte: Annotated[int | None, Query(description="greate or equal then... Only for age")]=None,
                        gt: Annotated[int | None, Query(description="greate then... Only for age")]=None,
                        lte: Annotated[int | None, Query(description="less or equal then... Only for age")]=None,
                        lt: Annotated[int | None, Query(description="less then... Only for age")]=None,
                        e: Annotated[int | None, Query(description="equal smth (number). Only for age")]=None,
                        class_id: Annotated[int | None, Query(description="Id of schooler's class")]=None,
                        subject_id: Annotated[int | None, Query(description="Subject id for searching speciffic teacher")] = None,
                        offset: int = 0,
                        limit: Annotated[int, Query(le=100)] = 0,)->List[Schooler]:
    
    person = Schooler if learner.value == "schooler" else Teacher
    statement = select(person) 
    
    if name is not None:
        statement = statement.where(person.name == name)
        
    if class_id is not None:
        statement = statement.where(person.class_id == class_id)
        
    if gte is not None:
        statement = statement.where(person.age >= gte)
        
    if gt is not None:
        statement = statement.where(person.age > gt)
        
    if lte is not None:
        statement = statement.where(person.age <= lte)
        
    if lt is not None:
        statement = statement.where(person.age < lt)
        
    if e is not None:
        statement = statement.where(person.age == e)
    
    if learner.value == "teacher" and subject_id is not None:
        statement = statement.where(person.subject_id == subject_id) 
        
    schoolers = session.exec(statement).offset(offset).limit(limit).all()
    
    return schoolers

"""Get added assignments."""
@router.get("/get/assignments/")
async def get_assign(session: SessionDep,
                    teacher_id: Annotated[int | None, Query()]=None,
                    subject_id: Annotated[int | None, Query()]=None,
                    assign_type: Annotated[str | None, Query()] = None,
                    gte: Annotated[date | None, Query(description="After or at this day. Only for added (type - date)")]=None,
                    gt: Annotated[date | None, Query(description="After this day. Only for added (type - date)")]=None,
                    lte: Annotated[date | None, Query(description="Before or at this day. Only for added (type - date)")]=None,
                    lt: Annotated[date | None, Query(description="Before this day. Only for added (type - date)")]=None,
                    e: Annotated[date | None, Query(description="At this day. Only for added (type - date)")]=None,
                        )->List[Assignment]:
    statement = select(Assignment)
    
    if teacher_id is not None:
        statement = statement.where(Assignment.teacher_id == teacher_id)
        
    if subject_id is not None:
        statement = statement.where(Assignment.subject_id == subject_id)
        
    if assign_type is not None:
        statement = statement.where(Assignment.assign_type == assign_type)
        
    if gte is not None:
        statement = statement.where(Assignment.added >= gte)
        
    if gt is not None:
        statement = statement.where(Assignment.added > gt)
        
    if lte is not None:
        statement = statement.where(Assignment.added <= lte)
        
    if lt is not None:
        statement = statement.where(Assignment.added < lt)
        
    if e is not None:
        statement = statement.where(Assignment.added == e)
    
    assignments = session.exec(statement=statement).all()
    
    return assignments

"""Get schoolers and their submitted assignments for a given assignment ID, with option to include/exclude late submissions."""

@router.get("/submitted/assignments/{assign_id}/")
async def get_submitted_asign(session: SessionDep,
                              assign_id: Annotated[int, Path(description="""Id of needed assign""")],
                              handed_late: Annotated[bool, Query(description="""Exclude or
                                                                 include assign that haded in late.
                                                                 True means include""")]=True)->Dict[Schooler,
                                                                                                     SchoolerAssignmentSubmission]:
    
        try:
            statement = select(Assignment).where(Assignment.assignment_id == assign_id)
            result = session.exec(statement=statement)
            assignment = result.one()
        except Exception as e:
            print("exception")

        statement_asign = select(SchoolerAssignmentSubmission).where(SchoolerAssignmentSubmission.assignment_id == assign_id)
        statement_schooler = select(Schooler)

        if handed_late == False:
            statement_asign.where(SchoolerAssignmentSubmission.submitted > assignment.deadline)

        assignments = session.exec(statement=statement_asign).all()

        for assign in assignments:
            statement_schooler = statement_schooler.where(Schooler.schooler_id == assign.schooler_id)

        schoolers = session.exec(statement_schooler).all()

        message ={"Schoolers": schoolers,
                "Submitted Assignments": assignments}

        return message

"""Get a list of classes filtered by name, with pagination support (offset, limit)."""
@router.get("/get/classes/")
async def get_classes(session: SessionDep,
                     name: Annotated[str | None, Query(description="Class name to search for")] = None,
                     offset: int = 0,
                     limit: Annotated[int, Query(le=100)] = 0) -> List[Class]:
    statement = select(Class)
    if name is not None:
        statement = statement.where(Class.name == name)
    classes = session.exec(statement).offset(offset).limit(limit).all()
    return classes

"""Get a list of subjects filtered by name, with pagination support (offset, limit)."""
@router.get("/get/subjects/")
async def get_subjects(session: SessionDep,
                      name: Annotated[str | None, Query(description="Subject name to search for")] = None,
                      offset: int = 0,
                      limit: Annotated[int, Query(le=100)] = 0) -> List[Subject]:
    statement = select(Subject)
    if name is not None:
        statement = statement.where(Subject.name == name)
    subjects = session.exec(statement).offset(offset).limit(limit).all()
    return subjects

"""Get a list of admins filtered by name, with pagination support (offset, limit)."""
@router.get("/get/admins/")
async def get_admins(session: SessionDep,
                    name: Annotated[str | None, Query(description="Admin name to search for")] = None,
                    offset: int = 0,
                    limit: Annotated[int, Query(le=100)] = 0) -> List[Admin]:
    statement = select(Admin)
    if name is not None:
        statement = statement.where(Admin.name == name)
    admins = session.exec(statement).offset(offset).limit(limit).all()
    return admins