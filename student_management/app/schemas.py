from pydantic import BaseModel, EmailStr
from typing import List, Optional

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    
    class Config:
        from_attributes = True

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    students: List[Student] = []
    
    class Config:
        from_attributes = True

class StudentWithGroups(Student):
    groups: List[Group] = []

class GroupTransfer(BaseModel):
    from_group_id: int
    to_group_id: int