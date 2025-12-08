from sqlalchemy.orm import Session
from sqlalchemy import and_
import models
import schemas

# Student CRUD operations
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False

# Group CRUD operations
def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(
        name=group.name,
        description=group.description
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if db_group:
        db.delete(db_group)
        db.commit()
        return True
    return False

# Student-Group relationship operations
def add_student_to_group(db: Session, student_id: int, group_id: int):
    student = get_student(db, student_id)
    group = get_group(db, group_id)
    
    if student and group:
        if group not in student.groups:
            student.groups.append(group)
            db.commit()
            db.refresh(student)
        return student
    return None

def remove_student_from_group(db: Session, student_id: int, group_id: int):
    student = get_student(db, student_id)
    group = get_group(db, group_id)
    
    if student and group:
        if group in student.groups:
            student.groups.remove(group)
            db.commit()
            db.refresh(student)
        return student
    return None

def get_students_in_group(db: Session, group_id: int):
    group = get_group(db, group_id)
    return group.students if group else []

def transfer_student(db: Session, student_id: int, from_group_id: int, to_group_id: int):
    student = get_student(db, student_id)
    from_group = get_group(db, from_group_id)
    to_group = get_group(db, to_group_id)
    
    if student and from_group and to_group:
        if from_group in student.groups:
            student.groups.remove(from_group)
            if to_group not in student.groups:
                student.groups.append(to_group)
            db.commit()
            db.refresh(student)
            return student
    return None

def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()

def get_group_by_name(db: Session, name: str):
    return db.query(models.Group).filter(models.Group.name == name).first()