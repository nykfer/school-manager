

from fastapi import APIRouter, Body, status, HTTPException
from sqlmodel import select
from typing import Annotated
from api.dependecies.models import (
    Class, ClassCreate, ClassPublic,
    Admin, AdminCreate, AdminPublic,
    Teacher, TeacherCreate, TeacherPublic,
    Schooler, SchoolerCreate, SchoolerPublic,
    Subject, SubjectCreate, SubjectPublic,
    Assignment, AssignmentCreate, AssignmentPublic,
    SubmittedAssignment, SubmittedAssignmentCreate, SubmittedAssignmentPublic
)
from api.dependecies.dependency import SessionDep

router_post: APIRouter = APIRouter()

# --- Admin POST ---
@router_post.post(
    "/admins/",
    response_model=AdminPublic,
    status_code=201,
    responses={
        400: {"description": "Invalid request data."},
        409: {"description": "Admin already exists."},
        500: {"description": "Internal server error."}
    }
)
async def create_admin(
    admin: Annotated[AdminCreate, Body(...)],
    session: SessionDep
) -> AdminPublic:
    """
    Create a new admin.

    Args:
        admin (AdminCreate): Admin data to create.
        session (SessionDep): SQLModel session dependency.

    Returns:
        AdminPublic: Newly created admin.

    Status Codes:
        201: Admin created successfully.
        400: Invalid request data.
        409: Admin already exists.
        500: Internal server error.
    """
    # Check for required fields
    if not admin.first_name or not admin.last_name or not admin.email or not admin.age:
        raise HTTPException(status_code=400, detail="All fields are required.")
    # Check for duplicate email
    existing = session.exec(select(Admin).where(Admin.email == admin.email)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Admin already exists.")
    try:
        admin_db = Admin.model_validate(admin)
        session.add(admin_db)
        session.commit()
        session.refresh(admin_db)
        return AdminPublic(**admin_db.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Teacher POST ---
@router_post.post(
    "/teachers/",
    response_model=TeacherPublic,
    status_code=201,
    responses={
        400: {"description": "Invalid request data."},
        409: {"description": "Teacher already exists."},
        500: {"description": "Internal server error."}
    }
)
async def create_teacher(
    teacher: Annotated[TeacherCreate, Body(...)],
    session: SessionDep
) -> TeacherPublic:
    """
    Create a new teacher.

    Args:
        teacher (TeacherCreate): Teacher data to create.
        session (SessionDep): SQLModel session dependency.

    Returns:
        TeacherPublic: Newly created teacher.

    Status Codes:
        201: Teacher created successfully.
        400: Invalid request data.
        409: Teacher already exists.
        500: Internal server error.
    """
    if not teacher.first_name or not teacher.last_name or not teacher.email or not teacher.age or not teacher.subject_id or not teacher.class_id:
        raise HTTPException(status_code=400, detail="All fields are required.")
    # Check for duplicate email
    existing = session.exec(select(Teacher).where(Teacher.email == teacher.email)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Teacher already exists.")
    try:
        teacher_db = Teacher.model_validate(teacher)
        session.add(teacher_db)
        session.commit()
        session.refresh(teacher_db)
        return TeacherPublic(**teacher_db.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Schooler POST ---
@router_post.post(
    "/schoolers/",
    response_model=SchoolerPublic,
    status_code=201,
    responses={
        400: {"description": "Invalid request data."},
        409: {"description": "Schooler already exists."},
        500: {"description": "Internal server error."}
    }
)
async def create_schooler(
    schooler: Annotated[SchoolerCreate, Body(...)],
    session: SessionDep
) -> SchoolerPublic:
    """
    Create a new schooler.

    Args:
        schooler (SchoolerCreate): Schooler data to create.
        session (SessionDep): SQLModel session dependency.

    Returns:
        SchoolerPublic: Newly created schooler.

    Status Codes:
        201: Schooler created successfully.
        400: Invalid request data.
        409: Schooler already exists.
        500: Internal server error.
    """
    if not schooler.first_name or not schooler.last_name or not schooler.email or not schooler.age or not hasattr(schooler, "class_id"):
        raise HTTPException(status_code=400, detail="All fields are required.")
    # Check for duplicate email
    existing = session.exec(select(Schooler).where(Schooler.email == schooler.email)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Schooler already exists.")
    try:
        schooler_db = Schooler.model_validate(schooler)
        session.add(schooler_db)
        session.commit()
        session.refresh(schooler_db)
        return SchoolerPublic(**schooler_db.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Subject POST ---
@router_post.post(
    "/subjects/",
    response_model=SubjectPublic,
    status_code=201,
    responses={
        400: {"description": "Invalid request data."},
        409: {"description": "Subject already exists."},
        500: {"description": "Internal server error."}
    }
)
async def create_subject(
    subject: Annotated[SubjectCreate, Body(...)],
    session: SessionDep
) -> SubjectPublic:
    """
    Create a new subject.

    Args:
        subject (SubjectCreate): Subject data to create.
        session (SessionDep): SQLModel session dependency.

    Returns:
        SubjectPublic: Newly created subject.

    Status Codes:
        201: Subject created successfully.
        400: Invalid request data.
        409: Subject already exists.
        500: Internal server error.
    """
    if not subject.name:
        raise HTTPException(status_code=400, detail="Name is required.")
    # Check for duplicate name
    existing = session.exec(select(Subject).where(Subject.name == subject.name)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Subject already exists.")
    try:
        subject_db = Subject.model_validate(subject)
        session.add(subject_db)
        session.commit()
        session.refresh(subject_db)
        return SubjectPublic(**subject_db.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Class POST ---
@router_post.post(
    "/classes/",
    response_model=ClassPublic,
    status_code=201,
    responses={
        400: {"description": "Invalid request data."},
        409: {"description": "Class already exists."},
        500: {"description": "Internal server error."}
    }
)
async def create_class(
    new_class: Annotated[ClassCreate, Body(...)],
    session: SessionDep
) -> ClassPublic:
    """
    Create a new class.

    Args:
        new_class (ClassCreate): Class data to create.
        session (SessionDep): SQLModel session dependency.

    Returns:
        ClassPublic: Newly created class.

    Status Codes:
        201: Class created successfully.
        400: Invalid request data.
        409: Class already exists.
        500: Internal server error.
    """
    if not new_class.name:
        raise HTTPException(status_code=400, detail="Name is required.")
    # Check for duplicate name
    existing = session.exec(select(Class).where(Class.name == new_class.name)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Class already exists.")
    try:
        class_db = Class.model_validate(new_class)
        session.add(class_db)
        session.commit()
        session.refresh(class_db)
        return ClassPublic(**class_db.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Assignment POST ---
@router_post.post(
    "/assignments/",
    response_model=AssignmentPublic,
    status_code=201,
    responses={
        400: {"description": "Invalid request data."},
        409: {"description": "Assignment already exists."},
        500: {"description": "Internal server error."}
    }
)
async def create_assignment(
    assignment: Annotated[AssignmentCreate, Body(...)],
    session: SessionDep
) -> AssignmentPublic:
    """
    Create a new assignment.

    Args:
        assignment (AssignmentCreate): Assignment data to create.
        session (SessionDep): SQLModel session dependency.

    Returns:
        AssignmentPublic: Newly created assignment.

    Status Codes:
        201: Assignment created successfully.
        400: Invalid request data.
        409: Assignment already exists.
        500: Internal server error.
    """
    if not assignment.teacher_id or not assignment.subject_id or not assignment.title or not assignment.description or not assignment.assign_type or not assignment.deadline:
        raise HTTPException(status_code=400, detail="All fields are required.")
    # Check for duplicate assignment (by title and teacher)
    existing = session.exec(select(Assignment).where(Assignment.title == assignment.title, Assignment.teacher_id == assignment.teacher_id)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Assignment already exists.")
    try:
        assignment_db = Assignment.model_validate(assignment)
        session.add(assignment_db)
        session.commit()
        session.refresh(assignment_db)
        return AssignmentPublic(**assignment_db.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- SubmittedAssignment POST ---
@router_post.post(
    "/assignments/submit/",
    response_model=SubmittedAssignmentPublic,
    status_code=201,
    responses={
        400: {"description": "Invalid request data."},
        409: {"description": "Submission already exists."},
        500: {"description": "Internal server error."}
    }
)
async def submit_assignment(
    submitted_assignment: Annotated[SubmittedAssignmentCreate, Body(...)],
    session: SessionDep
) -> SubmittedAssignmentPublic:
    """
    Submit a schooler's assignment.

    Args:
        submitted_assignment (SubmittedAssignmentCreate): Submitted assignment data.
        session (SessionDep): SQLModel session dependency.

    Returns:
        SubmittedAssignmentPublic: Newly created submitted assignment.

    Status Codes:
        201: Submission created successfully.
        400: Invalid request data.
        409: Submission already exists.
        500: Internal server error.
    """
    if not submitted_assignment.schooler_id or not submitted_assignment.assignment_id or not submitted_assignment.work:
        raise HTTPException(status_code=400, detail="All fields are required.")
    # Check for duplicate submission
    existing = session.exec(select(SubmittedAssignment).where(
        SubmittedAssignment.schooler_id == submitted_assignment.schooler_id,
        SubmittedAssignment.assignment_id == submitted_assignment.assignment_id
    )).first()
    if existing:
        raise HTTPException(status_code=409, detail="Submission already exists.")
    try:
        submitted_assignment_db = SubmittedAssignment.model_validate(submitted_assignment)
        session.add(submitted_assignment_db)
        session.commit()
        session.refresh(submitted_assignment_db)
        return SubmittedAssignmentPublic(**submitted_assignment_db.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))