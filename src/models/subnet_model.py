from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import Base


class Subnet(Base):
    __tablename__ = "subnets"

    id = Column(Integer, primary_key=True)
    subnet_id = Column(String(255), unique=True, nullable=False, index=True)
    vpc_id = Column(String(255), ForeignKey("vpcs.vpc_id", ondelete="CASCADE"), nullable=False, index=True)
    subnet_name = Column(String(255), nullable=False)
    cidr_block = Column(String(18), nullable=False)
    availability_zone = Column(String(50))
    created_by = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="active")

    vpc = relationship("VPC", back_populates="subnets")
