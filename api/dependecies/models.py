from sqlmodel import SQLModel, Field
from datetime import datetime

class Teacher(SQLModel, table=True):
    teacher_id:int | None = Field(default=None, primary_key=True)
    name: str 
    age: int 
    subject_id: str | None = Field(default=None, foreign_key=True)
    class_id: int | None = Field(defaut=None, foreign_key=True)
    added: datetime

class Schooler(SQLModel, table=True):
    schooler_id:int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int = Field(index=True)
    class_id: int | None = Field(defaut=None, foreign_key=True)
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
    teacher_id: int = Field(foreign_key=True)
    
class Assignment(SQLModel, table=True):
    assignment_id: int | None = Field(default=None, primary_key=True)
    teacher_id:int = Field(foreign_key=True)
    subject_id:int = Field(foreign_key=True)
    handed_in:int = Field(description="Amount of schoolers that handed in in time")
    handed_late:int = Field(description="Amoun of schoolers that handed in late")
    added: datetime