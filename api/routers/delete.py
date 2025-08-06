from fastapi import APIRouter, Path, status
from typing import Annotated

"""FastAPI's dependecies and models"""
from api.dependecies.models import Teacher, Admin, Schooler, Assignment, SubmittedAssignment, Subject, Class
from api.dependecies.dependency import SessionDep

"""Imports for mongodb"""
from database.mongodb.db import collection

router_delete: APIRouter = APIRouter() 

# Delete assignment by assignment_id
@router_delete.delete("/delete/assignment/{assignment_id}", status_code=status.HTTP_200_OK)
async def delete_asign(
    session:SessionDep,
    assignment_id: Annotated[int, Path()]
)->str:
    
    assignment = session.get(Assignment, assignment_id)
    
    if not assignment:
        return f"Assignment with id {assignment_id} not found."
    
    session.delete(assignment)
    session.commit()
    
    return f"Assignment {assignment} deleted successfully."

# Delete submitted assignment by submitted_assignment_id
@router_delete.delete("/delete/submmited/assignment/{submitted_assignment_id}", status_code=status.HTTP_200_OK)
async def submitted_delete_asign(
    session:SessionDep,
    submitted_assignment_id: Annotated[int, Path()]
)->str:
    """Delete an assignment by assignment_id."""
    assignment = session.get(SubmittedAssignment, submitted_assignment_id)
    
    if not assignment:
        return f"Submitted assignment with id {submitted_assignment_id} not found."
    
    session.delete(assignment)
    session.commit()
    
    return f"Assignment {assignment} deleted successfully."

# Delete class by class_id
@router_delete.delete("/delete/class/{class_id}", status_code=status.HTTP_200_OK)
async def delete_class(
    session: SessionDep,
    class_id: Annotated[int, Path()]
) -> str:
    
    class_obj = session.get(Class, class_id)
    
    if not class_obj:
        return f"Class with id {class_id} not found."
    
    session.delete(class_obj)
    session.commit()
    
    return f"Class {class_obj} deleted successfully."

# Delete subject by subject_id
@router_delete.delete("/delete/subject/{subject_id}", status_code=status.HTTP_200_OK)
async def delete_subject(
    session: SessionDep,
    subject_id: Annotated[int, Path()]
) -> str:
    
    subject = session.get(Subject, subject_id)
    
    if not subject:
        return f"Subject with id {subject_id} not found."
    
    session.delete(subject)
    session.commit()
    
    return f"Subject {subject} deleted successfully."

# Delete schooler by schooler_id
@router_delete.delete("/delete/schooler/{schooler_id}", status_code=status.HTTP_200_OK)
async def delete_schooler(
    session: SessionDep,
    schooler_id: Annotated[int, Path()]
) -> str:
    
    schooler = session.get(Schooler, schooler_id)
    
    if not schooler:
        return f"Schooler with id {schooler_id} not found."
    
    session.delete(schooler)
    session.commit()
    
    return f"Schooler {schooler} deleted successfully."

# Delete teacher by teacher_id
@router_delete.delete("/delete/teacher/{teacher_id}", status_code=status.HTTP_200_OK)
async def delete_teacher(
    session: SessionDep,
    teacher_id: Annotated[int, Path()]
) -> str:
    
    teacher = session.get(Teacher, teacher_id)
    
    if not teacher:
        return f"Teacher with id {teacher_id} not found."
    
    session.delete(teacher)
    session.commit()
    
    return f"Teacher {teacher} deleted successfully."

# Delete admin by admin_id
@router_delete.delete("/delete/admin/{admin_id}", status_code=status.HTTP_200_OK)
async def delete_admin(
    session: SessionDep,
    admin_id: Annotated[int, Path()]
) -> str:
    
    admin = session.get(Admin, admin_id)
    
    if not admin:
        return f"Admin with id {admin_id} not found."
    
    session.delete(admin)
    session.commit()
    
    return f"Admin {admin} deleted successfully."