from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import crud
import schemas

router = APIRouter()

@router.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db=db, student=student)

@router.post("/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud.get_group_by_name(db, name=group.name)
    if db_group:
        raise HTTPException(status_code=400, detail="Group name already exists")
    return crud.create_group(db=db, group=group)

@router.get("/students/{student_id}", response_model=schemas.StudentWithGroups)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.get("/groups/{group_id}", response_model=schemas.Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    success = crud.delete_student(db, student_id=student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

@router.delete("/groups/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    success = crud.delete_group(db, group_id=group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"message": "Group deleted successfully"}

@router.get("/students/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@router.get("/groups/", response_model=List[schemas.Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = crud.get_groups(db, skip=skip, limit=limit)
    return groups

@router.post("/students/{student_id}/groups/{group_id}")
def add_student_to_group(student_id: int, group_id: int, db: Session = Depends(get_db)):
    result = crud.add_student_to_group(db, student_id=student_id, group_id=group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student or group not found")
    return {"message": "Student added to group successfully"}

@router.delete("/students/{student_id}/groups/{group_id}")
def remove_student_from_group(student_id: int, group_id: int, db: Session = Depends(get_db)):
    result = crud.remove_student_from_group(db, student_id=student_id, group_id=group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student or group not found")
    return {"message": "Student removed from group successfully"}

@router.get("/groups/{group_id}/students/", response_model=List[schemas.Student])
def get_students_in_group(group_id: int, db: Session = Depends(get_db)):
    students = crud.get_students_in_group(db, group_id=group_id)
    return students

@router.post("/students/{student_id}/transfer/")
def transfer_student(
    student_id: int, 
    transfer: schemas.GroupTransfer, 
    db: Session = Depends(get_db)
):
    result = crud.transfer_student(
        db, 
        student_id=student_id, 
        from_group_id=transfer.from_group_id, 
        to_group_id=transfer.to_group_id
    )
    if not result:
        raise HTTPException(status_code=404, detail="Student or groups not found")
    return {"message": "Student transferred successfully"}