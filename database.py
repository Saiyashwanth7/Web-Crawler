from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values

config=dotenv_values('.env')
POSTGRESQL_DB=config.get('DATABASE_URL')
engine=create_engine(POSTGRESQL_DB)
LocalSession=sessionmaker(bind=engine)
Base=declarative_base()