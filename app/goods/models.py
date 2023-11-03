from app.root.models import Base, BaseWithImage, BaseWithSlug
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime


class Good(BaseWithImage, BaseWithSlug):
    __tablename__ = 'good'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    type = Column(String, default='service')
    label = Column(String(100), nullable=False)
    price = Column(DECIMAL, nullable=False)
    discount = Column(DECIMAL, default=0)
    unit = Column(String, nullable=False)
    create_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    update_date = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = Column(Integer, ForeignKey('category.id'), default='0')
    tag_id = Column(Integer, ForeignKey('tag.id'), default='0')
    category = relationship('Category', back_populates='goods')
    tag = relationship('Tag', back_populates='goods')


class Category(BaseWithImage, BaseWithSlug):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    label = Column(String(100), nullable=False)
    notice = Column(String, default='')
    description = Column(String, nullable=False)
    goods = relationship('Good', back_populates='category')
    works = relationship('Work', back_populates='category')


class Tag(BaseWithSlug):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    label = Column(String(100), nullable=False)
    goods = relationship('Good', back_populates='tag')


class Work(BaseWithImage, BaseWithSlug):
    __tablename__ = 'work'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    label = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='works')
