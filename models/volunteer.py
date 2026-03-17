from sqlalchemy import Column, Integer, String
from database.db import Base


class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    phone = Column(String(20), nullable=True)
    specialization = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Volunteer(id={self.id}, name='{self.name}', specialization='{self.specialization}')>"