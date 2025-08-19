from sqlmodel import SQLModel, Relationship, Field, Column, DateTime, func
from sqlalchemy import String
from datetime import datetime, date
from typing import Optional, List
from pydantic import EmailStr

class ClassBase(SQLModel):
    name: str = Field(unique=True, nullable=False, sa_type=String(3))
    
class ClassCreate(ClassBase):
    pass

class Class(ClassBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    added: date = Field(default_factory=date.today, nullable=False)
    schoolers: List["Schooler"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete, delete-orphan"},
        back_populates="class_item"
    )

class ClassPublic(ClassBase):
    id: int

class ClassPublicWithUsers(ClassPublic):
    schoolers: List["SchoolerPublic"]
    teacher: "TeacherPublic"

class UserBase(SQLModel):
    first_name: str = Field(nullable=False, sa_type=String(100))
    last_name: str = Field(nullable=False, sa_type=String(100))
    email: EmailStr = Field(nullable=False, unique=True, index=True, sa_type=String(100))
    age: int = Field(nullable=False, gt=0)

class TeacherBase(UserBase):
    class_id: int = Field(nullable=False, unique=True, foreign_key="class.id")
    subject_id: int = Field(nullable=False, foreign_key="subject.id")
    
class TeacherCreate(TeacherBase):
    pass
    
class Teacher(TeacherBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    added: date = Field(default_factory=date.today)
    assignments: List["Assignment"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete, delete-orphan"},
        back_populates="teacher"
    )

class TeacherPublic(TeacherBase):
    id: int

class TeacherPublicWithData(TeacherPublic):
    class_item: ClassPublic
    subject: "SubjectPublic"

class TeacherWithAssignments(TeacherPublic):
    assignments: List["Assignment"]

class SchoolerBase(UserBase):
    class_id: int = Field(foreign_key="class.id")   
     
class SchoolerCreate(UserBase):
    pass
    
class Schooler(SchoolerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    added: date = Field(default_factory=date.today)
    class_item: Class = Relationship(back_populates="schoolers")
    assignments: List["SubmittedAssignment"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete, delete-orphan"},
        back_populates="schooler"
    )
    
class SchoolerPublic(SchoolerBase):
    id: int  

class SchoolerPublicWithClass(SchoolerPublic):
    class_item: ClassPublic

class SchoolerPublicWithAssignments(SchoolerPublic):
    assignments: List["AssignmentPublic"] = []

class AdminCreate(UserBase):
    pass

class Admin(UserBase, table=True):
    admin_id: int | None = Field(default=None, primary_key=True)
    added: date = Field(default_factory=date.today)

class AdminPublic(UserBase):
    admin_id: int

class SubjectBase(SQLModel):
    name: str = Field(unique=True, nullable=False, sa_type=String(100))

class SubjectCreate(SubjectBase):
    pass
    
class Subject(SubjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    added: date = Field(default_factory=date.today)
    assignments: List["Assignment"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete, delete-orphan"},
        back_populates="subject"
    )
        
class SubjectPublic(SubjectBase):
    id: int
    
class SubjectPublicWithAssignments(SubjectPublic):
    assignments: List["AssignmentPublic"] = []
    
class AssignmetBase(SQLModel):
    teacher_id: int = Field(nullable=False, foreign_key="teacher.id")
    subject_id: int = Field(nullable=False, foreign_key="subject.id")
    title: str = Field(nullable=False, sa_type=String(150))
    description: str = Field(nullable=False, sa_type=String(1000))
    assign_type: str = Field(nullable=False, sa_type=String(25))
    deadline: date = Field(nullable=False)
    
class AssignmentCreate(AssignmetBase):
    pass

class Assignment(AssignmetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    added:datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            index=True,
            server_default=func.now(),
            nullable=False
            )
        )
    changed: datetime = Field(sa_column=Column(
        DateTime(timezone=True),
            index=True,
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
    ))
    teacher: Teacher = Relationship(back_populates="assignments")
    subject: Subject = Relationship(back_populates="assignments")
    submitted_assignments: List["SubmittedAssignment"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete, delete-orphan"},
        back_populates="assignment"
    )
    
class AssignmentPublic(AssignmetBase):
    id: int
    added: datetime
    changed: datetime
    
class AssignmentPublicWithData(AssignmentPublic):
    teacher: TeacherPublic
    subject: SubjectPublic
    
class SubmittedAssignmentBase(SQLModel):
    work: str = Field(nullable=False, description="work that schoolers handed in", sa_type=String(15000))
    grade: Optional[int] = Field(default=None)
    schooler_id: int = Field(foreign_key="schooler.id")
    assignment_id: int = Field(foreign_key="assignment.id") 

class SubmittedAssignmentCreate(SubmittedAssignmentBase):
    pass
    
class SubmittedAssignment(SubmittedAssignmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    submitted: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            index=True,
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
            )
        ) 
    schooler: Schooler = Relationship(back_populates="assignments")
    assignment: Assignment = Relationship(back_populates="submitted_assignments")

class SubmittedAssignmentPublic(SubmittedAssignmentBase):
    id: int
    submitted: datetime

class SubmittedAssignmentPublicWithData(SubmittedAssignmentPublic):
    assignment: AssignmentPublic
    schooler: SchoolerPublic