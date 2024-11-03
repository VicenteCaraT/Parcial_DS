from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DNARecord(Base):
    __tablename__ = "dna_records"
    
    id = Column(Integer, primary_key=True, index=True)
    dna_sequence = Column(String(255), unique=True, nullable=False) 
    is_mutant = Column(Boolean, nullable=False)
    
    def __repr__(self):
        return f"<DNARecord: [dna_sequence: {self.dna_sequence}, is_mutant: {self.is_mutant}]>"
