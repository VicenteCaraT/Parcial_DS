from sqlalchemy.orm import Session
from mutant_app.models.dna_model import DNARecord
from mutant_app.config.database import Database

class DNARepository:
    def __init__(self):
        self.db = Database()
        
    def save_dna_record(self, dna_sequence: list, is_mutant: bool):
        # Convertir la lista a una cadena
        dna_sequence_str = ''.join(dna_sequence)  # Une los elementos de la lista sin espacios

        with self.db.get_session() as session:
            new_record = DNARecord(dna_sequence=dna_sequence_str, is_mutant=is_mutant)
            session.add(new_record)
            session.commit()
                
    def get_stats(self):
        with self.db.get_session() as session:
            count_mutant_dna = session.query(DNARecord).filter_by(is_mutant=True).count()
            count_human_dna = session.query(DNARecord).filter_by(is_mutant=False).count()
            total_count = count_mutant_dna + count_human_dna
            ratio = count_mutant_dna / total_count if total_count > 0 else 0
            return {
                "count_mutant_dna": count_mutant_dna,
                "count_human_dna": count_human_dna,
                "ratio": ratio
            }