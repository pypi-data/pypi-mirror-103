from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)

    children = relationship("Child", cascade="all, delete")
    car = relationship("Car", cascade="all, delete", uselist=False, back_populates="owner")


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)

    popsicles = relationship("Popsicle", cascade="all, delete")


class Popsicle(Base):
    __tablename__ = "popsicles"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    flavor = Column(String, nullable=False)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    color = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("parents.id"), nullable=False)

    owner = relationship("Parent", back_populates="car")
