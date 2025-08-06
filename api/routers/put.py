from fastapi import APIRouter, Path, Query, status
from typing import Annotated
from datetime import date

"""FastAPI's dependecies and models"""
from api.dependecies.models import Teacher, Admin, Schooler, Assignment, SubmittedAssignment, Subject, Class
from api.dependecies.dependency import SessionDep

"""Imports for postgres db"""
from sqlmodel import select

"""Imports for mongodb"""
from database.mongodb.db import collection

router_put: APIRouter = APIRouter() 

@router_put.put("/update/assignment/{assignment_id}/", status_code=status.HTTP_200_OK)
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

@router_put.put("/give/garde/{grade}/assignment/{submitted_assignment_id}", status_code=status.HTTP_200_OK)
async def give_grade(
    session: SessionDep,
    submitted_assignment_id: Annotated[int, Path()],
    grade: Annotated[int, Path()]
    )->str:
    
    assignment = session.get(SubmittedAssignment, submitted_assignment_id)
    if not assignment:
        return f"Assignment with id {submitted_assignment_id} not found."
    
    assignment.grade = grade
    
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    
    return f"Grade {grade} added successfully to the assignment {assignment}."

""""This is the function for schoolers to update their handed in assignments"""
@router_put.put("/update/submitted/assignment/{assignment_id}/{schooler_id}/work/{work}", status_code=status.HTTP_200_OK)
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
        print(f"Error during finding assignment with {assignment_id} and {schooler_id}: {e}")
        
    assignment.work = work
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    
    return f"Work is updated in the assignment - {assignment}"

# Update class info
@router_put.put("/update/class/{class_id}/", status_code=status.HTTP_200_OK)
async def update_class_info(
    session: SessionDep,
    class_id: Annotated[int, Path()],
    name: Annotated[str | None, Query()] = None,
    teacher_id: Annotated[int | None, Query()] = None
) -> str:
    
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
@router_put.put("/update/subject/{subject_id}/name/{name}", status_code=status.HTTP_200_OK)
async def update_subject_info(
    session: SessionDep,
    subject_id: Annotated[int, Path()],
    name: Annotated[str | None, Path()]
) -> str:
    
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
@router_put.put("/update/schooler/{schooler_id}/", status_code=status.HTTP_200_OK)
async def update_schooler_info(
    session: SessionDep,
    schooler_id: Annotated[int, Path()],
    name: Annotated[str | None, Query()] = None,
    age: Annotated[int | None, Query()] = None,
    class_id: Annotated[int | None, Query()] = None
) -> str:
    
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
@router_put.put("/update/teacher/{teacher_id}/", status_code=status.HTTP_200_OK)
async def update_teacher_info(
    session: SessionDep,
    teacher_id: Annotated[int, Path()],
    name: Annotated[str | None, Query()] = None,
    age: Annotated[int | None, Query()] = None,
    subject_id: Annotated[int | None, Query()] = None,
    class_id: Annotated[int | None, Query()] = None
) -> str:
    
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
@router_put.put("/update/admin/{admin_id}/", status_code=status.HTTP_200_OK)
async def update_admin_info(
    session: SessionDep,
    admin_id: Annotated[int, Path()],
    name: Annotated[str | None, Query()] = None
) -> str:
    
    admin = session.get(Admin, admin_id)
    
    if not admin:
        return f"Admin with id {admin_id} not found."
    if name is not None:
        admin.name = name
        
    session.add(admin)
    session.commit()
    session.refresh(admin)
    
    return f"Admin {admin} updated successfully."