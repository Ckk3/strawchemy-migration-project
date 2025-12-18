import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.orm import relationship

from database import Base


class Department(Base):
    __tablename__ = "department"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)

    employees = relationship("Employee", back_populates="department")


class Employee(Base):
    __tablename__ = "employee"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    department_id = Column(CHAR(36), ForeignKey("department.id"))

    department = relationship("Department", back_populates="employees")
