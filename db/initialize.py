import os
from sqlalchemy import create_engine

db_name = os.getenv('DB_NAME')
host = os.getenv('HOST')
port = os.getenv('PORT')
username = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')
ssl_mode = os.getenv('SSL_MODE')

def get_db_connection():
    engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{db_name}")
    # Test the connection
    connection = engine.connect()

    return connection
