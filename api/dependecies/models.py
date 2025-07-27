from sqlmodel import SQLModel, Field

class Teacher(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int = Field(index=True)