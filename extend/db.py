from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

username = "root"
pwd = "Zaikeya0203"
host = "localhost"
port = "3306"
db_name = "zky_system"

url = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(username,pwd,host,port,db_name)

Engin = create_engine(url)

LocalSession = sessionmaker(bind=Engin)

Base = declarative_base()