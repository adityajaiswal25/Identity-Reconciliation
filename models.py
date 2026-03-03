from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from database import Base, engine

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    linkedId = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    linkPrecedence = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow)
    deletedAt = Column(DateTime, nullable=True)

Base.metadata.create_all(bind=engine)