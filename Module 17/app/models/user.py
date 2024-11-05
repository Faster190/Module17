from app.backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, index=True)

    tasks = relationship("Task", back_populates="user")


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable
    print(CreateTable(User.__table__))
