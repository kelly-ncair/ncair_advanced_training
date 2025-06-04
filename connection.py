from sqlalchemy import create_engine
import os # Import the 'os' module to access environment variables

# --- Database Connection Configuration ---

# Get the Database URL from the environment variable set in docker-compose.yml
# If it's not set (e.g., running outside Docker), fall back to the external URL.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3308/ncair_api"
)

print(f"Connecting to database at: {DATABASE_URL}")

# Create the SQLAlchemy engine using the determined URL.
engine = create_engine(DATABASE_URL)

print("Database engine created.")