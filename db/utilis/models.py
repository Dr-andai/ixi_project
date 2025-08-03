from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector 

Base = declarative_base()
metadata = Base.metadata

class ParticipantMetadata(Base):
    __tablename__ = "participant_metadata"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(String, unique=True, index=True)
    age = Column(Integer)
    sex = Column(String)
    height = Column(Integer)
    weight = Column(Integer) 
    site_name = Column(String)

    embeddings = relationship("MRIEmbedding", back_populates="participant", uselist=False)

class MRIEmbedding(Base):
    __tablename__ = 'mri_embeddings'
    id = Column(Integer, primary_key=True)
    participant_id = Column(String, ForeignKey("participant_metadata.participant_id"))
    scan_type = Column(String, nullable=False)  
    embedding = Column(Vector(512), nullable=False)
    
    participant = relationship("ParticipantMetadata", back_populates="embeddings")

