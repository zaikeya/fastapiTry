from sqlalchemy.orm import Session
from models.users.user_model import Department
from extend.db import LocalSession

def create_department(name:str,leader:str,desc:str):
    sess = LocalSession()
    department = Department()
    department.name = name
    department.leader = leader
    department.desc = desc
    sess.add(department)
    sess.commit()
    pass

def update_department_by_id(db:Session,id:int,name:str,leader:str,desc:str):
    department = db.query(Department).filter(Department.id == id).first()
    if department:
        department.name = name
        department.leader = leader
        department.desc = desc
        db.commit()
        db.close()
        pass

def del_department_by_id(db:Session,id:int):
    department = db.query(Department).filter(Department.id == id).first()
    if department:
        db.delete(department)
        db.commit()
        db.flush()
        pass




def get_department_by_id(db:Session,id:int):
  department = db.query(Department.id,Department.name,Department.leader,Department.state,Department.desc).filter(Department.id == id).first()
  return department

def get_all_department(db:Session,skip:int,limit:int):
    department = db.query(Department.id,Department.name,Department.leader,Department.desc,Department.state).slice((skip-1)*limit,(skip-1)*limit+limit).all()
    return department