import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from extend.db import Engin,LocalSession,Base
from apps.user import app_user
from apps.department import app_department
from uploads.users import upload
import os
from fastapi.staticfiles import StaticFiles

# c0tz0kth_1GJNuz1JYiJJfhJ5xpsYkwuSu34orsaP

# c0tz0kth

EXPIRE_MINUTE = 60 * 24

app = FastAPI(
    title="zky系统",
    description="接口描述"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR,'static')
app.mount('/s',StaticFiles(directory=STATIC_DIR))

#跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True
)

#创建数据表结构
Base.metadata.create_all(bind=Engin)

app.include_router(app_user.router)
app.include_router(app_department.router)
app.include_router(upload.router)




if __name__ == '__main__':
    uvicorn.run(app="main:app",reload=True,host="0.0.0.0",port=8080)