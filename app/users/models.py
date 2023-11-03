from app.root.models import Base, BaseWithImage, BaseWithSlug
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime


class User(BaseWithImage):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship('Role', back_populates="users")
    register_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_visit = Column(DateTime(timezone=True), default=datetime.utcnow)
    disabled = Column(Boolean, default=False)


class Role(BaseWithSlug):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(50), nullable=False)
    permissions = Column(ARRAY(String), default=[])
    users = relationship('User', back_populates="role")