from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .user import Base

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    zone_id_fk = Column(Integer, ForeignKey('zones.id'), nullable=False)
    record_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(10), nullable=False)
    proxied = Column(Boolean, default=False)
    ttl = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    zone = relationship("Zone", back_populates="records")
    updates = relationship("Update", back_populates="record")
