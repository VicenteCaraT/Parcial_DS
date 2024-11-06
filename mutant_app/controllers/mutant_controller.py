from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError  # Ajusta según tu ORM si es necesario
from services.mutant_service import MutantService
from repositories.dna_repository import DNARepository

class DnaRequest(BaseModel):
    dna: list[str]

class MutantController:
    def __init__(self):
        self.router = APIRouter()
        self.repository = DNARepository()
        self.service = MutantService(self.repository)
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/", self.detect_mutant, methods=["POST"])
        self.router.add_api_route("/stats", self.get_stats, methods=["GET"])

    async def detect_mutant(self, dna_request: DnaRequest):
        dna_sequence = dna_request.dna

        if not dna_sequence:
            raise HTTPException(status_code=400, detail="DNA sequence is required")

        is_mutant = self.service.is_mutant(dna_sequence)

        try:
            self.repository.save_dna_record(dna_sequence, is_mutant=is_mutant)
            
            if is_mutant:
                return {"status": "Mutant detected"}
            else:
                raise HTTPException(status_code=403, detail="Not a mutant")
                
        except IntegrityError:
            # Manejo de excepción por ADN duplicado
            raise HTTPException(status_code=409, detail="ADN duplicated. Entre another ")

    async def get_stats(self):
        stats = self.service.get_stats()
        return stats

mutant_controller = MutantController()
router = mutant_controller.router