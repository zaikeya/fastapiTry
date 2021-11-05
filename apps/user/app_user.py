from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from utils.get_md5_data import get_md5_pwd
from models.users.user_model import User
from models.users.user_operation import create_user,get_all_user,get_user_by_id,update_user_by_id,get_user_username_and_pwd,del_user_by_id
from models.department.department_operation import get_department_by_id
from sqlalchemy.orm import Session
from extend.get_db import get_db
from datetime import timedelta
from utils.get_token import create_token,parse_token
from typing import Optional

import os


EXPIRE_MINUTE = 60 * 24

UPLOAD_DIRECTORY = os.getcwd()

router = APIRouter(
    prefix="/user",
    tags=["用户"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register",summary='用户注册')
def register(username:str,pwd:str,addr:str,avatar:Optional[str] = None):
    md5_pwd = get_md5_pwd(pwd)
    create_user(username,md5_pwd,addr,avatar)
    content = {"code": 200, "msg": "注册成功"}
    return JSONResponse(content=content)
    pass

@router.put('/{id}',summary='更新用户信息')
def update_user(id:int,username:str,addr:str,avatar:str,ids:str = Depends(parse_token),db:Session = Depends(get_db)):
    user1 = get_user_by_id(db,int(ids))
    if user1:
        update_user_by_id(db,id,username,addr,avatar)
        content = {"code": 200, "msg": "用户更新成功"}
        return JSONResponse(content=content)
        pass

@router.post("/login",summary='用户登录')
async def Login(user:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
    #1.用户信息获取
    username = user.username
    pwd = user.password
    #密码加密
    md5_pwd = get_md5_pwd(pwd)
    #2.数据库校验
    user = get_user_username_and_pwd(db,username,md5_pwd)
    if user:
        #3.token生成认证
        expire_time = timedelta(minutes=EXPIRE_MINUTE)
        token = create_token({"sub":str(user.id)},expire_time)
        #4.返回token及用户信息(日期格式需要转成字符串)

        ret_user = {"username":user.username,"avatar":user.avatar,"ip":user.ip,"last_login_date":user.last_login_date.strftime("%Y-%m-%d")}
        content = {"code": 200, "msg": "登录成功","token":token,"user":ret_user}
        return JSONResponse(content=content)
        pass
    else:
        content = {"code":500,"msg":"用户名或密码错误"}
        return JSONResponse(content=content)


@router.get("/index",summary='用户信息')
async def get_user(ids:str = Depends(parse_token),db:Session = Depends(get_db)):
    user = get_user_by_id(db,int(ids))
    if user:
        department = get_department_by_id(db,user.dep_id)
        return {"code":200,"user":user,"department":department}
        pass


@router.get("/all",summary='获取所有用户')
async def all_users(ids:str = Depends(parse_token),db:Session = Depends(get_db),skip:int = 1, limit: int = 10):
     user1 = get_user_by_id(db,int(ids))
     uu = db.query(User).all()
     if user1:
         user = get_all_user(db,skip,limit)
         meta = {"total":len(uu),"skip":skip,"limit":limit}
         return {"code":200,"users":user,"meta":meta}
         pass

@router.delete('/{id}',summary='删除用户')
async def remove_user(id:int,ids:str = Depends(parse_token),db:Session = Depends(get_db)):
    user1 = get_user_by_id(db,int(ids))
    if user1:
        del_user_by_id(db,id)
        content = {"code": 200, "msg": "删除用户成功！"}
        return JSONResponse(content=content)
        pass

