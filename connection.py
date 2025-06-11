from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = os.getenv("DB_PORT")
DB_NAME     = os.getenv("DB_NAME")


# MYSQL URL STANDARD = "mysql+pymysql://{ROOT_USERNAME}:{ROOT_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# WHEN CONNECTING TO THE DOCKER MYSQL SERVER EXTERNALLY
DATABASE_URL = (f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"f"@{DB_HOST}:{DB_PORT}/{DB_NAME}")
engine = create_engine(DATABASE_URL)


# WHEN CONNECTING TO THE DOCKER MYSQL SERVER INTERNALLY
# engine = create_engine("mysql+pymysql://root:password@db:3306/ncair_api")

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
