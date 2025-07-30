from typing import Annotated
from sqlmodel import Session
from fastapi import Depends
from ...database.postgres.db import get_session_db
from enum import Enum
  
SessionDep = Annotated[Session, Depends(get_session_db)]

class Learners(Enum, str):
    schooler = "schooler"
    teacher = "teacher"