from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

env_mode = os.getenv("ENV_MODE")

if env_mode == "local":
    load_dotenv('.env')
else:
    load_dotenv('.env.docker')
    
connection_string = os.getenv("DB_URL")

engine = create_engine(connection_string)

# MYSQL URL STANDARD = "mysql+pymysql://{ROOT_USERNAME}:{ROOT_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"



# WHEN CONNECTING TO THE DOCKER MYSQL SERVER INTERNALLY
# engine = create_engine("mysql+pymysql://root:password@db:3306/ncair_api")
