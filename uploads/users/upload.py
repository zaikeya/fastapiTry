from fastapi import APIRouter,Depends,File, UploadFile
from fastapi.staticfiles import StaticFiles
from typing import List
from utils.get_token import parse_token
from models.users.user_operation import get_user_by_id
from sqlalchemy.orm import Session
from extend.get_db import get_db
import shutil
import os
from tempfile import NamedTemporaryFile
from pathlib import Path

router = APIRouter(
    prefix="/upload",
    tags=["文件上传"],
    responses={404: {"description": "Not found"}},
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))

STATIC_DIR = os.path.join(BASE_DIR,'static')


UPLOAD_DIRECTORY = os.getcwd()

@router.post("/file",summary='单个文件上传')
async def image(image: UploadFile = File(...),ids:str = Depends(parse_token),db:Session = Depends(get_db)):
    user = get_user_by_id(db, int(ids))
    content = await image.read()
    user_id = user.id
    filename = f'avatars/{user_id}.png'
    if image.content_type != "image/png":
        return {"msg":"图片格式需要为png！"}
    with open (os.path.join(STATIC_DIR,filename),'wb') as f:
        f.write(content)
    return {"msg":"上传成功！","filename":f'/s/{filename}'}



@router.post("/files",summary='多个文件上传')
async def images(images: List[UploadFile] = File(...),ids:str = Depends(parse_token),db:Session = Depends(get_db)):
    user = get_user_by_id(db, int(ids))
    if user:
        for image in images:
            with open(os.path.join(UPLOAD_DIRECTORY, "avatars", image.filename), "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
        return {"filenames": [f"/s/avatars/{file.filename}" for file in images]}