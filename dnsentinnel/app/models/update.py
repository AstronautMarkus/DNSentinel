from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .user import Base

class Update(Base):
    __tablename__ = 'updates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id_fk = Column(Integer, ForeignKey('records.id'), nullable=False)
    old_ip = Column(String(45), nullable=True)
    new_ip = Column(String(45), nullable=True)
    status = Column(String(20), nullable=False)
    response = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    record = relationship("Record", back_populates="updates")
