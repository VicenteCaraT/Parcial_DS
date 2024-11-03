import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from models.dna_model import Base

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env'))
load_dotenv(env_path)

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DB = os.getenv('MYSQL_DB')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# URI de conexión a la base de datos
DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'

class Database: 
    _instance = None
    print(f"Connecting to database at: {DATABASE_URI}")
    
    def __init__(self):
        self._create_database_if_not_exists()
        
        self.engine = create_engine(DATABASE_URI)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        if self.check_connection():
            self.create_tables()

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def get_session(self) -> Session:
        if not hasattr(self, '_session') or self._session is None:
            self._session = self.SessionLocal()
        return self._session

    def drop_database(self):
        try:
            Base.metadata.drop_all(self.engine)
            print("Tables dropped.")
        except Exception as e:
            print(f"Error dropping tables: {e}")

    def create_tables(self):
        try:
            Base.metadata.create_all(self.engine)
            print("Tables created.")
        except Exception as e:
            print(f"Error creating tables: {e}")

    def close_session(self):
        if hasattr(self, "_session"):
            self._session.close()
            del self._session

    def check_connection(self):
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Connection established.")
            return True
        except OperationalError as e:
            print(f"Error connecting to database: {e}")
            return False

    def _create_database_if_not_exists(self):
        temp_database_uri = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/'
        temp_engine = create_engine(temp_database_uri)
        
        try:
            with temp_engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}"))
            print(f"Database '{MYSQL_DB}' checked/created successfully.")
        except Exception as e:
            print(f"Error creating database '{MYSQL_DB}': {e}")
        finally:
            temp_engine.dispose()