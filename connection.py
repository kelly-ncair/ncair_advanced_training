from sqlalchemy import create_engine

# Engine is the main object that connects to the database externally
# engine = create_engine("mysql+pymysql://root:password@localhost:4409/ncair_apk")

# Engine is the main object that connects to the database internally
engine = create_engine("mysql+pymysql://root:password@dbase:3306/ncair_apk")
