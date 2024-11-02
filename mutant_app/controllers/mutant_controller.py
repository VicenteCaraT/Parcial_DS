from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from mutant_app.services.mutant_service import is_mutant

router = APIRouter()

class DnaRequest(BaseModel):
    dna: list[str]

@router.post("/")
async def detect_mutant(dna_request: DnaRequest):
    dna_sequence = dna_request.dna

    # Validar que la secuencia de ADN no está vacía
    if not dna_sequence:
        raise HTTPException(status_code=400, detail="DNA sequence is required")

    # Verificar si la secuencia de ADN corresponde a un mutante
    if is_mutant(dna_sequence):
        return {"status": "Mutant detected"}
    else:
        raise HTTPException(status_code=403, detail="Not a mutant")