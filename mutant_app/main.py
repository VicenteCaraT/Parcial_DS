from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException

# Importa tu router de controladores
from mutant_app.controllers.mutant_controller import router as mutant_router
from mutant_app.config.database import Database

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

# Inicializa la base de datos y crea tablas
db = Database()
db.create_tables()

# Puedes añadir más rutas aquí si es necesario

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)