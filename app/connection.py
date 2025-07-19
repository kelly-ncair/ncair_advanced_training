import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus


# Load environment variables
load_dotenv()

env_mode = os.getenv('ENV_MODE')

if env_mode == "local":
    load_dotenv(".env")
else: load_dotenv(".env.docker")
# Get database configuration from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD'))
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Create database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine is the main object that connects to the database internally
engine = create_engine(DATABASE_URL)