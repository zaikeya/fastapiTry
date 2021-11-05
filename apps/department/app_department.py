from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from extend.get_db import get_db
from models.users.user_model import Department
from models.users.user_operation import get_user_by_id
from models.department.department_operation import create_department,get_all_department,get_department_by_id,del_department_by_id,update_department_by_id
from utils.get_token import parse_token

router = APIRouter(
    prefix="/department",
    tags=["部门"],
    responses={404: {"description": "Not found"}},
)


@router.post("/add",summary='添加部门')
async def new_department(name:str,leader:str,desc:str,ids:str = Depends(parse_token),db:Session = Depends(get_db)):
     user1 = get_user_by_id(db,int(ids))
     if user1:
        create_department(name,leader,desc)
        content = {"code": 200, "msg": "新建部门成功"}
        return JSONResponse(content=content)
        pass

@router.get("/all",summary='获取所有部门')
async def all_department(id:str = Depends(parse_token),db:Session = Depends(get_db),skip:int = 1, limit: int = 10):
    user = get_user_by_id(db,int(id))
    uu = db.query(Department).all()
    if user:
        department = get_all_department(db,skip,limit)
        meta = {"total":len(uu),"skip":skip,"limit":limit}
        return {"code":200,"departments":department,"meta":meta}
        pass

@router.put('/{id}',summary='更新部门信息')
async def update_department(id:int,name:str,leader:str,desc:str,ids:str = Depends(parse_token),db:Session = Depends(get_db)):
    user1 = get_user_by_id(db,int(ids))
    if user1:
        update_department_by_id(db,id,name,leader,desc)
        content = {"code": 200, "msg": "部门更新成功"}
        return JSONResponse(content=content)
        pass

@router.delete('/{id}',summary='删除部门')
async def remove_department(dep_id:int,db:Session = Depends(get_db),ids:str = Depends(parse_token)):
    user1 = get_user_by_id(db,ids)
    if user1:
        del_department_by_id(db,dep_id)
        content = {"code": 200, "msg": "删除部门成功！"}
        return JSONResponse(content=content)
        pass




