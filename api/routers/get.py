from fastapi import APIRouter, Path, Query, Body, status
from typing import Annotated, List, Dict
from datetime import date

"""FastAPI's dependecies and models"""
from api.dependecies.models import Teacher, Admin, Schooler, Assignment, SubmittedAssignment, Subject, Class
from api.dependecies.dependency import SessionDep, ComparativeDep, SelectDep, Learners

"""Imports for postgres db"""
from sqlmodel import select

"""Imports for mongodb"""
from database.mongodb.db import collection

router_get = APIRouter()

"""Get a list of learners (schoolers or theachers) with optional filters for name, age, class, and pagination."""
@router_get.get("/get/learners/list/{learner}", status_code=status.HTTP_200_OK)
async def get_schoolers(
    session:SessionDep,
    select_params: SelectDep,
    comparative_params: ComparativeDep,
    learner: Annotated[Learners, Path(description="schooler or teacher")],
    name: Annotated[str | None, Query(description="Full schooler name")]=None,
    class_id: Annotated[int | None, Query(description="Id of schooler's class")]=None,
    subject_id: Annotated[int | None, Query(description="Subject id for searching speciffic teacher")] = None,
    )->List[Schooler]:
    
    person = Schooler if learner.value == "schooler" else Teacher
    statement = select(person) 
    
    if name is not None:
        statement = statement.where(person.name == name)
        
    if class_id is not None:
        statement = statement.where(person.class_id == class_id)
        
    if comparative_params.gte is not None:
        statement = statement.where(person.age >= comparative_params.gte)
        
    if comparative_params.gt is not None:
        statement = statement.where(person.age > comparative_params.gt)
        
    if comparative_params.lte is not None:
        statement = statement.where(person.age <= comparative_params.lte)
        
    if comparative_params.lt is not None:
        statement = statement.where(person.age < comparative_params.lt)
        
    if comparative_params.e is not None:
        statement = statement.where(person.age == comparative_params.e)
    
    if learner.value == "teacher" and subject_id is not None:
        statement = statement.where(person.subject_id == subject_id) 
    
    statement = statement.offset(select_params.offset).limit(select_params.limit)  
    schoolers = session.exec(statement).all()
    
    return schoolers

"""Get added assignments."""
@router_get.get("/get/assignments/", status_code=status.HTTP_200_OK)
async def get_assign(
    session: SessionDep,
    teacher_id: Annotated[int | None, Query()]=None,
    subject_id: Annotated[int | None, Query()]=None,
    assign_type: Annotated[str | None, Query()] = None,
    gte: Annotated[date | None, Query(description="After or at this day. Only for added (type - date)")]=None,
    gt: Annotated[date | None, Query(description="After this day. Only for added (type - date)")]=None,
    lte: Annotated[date | None, Query(description="Before or at this day. Only for added (type - date)")]=None,
    lt: Annotated[date | None, Query(description="Before this day. Only for added (type - date)")]=None,
    e: Annotated[date | None, Query(description="At this day. Only for added (type - date)")]=None,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 0
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
    
    statement = statement.offset(offset).limit(limit)
    assignments = session.exec(statement=statement).all()
    
    return assignments

"""Get schoolers and their submitted assignments for a given assignment ID, with option to include/exclude late submissions."""
@router_get.get("/get/submitted/assignments/{assign_id}/", status_code=status.HTTP_200_OK)
async def get_submitted_asign(
    session: SessionDep,
    assign_id: Annotated[int, Path(description="""Id of needed assign""")],
    handed_late: Annotated[bool, Query(description="""Exclude or
                                                        include assign that haded in late.
                                                        True means include""")]=True
    )->Dict[
        Schooler,
        SubmittedAssignment
        ]:
    
        try:
            statement = select(Assignment).where(Assignment.assignment_id == assign_id)
            result = session.exec(statement=statement)
            assignment = result.one()
        except Exception as e:
            print(e)

        statement_asign = select(SubmittedAssignment).where(SubmittedAssignment.assignment_id == assign_id)
        statement_schooler = select(Schooler)

        if handed_late == False:
            statement_asign.where(SubmittedAssignment.submitted > assignment.deadline)

        assignments = session.exec(statement=statement_asign).all()

        for assign in assignments:
            statement_schooler = statement_schooler.where(Schooler.schooler_id == assign.schooler_id)

        schoolers = session.exec(statement_schooler).all()

        message ={"Schoolers": schoolers,
                "Submitted Assignments": assignments}

        return message

"""Get a list of classes filtered by name, with pagination support (offset, limit)."""
@router_get.get("/get/classes/", status_code=status.HTTP_200_OK)
async def get_classes(
    session: SessionDep,
    name: Annotated[str | None, Query(description="Class name to search for")] = None,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 0
    ) -> List[Class]:
    
    statement = select(Class)
    
    if name is not None:
        statement = statement.where(Class.name == name)
    
    statement = statement.offset(offset).limit(limit)
    classes = session.exec(statement).all()
    
    return classes

"""Get a list of subjects filtered by name, with pagination support (offset, limit)."""
@router_get.get("/get/subjects/", status_code=status.HTTP_200_OK)
async def get_subjects(
    session: SessionDep,
    name: Annotated[str | None, Query(description="Subject name to search for")] = None,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 0
    ) -> List[Subject]:
    
    statement = select(Subject)
    
    if name is not None:
        statement = statement.where(Subject.name == name)
    
    statement = statement.offset(offset).limit(limit)
    subjects = session.exec(statement).all()
    
    return subjects

"""Get a list of admins filtered by name, with pagination support (offset, limit)."""
@router_get.get("/get/admins/", status_code=status.HTTP_200_OK)
async def get_admins(
    session: SessionDep,
    name: Annotated[str | None, Query(description="Admin name to search for")] = None,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 0
    ) -> List[Admin]:
    
    statement = select(Admin)

    if name is not None:
        statement = statement.where(Admin.name == name)
    
    statement  = statement.offset(offset).limit(limit)
    admins = session.exec(statement).all()

    return admins