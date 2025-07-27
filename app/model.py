from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Posts(Base):
    __tablename__="Posts"
    id=Column(Integer,primary_key=True, nullable=False,index=True)
    content=Column(String)
    owner_id = Column(Integer, ForeignKey("User.id"))

    owner = relationship("User", back_populates="notes")


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True,  nullable=False,index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    username = Column(String(50), nullable=False)
    password = Column(String, nullable=False)

    notes = relationship("Posts", back_populates="owner")
    


    