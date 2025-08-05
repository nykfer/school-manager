from fastapi import APIRouter, Path, Query, Body, status, HTTPException
from typing import Annotated, List, Dict
from datetime import date
from contextlib import asynccontextmanager
import logging

"""FastAPI's dependecies and models"""
from api.dependecies.models import Teacher, Admin, Schooler, Assignment, SubmittedAssignment, Subject, Class
from api.dependecies.dependency import SessionDep, Learners

"""Imports for postgres db"""
from sqlmodel import select
from database.postgres.db import create_db_and_tables
from database.mongodb.db import client, database

"""Imports for mongodb"""
from database.mongodb.db import database, collection

router: APIRouter = APIRouter() 

logger = logging.getLogger(__name__)
@asynccontextmanager
async def app_lifespan(app:APIRouter):
    
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
    
router: APIRouter = APIRouter(lifespan=app_lifespan)

@router.get("/")
async def root():
    return "Hello app"

# Get calls

"""Get a list of learners (schoolers or theachers) with optional filters for name, age, class, and pagination."""
@router.get("/get/learners/list/{learner}")
async def get_schoolers(
    session:SessionDep,
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
    limit: Annotated[int, Query(le=100)] = 0
    )->List[Schooler]:
    
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
    
    assignments = session.exec(statement=statement).offset(offset).limit(limit).all()
    
    return assignments

"""Get schoolers and their submitted assignments for a given assignment ID, with option to include/exclude late submissions."""
@router.get("/get/submitted/assignments/{assign_id}/")
async def get_submitted_asign(
    session: SessionDep,
    assign_id: Annotated[int, Path(description="""Id of needed assign""")],
    handed_late: Annotated[bool, Query(description="""Exclude or
                                                        include assign that haded in late.
                                                        True means include""")]=True
    )->Dict[Schooler,
            SubmittedAssignment
            ]:
    
        try:
            statement = select(Assignment).where(Assignment.assignment_id == assign_id)
            result = session.exec(statement=statement)
            assignment = result.one()
        except Exception as e:
            print("exception")

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
@router.get("/get/classes/")
async def get_classes(
    session: SessionDep,
    name: Annotated[str | None, Query(description="Class name to search for")] = None,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 0
    ) -> List[Class]:
    
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

# Post calls

"""Add a new admin to the database."""
@router.post("/add/admin", status_code=status.HTTP_201_CREATED)
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
@router.post("/add/teacher", status_code=status.HTTP_201_CREATED)
async def post_teacher(
    teacher: Annotated[Teacher,
                       Body(description="""
                            Provide fields for Teacher table:
                            name:str
                            age:int
                            subject_id: int, foreign key
                            """)],
    session: SessionDep)->str:
    
    if not teacher.name or not teacher.age or teacher.subject_id:
        raise HTTPException(status_code=400, detail="Invalid data inputs")
    
    if teacher.name == "":
        raise HTTPException(status_code=400, detail="Name cannot be an empty string")
    
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    
    return f"Added new teacher - {teacher}"

"""Add a new schooler to the database."""
@router.post("/add/schooler", status_code=status.HTTP_201_CREATED)
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
    
    if not schooler.name or not schooler.age:
        raise HTTPException(status_code=400, detail="Invalid data inputs")
    if schooler.name == "":
        raise HTTPException(status_code=400, detail="Name cannot be an empty string")
    
    session.add(schooler)
    session.commit()
    session.refresh(schooler)
    
    return f"Added new schooler - {schooler}"

"""Create a new assignment and add it to the database."""
@router.post("/add/assignment", status_code=status.HTTP_201_CREATED)
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
    if not assignment.title or not assignment.teacher_id or not assignment.subject_id or not assignment.deadline:
        raise HTTPException(status_code=400, detail="Invalid data inputs for assignment")
    
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    
    return f"New assignment was added - {assignment}"

"""Submit a schooler's assignment to the database."""
@router.post("/submit/assignment", status_code=status.HTTP_201_CREATED)
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
@router.post("/add/class", status_code=status.HTTP_201_CREATED)
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
@router.post("/add/subject", status_code=status.HTTP_201_CREATED)
async def post_subject(
    subject: Annotated[Subject,
                       Body(description="""Provide fields for Schooler table:
                            name: str""")],
    session: SessionDep
    )->str:
    if not subject.name:
        raise HTTPException(status_code=400, detail="Invalid data inputs")
    
    session.add(subject)
    session.commit()
    session.refresh(subject)
    
    return f"Added new subject - {subject}"

#update calls

@router.put("/update/{assignment_id}/")
async def update_assign(
    session: SessionDep,
    assignment_id: Annotated[int, Path()],
    title: Annotated[str | None, Query()] = None,
    description: Annotated[str | None, Query()] = None,
    deadline: Annotated[date | None, Query()] = None,
    assign_type: Annotated[str | None, Query()] = None,
    subject_id: Annotated[int | None, Query()] = None,
    teacher_id: Annotated[int | None, Query()] = None,
) -> str:
    assignment = session.get(Assignment, assignment_id)
    if not assignment:
        return f"Assignment with id {assignment_id} not found."
    if title is not None:
        assignment.title = title
    if description is not None:
        assignment.description = description
    if deadline is not None:
        assignment.deadline = deadline
    if assign_type is not None:
        assignment.assign_type = assign_type
    if subject_id is not None:
        assignment.subject_id = subject_id
    if teacher_id is not None:
        assignment.teacher_id = teacher_id
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return f"Assignment {assignment} updated successfully."

@router.put("/give/garde/{grade}/assign/{submitted_assignment_id}")
async def give_grade(
    session: SessionDep,
    submitted_assignment_id: Annotated[int, Path()],
    grade: Annotated[int, Path()]
    )->str:
    
    assignment = session.get(SubmittedAssignment, submitted_assignment_id)
    assignment.grade = grade
    
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    
    return f"Grade {grade} added successfully to the assignment {assignment}."

""""This is the function for schoolers to update their handed in assignments"""
@router.put("/update/submitted/assignment/{assignment_id}/{schooler_id}/work/{work}")
async def update_submitted_assign(
    session: SessionDep,
    assignment_id: Annotated[int, Path()],
    schooler_id: Annotated[int, Path()],
    work: Annotated[str, Path()]
    )->str:
    statement = select(SubmittedAssignment).where(SubmittedAssignment.schooler_id == schooler_id)
    statement = statement.where(SubmittedAssignment.assignment_id == assignment_id)
    
    try:
        assignment = session.exec(statement).one()
    except Exception as e:
        print(f"Error during finding assignment with {assignment_id} and {schooler_id}")
        
    assignment.work = work
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    
    return f"Work is updated in the assignment - {assignment}"

# Update class info
@router.put("/update/class/{class_id}/")
async def update_class_info(
    session: SessionDep,
    class_id: Annotated[int, Path()],
    name: Annotated[str | None, Query()] = None,
    teacher_id: Annotated[int | None, Query()] = None
) -> str:
    """Update class information by class_id."""
    class_obj = session.get(Class, class_id)
    if not class_obj:
        return f"Class with id {class_id} not found."
    if name is not None:
        class_obj.name = name
    if teacher_id is not None:
        class_obj.teacher_id = teacher_id
    session.add(class_obj)
    session.commit()
    session.refresh(class_obj)
    return f"Class {class_obj} updated successfully."

# Update subject info
@router.put("/update/subject/{subject_id}/name/{name}")
async def update_subject_info(
    session: SessionDep,
    subject_id: Annotated[int, Path()],
    name: Annotated[str | None, Path()]
) -> str:
    """Update subject information by subject_id."""
    subject = session.get(Subject, subject_id)
    if not subject:
        return f"Subject with id {subject_id} not found."
    if name is not None:
        subject.name = name
    session.add(subject)
    session.commit()
    session.refresh(subject)
    return f"Subject {subject} updated successfully."

# Update schooler info
@router.put("/update/schooler/{schooler_id}/")
async def update_schooler_info(
    session: SessionDep,
    schooler_id: Annotated[int, Path()],
    name: Annotated[str | None, Query()] = None,
    age: Annotated[int | None, Query()] = None,
    class_id: Annotated[int | None, Query()] = None
) -> str:
    """Update schooler information by schooler_id."""
    schooler = session.get(Schooler, schooler_id)
    if not schooler:
        return f"Schooler with id {schooler_id} not found."
    if name is not None:
        schooler.name = name
    if age is not None:
        schooler.age = age
    if class_id is not None:
        schooler.class_id = class_id
    session.add(schooler)
    session.commit()
    session.refresh(schooler)
    return f"Schooler {schooler} updated successfully."

# Update teacher info
@router.put("/update/teacher/{teacher_id}/")
async def update_teacher_info(
    session: SessionDep,
    teacher_id: Annotated[int, Path()],
    name: Annotated[str | None, Query()] = None,
    age: Annotated[int | None, Query()] = None,
    subject_id: Annotated[int | None, Query()] = None,
    class_id: Annotated[int | None, Query()] = None
) -> str:
    """Update teacher information by teacher_id."""
    teacher = session.get(Teacher, teacher_id)
    if not teacher:
        return f"Teacher with id {teacher_id} not found."
    if name is not None:
        teacher.name = name
    if age is not None:
        teacher.age = age
    if subject_id is not None:
        teacher.subject_id = subject_id
    if class_id is not None:
        teacher.class_id = class_id
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    return f"Teacher {teacher} updated successfully."

# Update admin info
@router.put("/update/admin/{admin_id}/")
async def update_admin_info(
    session: SessionDep,
    admin_id: Annotated[int, Path()],
    name: Annotated[str | None, Query()] = None
) -> str:
    """Update admin information by admin_id."""
    admin = session.get(Admin, admin_id)
    if not admin:
        return f"Admin with id {admin_id} not found."
    if name is not None:
        admin.name = name
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return f"Admin {admin} updated successfully."

#delete calls

# Delete assignment by assignment_id
@router.delete("/delete/assignment/{assignment_id}")
async def delete_asign(
    session:SessionDep,
    assignment_id: Annotated[int, Path()]
)->str:
    """Delete an assignment by assignment_id."""
    assignment = session.get(Assignment, assignment_id)
    if not assignment:
        return f"Assignment with id {assignment_id} not found."
    session.delete(assignment)
    session.commit()
    return f"Assignment {assignment} deleted successfully."

# Delete submitted assignment by submitted_assignment_id
@router.delete("/delete/submmited/assignment/{submitted_assignment_id}")
async def submitted_delete_asign(
    session:SessionDep,
    submitted_assignment_id: Annotated[int, Path()]
)->str:
    """Delete an assignment by assignment_id."""
    assignment = session.get(Assignment, submitted_assignment_id)
    if not assignment:
        return f"Submitted assignment with id {submitted_assignment_id} not found."
    session.delete(assignment)
    session.commit()
    return f"Assignment {assignment} deleted successfully."

# Delete class by class_id
@router.delete("/delete/class/{class_id}")
async def delete_class(
    session: SessionDep,
    class_id: Annotated[int, Path()]
) -> str:
    """Delete a class by class_id."""
    class_obj = session.get(Class, class_id)
    if not class_obj:
        return f"Class with id {class_id} not found."
    session.delete(class_obj)
    session.commit()
    return f"Class {class_obj} deleted successfully."

# Delete subject by subject_id
@router.delete("/delete/subject/{subject_id}")
async def delete_subject(
    session: SessionDep,
    subject_id: Annotated[int, Path()]
) -> str:
    """Delete a subject by subject_id."""
    subject = session.get(Subject, subject_id)
    if not subject:
        return f"Subject with id {subject_id} not found."
    session.delete(subject)
    session.commit()
    return f"Subject {subject} deleted successfully."

# Delete schooler by schooler_id
@router.delete("/delete/schooler/{schooler_id}")
async def delete_schooler(
    session: SessionDep,
    schooler_id: Annotated[int, Path()]
) -> str:
    """Delete a schooler by schooler_id."""
    schooler = session.get(Schooler, schooler_id)
    if not schooler:
        return f"Schooler with id {schooler_id} not found."
    session.delete(schooler)
    session.commit()
    return f"Schooler {schooler} deleted successfully."

# Delete teacher by teacher_id
@router.delete("/delete/teacher/{teacher_id}")
async def delete_teacher(
    session: SessionDep,
    teacher_id: Annotated[int, Path()]
) -> str:
    """Delete a teacher by teacher_id."""
    teacher = session.get(Teacher, teacher_id)
    if not teacher:
        return f"Teacher with id {teacher_id} not found."
    session.delete(teacher)
    session.commit()
    return f"Teacher {teacher} deleted successfully."

# Delete admin by admin_id
@router.delete("/delete/admin/{admin_id}")
async def delete_admin(
    session: SessionDep,
    admin_id: Annotated[int, Path()]
) -> str:
    """Delete an admin by admin_id."""
    admin = session.get(Admin, admin_id)
    if not admin:
        return f"Admin with id {admin_id} not found."
    session.delete(admin)
    session.commit()
    return f"Admin {admin} deleted successfully."