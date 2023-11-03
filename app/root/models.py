import shutil
from fastapi import UploadFile
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy import Column, Integer, String
import slugify


class Base(DeclarativeBase):
    pass


class BaseWithImage(Base):
    __abstract__ = True
    image = Column(String, default='', nullable=True)

    def save_image(self, image_file: UploadFile):
        image_path = f"images/{self.slug}.jpg"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
        self.image = image_path
        return self


class BaseWithSlug(Base):
    __abstract__ = True
    slug: Mapped[str] = Column(String(50), nullable=False, default='', unique=True, index=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.slug == '':
            self.slug = slugify(self.label)[0:50]
