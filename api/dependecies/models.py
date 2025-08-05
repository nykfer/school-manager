from sqlmodel import SQLModel, Field, Column, DateTime, func
from datetime import date
import datetime

class Teacher(SQLModel, table=True):
    teacher_id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    subject_id: int = Field(default=None, foreign_key="subject.subject_id")
    class_id: int | None = Field(default=None, foreign_key="class.class_id")
    added: date = Field(default_factory=date.today)

class Schooler(SQLModel, table=True):
    schooler_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int = Field(index=True)
    class_id: int | None = Field(default=None, foreign_key="class.class_id")
    added: date = Field(default_factory=date.today)
    
class Admin(SQLModel, table=True):
    admin_id: int | None = Field(default=None, primary_key=True)
    name: str
    added: date = Field(default_factory=date.today)
    
class Subject(SQLModel, table=True):
    subject_id: int | None = Field(default=None, primary_key=True)
    name: str
    added: date = Field(default_factory=date.today)
    
class Class(SQLModel, table=True):
    class_id: int | None = Field(default=None, primary_key=True)
    name: str
    teacher_id: int = Field(foreign_key="teacher.teacher_id")
    added: date = Field(default_factory=date.today)
    
class Assignment(SQLModel, table=True):
    assignment_id: int | None = Field(default=None, primary_key=True)
    teacher_id: int = Field(foreign_key="teacher.teacher_id", index=True)
    subject_id: int = Field(foreign_key="subject.subject_id", index=True)
    title: str
    description: str
    assign_type: str = Field(index=True)
    deadline: date
    added: date
    # added:datetime = Field(
    #     sa_column=Column(
    #         DateTime(timezone=True),
    #         index=True,
    #         server_default=func.now(),
    #         onupdate=func.now()
    #         )
    #     ) #where assign was added
    
class SchoolerAssignmentSubmission(SQLModel, table=True):
    submitted_assignment_id: int | None = Field(primary_key=True)
    schooler_id: int = Field(foreign_key="schooler.schooler_id")
    assignment_id: int = Field(foreign_key="assignment.assignment_id") 
    work: str = Field(description="work that schoolers handed in")
    submitted: date
    grade: int | None = Field(default=None)