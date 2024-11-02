from fastapi import FastAPI
from mutant_app.controllers.mutant_controller import router as mutant_router

app = FastAPI()

app.include_router(mutant_router, prefix="/mutant", tags=["Mutants"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Mutant Detection API"}