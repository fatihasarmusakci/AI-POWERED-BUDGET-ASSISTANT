from sqlalchemy import Column, String, SmallInteger, Decimal, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base # Bunu birazdan oluşturacağız

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(500), nullable=False)
    city = Column(String(255))
    country = Column(String(255))
    address = Column(String)
    star_rating = Column(SmallInteger)
    latitude = Column(Decimal(9, 6))
    longitude = Column(Decimal(9, 6))
    pinecone_id = Column(String(255)) # Vektör DB referansı
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
