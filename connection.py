from sqlalchemy import create_engine

# MYSQL URL STANDARD = "mysql+pymysql://{ROOT_USERNAME}:{ROOT_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# WHEN CONNECTING TO THE DOCKER MYSQL SERVER EXTERNALLY
engine = create_engine("mysql+pymysql://root:password@localhost:3308/ncair_api")


# WHEN CONNECTING TO THE DOCKER MYSQL SERVER INTERNALLY
# engine = create_engine("mysql+pymysql://root:password@db:3306/ncair_api")
