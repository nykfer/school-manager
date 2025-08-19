from typing import Annotated
from fastapi import Query
from sqlmodel import Session
from fastapi import Depends
from database.postgres.db import get_session_db
from enum import Enum
from datetime import date
from typing import Union, Optional
  
SessionDep = Annotated[Session, Depends(get_session_db)]

class ComparativeFilter:
    def __init__(
        self, 
        gte: Annotated[Optional[Union[date, int]], Query(description="greater then or equal")]=None,
        gt: Annotated[Optional[Union[date, int]], Query(description="greater then")]=None,
        lte: Annotated[Optional[Union[date, int]], Query(description="less then or equal")]=None,
        lt: Annotated[Optional[Union[date, int]], Query(description="less then")]=None,
        e: Annotated[Optional[Union[date, int]], Query(description="equal")]=None,
    ):
        self.gte = gte
        self.gt = gt
        self.lte = lte
        self.lt = lt
        self.e = e

ComparativeDep = Annotated[ComparativeFilter, Depends(ComparativeFilter)]

class SelectFilter:
    def __init__(
        self,
        offset: Annotated[int, Query()] = 0,
        limit: Annotated[int, Query(le=100)] = 0
        ):
        self.offset = offset
        self.limit = limit
        
SelectDep = Annotated[SelectFilter, Depends(SelectFilter)]
    
class Learners(str, Enum):
    schooler = "schooler"
    teacher = "teacher"    