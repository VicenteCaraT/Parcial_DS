import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

class DataBase:
    def __init__(self):
        # Cargar las variables de entorno desde el archivo .env
        env_path = os.path.join(os.path.dirname(__file__), '../.env')
        load_dotenv(env_path)

        # Configuración de la base de datos
        self.database_user = os.getenv('DATABASE_USER')
        self.database_password = os.getenv('DATABASE_PASSWORD')
        self.database_host = os.getenv('DATABASE_HOST')
        self.database_port = os.getenv('DATABASE_PORT')
        self.database_name = os.getenv('DATABASE_NAME')
        
        # URI de la base de datos PostgreSQL
        self.database_uri = f"postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"
        
        # Configuración SQLAlchemy
        self.engine = create_async_engine(self.database_uri, echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_async_session(self) -> AsyncSession: # type: ignore
        async with self.SessionLocal() as session:
            yield session

# Crear una instancia de la clase DataBase
db_conf = DataBase()