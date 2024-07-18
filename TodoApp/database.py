from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#   SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:iran1379@localhost/TodoApplicationDatabase' 
#   SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:iran1379@127.0.0.1:3306/TodoApplicationDatabase' 
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todo-app.db'

#   engine = create_engine(url=SQLALCHEMY_DATABASE_URL) # --> Postgresql & Mysql
engine = create_engine(url=SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) #--> sqlite

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()