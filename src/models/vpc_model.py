from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import Base


class VPC(Base):
    __tablename__ = "vpcs"

    id = Column(Integer, primary_key=True)
    vpc_id = Column(String(255), unique=True, nullable=False, index=True)
    vpc_name = Column(String(255), nullable=False)
    cidr_block = Column(String(18), nullable=False)
    region = Column(String(50), nullable=False)
    created_by = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="active")

    subnets = relationship("Subnet", back_populates="vpc", cascade="all, delete-orphan")


