from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from mutant_app.services.mutant_service import is_mutant
from mutant_app.repositories.dna_repository import DNARepository

class DnaRequest(BaseModel):
    dna: list[str]

class MutantController:
    def __init__(self):
        self.router = APIRouter()
        self.repository = DNARepository()
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/", self.detect_mutant, methods=["POST"])
        self.router.add_api_route("/stats", self.get_stats, methods=["GET"])

    async def detect_mutant(self, dna_request: DnaRequest):
        dna_sequence = dna_request.dna

        # Validar que la secuencia de ADN no está vacía
        if not dna_sequence:
            raise HTTPException(status_code=400, detail="DNA sequence is required")

        # Verificar si la secuencia de ADN corresponde a un mutante
        if is_mutant(dna_sequence):
            # Guardar el registro en la base de datos si es mutante
            self.repository.save_dna_record(dna_sequence, is_mutant=True)
            return {"status": "Mutant detected"}
        else:
            # Guardar el registro en la base de datos si no es mutante
            self.repository.save_dna_record(dna_sequence, is_mutant=False)
            raise HTTPException(status_code=403, detail="Not a mutant")

    async def get_stats(self):
        stats = self.repository.get_stats()
        return stats

# Instancia del controlador y su enrutador
mutant_controller = MutantController()
router = mutant_controller.router