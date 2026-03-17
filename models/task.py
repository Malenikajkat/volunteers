from sqlalchemy import Column, Integer, String, Text, DateTime
from database.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=False)
    required_volunteers = Column(Integer, default=1, nullable=False)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', deadline={self.deadline})>"