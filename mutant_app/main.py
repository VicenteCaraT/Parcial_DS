from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
import time

from controllers.mutant_controller import router as mutant_router
from config.database import Database, check_mysql_service

app = FastAPI()

# Manejo de excepciones personalizado
class InstanceNotFoundError(Exception):
    pass

@app.exception_handler(InstanceNotFoundError)
async def instance_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)},
    )

# Incluye tus routers
app.include_router(mutant_router, prefix='/mutant')

# Inicializa la base de datos y crea tablas al iniciar la app
@app.on_event("startup")
async def startup_event():
    print("Waiting for MySQL service to become available...")
    for _ in range(10):  # Intentar hasta 10 veces
        if check_mysql_service():
            print("MySQL service is active. Initializing Database...")
            db = Database()  # Inicializar la base de datos solo cuando MySQL esté disponible
            db.create_tables()  # Crear las tablas
            break
        else:
            print("MySQL not available yet, retrying in 5 seconds...")
            time.sleep(5)
    else:
        print("MySQL service was not available after multiple attempts.")
        raise Exception("No se pudo conectar a la base de datos después de múltiples intentos.")
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)