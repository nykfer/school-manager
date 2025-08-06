from fastapi import APIRouter, Body, status, HTTPException
from typing import Annotated, List

"""FastAPI's dependecies and models"""
from api.dependecies.models import Teacher, Admin, Schooler, Assignment, SubmittedAssignment, Subject, Class
from api.dependecies.dependency import SessionDep

"""Imports for mongodb"""
from database.mongodb.db import collection

router_post: APIRouter = APIRouter() 

"""Add a new admin to the database."""
@router_post.post("/add/admin", status_code=status.HTTP_201_CREATED)
async def post_admin(
    admin: Annotated[Admin, 
                     Body(description="""
                          Provide fields for Teacher table: 
                          name:str""")],
    session: SessionDep
    )->str:
    
    if not admin.name or admin.name == "":
        raise HTTPException(status_code=400, detail="Admin name must be provided")
    
    session.add(admin)
    session.commit()
    session.refresh(admin)
    
    return f"Added new admin - {admin}"

"""Add a new teacher to the database."""
@router_post.post("/add/teacher", status_code=status.HTTP_201_CREATED)
async def post_teacher(
    teacher: Annotated[Teacher,
                       Body(description="""
                            Provide fields for Teacher table:
                            name:str
                            age:int
                            subject_id: int, foreign key
                            """)],
    session: SessionDep)->str:
    
    if not teacher.name or not teacher.age or not teacher.subject_id:
        raise HTTPException(status_code=400, detail="Invalid data inputs")
    
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    
    return f"Added new teacher - {teacher}"

"""Add a new schooler to the database."""
@router_post.post("/add/schooler", status_code=status.HTTP_201_CREATED)
async def post_schooler(
    schooler: Annotated[Schooler,
                        Body(description="""
                             Provide fields for Schooler table:
                             name: str
                             age: int
                             class_id: int, foreign key
                             """)],
    session: SessionDep
    )->str:
    
    if not schooler.name or not schooler.age or not schooler.class_id:
        raise HTTPException(status_code=400, detail="Invalid data inputs")
    
    session.add(schooler)
    session.commit()
    session.refresh(schooler)
    
    return f"Added new schooler - {schooler}"

"""Create a new assignment and add it to the database."""
@router_post.post("/add/assignment", status_code=status.HTTP_201_CREATED)
async def post_assing(
    assignment: Annotated[Assignment, Body(description="""
        Provide fields for Assignment table:
        teacher_id: int
        subject_id: int
        title: str
        description: str
        assign_type: str
        deadline: date
    """)],
    session: SessionDep
) -> str:
    if not assignment.description or not assignment.title or not assignment.teacher_id or not assignment.subject_id or not assignment.deadline or not assignment.assign_type:
        raise HTTPException(status_code=400, detail="Invalid data inputs for assignment")
    
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    
    return f"New assignment was added - {assignment}"

"""Submit a schooler's assignment to the database."""
@router_post.post("/submit/assignment", status_code=status.HTTP_201_CREATED)
async def submit_assign(
    submitted_assignment: Annotated[SubmittedAssignment, Body(description="""
        Provide fields for SubmittedAssignment table:
        schooler_id: int
        assignment_id: int
        work: str
    """)],
    session: SessionDep
) -> str:
    
    if not submitted_assignment.schooler_id or not submitted_assignment.assignment_id or not submitted_assignment.work:
        raise HTTPException(status_code=400, detail="Invalid data inputs for submitted assignment")
    
    session.add(submitted_assignment)
    session.commit()
    session.refresh(submitted_assignment)
    
    return f"Assignment submitted successfully - {submitted_assignment}"


"""Add a new class to the database."""
@router_post.post("/add/class", status_code=status.HTTP_201_CREATED)
async def post_class(
    new_class: Annotated[Class,
                         Body(description="""
                              Provide fields for Schooler table:
                              name:str
                              teacher_id: int, foreign key
                              """)],
    session: SessionDep,
    schoolers: Annotated[List[Schooler] | None, 
                         Body(description="""Provide list of students for the class""")] = None
    )->str:
    
    if not new_class.name or not new_class.teacher_id:
        raise HTTPException(status_code=400, detail=f"Invalid data inputs {new_class}")
    
    if new_class.name == "":
        raise HTTPException(status_code=400, detail="Name cannot be an empty string")
    
    if schoolers is not None:
        new_class.schoolers = schoolers
    
    session.add(new_class)
    session.commit()
    session.refresh(new_class)
    
    return f"Added new class - {new_class}"

"""Add a new subject to the database."""
@router_post.post("/add/subject", status_code=status.HTTP_201_CREATED)
async def post_subject(
    subject: Annotated[Subject,
                       Body(description="""Provide fields for Schooler table:
                            name: str""")],
    session: SessionDep
    )->str:
    if not subject.name or subject.name == "":
        raise HTTPException(status_code=400, detail="Invalid data inputs")
    
    session.add(subject)
    session.commit()
    session.refresh(subject)
    
    return f"Added new subject - {subject}"