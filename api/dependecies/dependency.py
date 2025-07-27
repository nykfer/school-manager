from typing import Annotated
from sqlmodel import Session
from fastapi import Depends
from ...database.postgres.db import get_session_db
  
SessionDep = Annotated[Session, Depends(get_session_db)]