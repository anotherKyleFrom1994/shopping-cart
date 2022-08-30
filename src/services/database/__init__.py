from sqlalchemy import create_engine
from databases import Database
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:mysecretpassword@database:5432"

engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)
Base = declarative_base()
