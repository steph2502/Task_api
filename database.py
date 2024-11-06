from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_URL = 'postgresql://postgres:stephanie214@localhost:5433/tasks_db'

engine = create_engine(DB_URL)

sessionlocal = sessionmaker(bind=engine)
Base = declarative_base()

