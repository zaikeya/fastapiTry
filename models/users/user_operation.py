#user的数据库操作
from sqlalchemy.orm import Session
from models.users.user_model import User
from extend.db import LocalSession

def create_user(username:str,pwd:str,addr:str,avatar:str):
    sess = LocalSession()
    user = User()
    user.username = username
    user.avatar = avatar
    user.pwd = pwd
    user.addr = addr
    sess.add(user)
    sess.commit()

def get_user_username_and_pwd(db:Session,username:str,md5_pwd:str):
   user = db.query(User.id,User.username,User.avatar,User.ip,User.last_login_date).filter(User.username == username,User.pwd == md5_pwd).first()
   return user


def update_user_by_id(db:Session,id:int,username:str,addr:str,avatar:str):
    user = db.query(User).filter(User.id == id).first()
    if user:
        user.username = username
        user.avatar = avatar
        user.addr = addr
        db.commit()
        db.close()
        pass

def get_user_by_id(db:Session,id:int):
  user = db.query(User.id,User.username,User.avatar,User.ip,User.last_login_date,User.dep_id).filter(User.id == id).first()
  return user

def get_all_user(db:Session,skip:int,limit:int):
    user = db.query(User.id,User.username,User.avatar,User.ip,User.addr,User.state,User.last_login_date).slice((skip-1)*limit,(skip-1)*limit+limit).all()
    return user


def del_user_by_id(db:Session,id:int):
    user = db.query(User).filter(User.id == id).first()
    if user:
        db.delete(user)
        db.commit()
        db.flush()
        pass