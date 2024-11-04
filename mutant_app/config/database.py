import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from models.dna_model import Base

# Cargar las variables de entorno
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env'))
load_dotenv(env_path)

# Configuración de conexión a MySQL
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DB = os.getenv('MYSQL_DB')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# URI de conexión a la base de datos
DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'


def check_mysql_service():
    """Verifica si el servicio MySQL está activo."""
    temp_engine = create_engine(DATABASE_URI)
    try:
        with temp_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except OperationalError:
        return False
    finally:
        temp_engine.dispose()


class Database:
    _instance = None

    def __init__(self):
        print("Connecting TO: ", DATABASE_URI)
        
        # Intentar conectar a la base de datos, con reintentos en caso de fallo
        for attempt in range(5):  # Intentar 5 veces
            try:
                self.engine = create_engine(DATABASE_URI)
                self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
                if self.check_connection():
                    print("Database connected.")
                break  
            except OperationalError as e:
                print(f"Attempt {attempt + 1}: Error connecting to the database: {e}")
                time.sleep(5)  # Esperar 5 segundos antes de volver a intentar
        else:
            raise Exception("Unable to connect to the database after multiple attempts.")

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
            raise

    def close_session(self):
        if hasattr(self, "_session"):
            self._session.close()
            del self._session

    def check_connection(self):
        """Verifica si la conexión con la base de datos es posible."""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Connection established.")
            return True
        except OperationalError as e:
            print(f"Error connecting to database: {e}")
            return False
