from sqlmodel import SQLModel, Field
from datetime import datetime

class Teacher(SQLModel, table=True):
    teacher_id:int | None = Field(default=None, primary_key=True)
    name: str 
    age: int 
    subject_id: str | None = Field(default=None, foreign_key="subject.subject_id")
    class_id: int | None = Field(defaut=None, foreign_key="class.class_id")
    added: datetime

class Schooler(SQLModel, table=True):
    schooler_id:int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int = Field(index=True)
    class_id: int | None = Field(defaut=None, foreign_key="class.class_id")
    added: datetime
    
class Admin(SQLModel, table=True):
    admin_id: int | None = Field(default=None, primary_key=True)
    name: str
    added: datetime
    
class Subject(SQLModel, table=True):
    subject_id: int | None = Field(default=None, primary_key=True)
    name: str
    
class Class(SQLModel, table=True):
    class_id: int | None = Field(default=True, primary_key=True)
    teacher_id: int = Field(foreign_key="teacher.teacher_id")
    
class Assignment(SQLModel, table=True):
    assignment_id: int | None = Field(default=None, primary_key=True)
    teacher_id:int = Field(foreign_key="teacher.teacher_id")
    subject_id:int = Field(foreign_key="subject.subject_id")
    title:str
    description:str
    assign_type:str
    deadline:datetime
    added: datetime
    
class SchoolerAssignmentSubmission(SQLModel, table=True):
    schooler_id:int = Field(foreign_key="schooler.schooler_id")
    assignment_id = Field(foreign_key="assignment.assignment_id") 
    submitted:datetime
    grade:int | None = Field(default=None)