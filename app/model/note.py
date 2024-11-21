from sqlmodel import SQLModel, Field
from typing import Optional


class Note(SQLModel, table=True):
    __tablename__ = "note"

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(default=None, nullable=False)
    description: str = Field(default=None, nullable=False)
