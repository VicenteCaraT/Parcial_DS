from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from controllers.mutant_controller import router as mutant_router
from config.database import Database
from sqlalchemy.exc import OperationalError
import time
app = FastAPI()
db = Database()

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
    for _ in range(5):  # Intentar 5 veces
        try:
            db.create_tables()  # Intentar crear tablas
            break  # Si tiene éxito, salir del bucle
        except OperationalError:
            time.sleep(5)  # Esperar 5 segundos antes de volver a intentar


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)