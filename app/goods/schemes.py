from pydantic import BaseModel
from datetime import datetime
from .models import Tag, Category



class CategoryScheme(BaseModel):
    id: int
    label: str
    slug: str
    notice: str
    description: str
    image: str
    goods: str
    works: str

class CategoryCreateScheme(BaseModel):
    label: str
    slug: str
    notice: str
    description: str
    image: str


class CategoryResponseScheme(BaseModel):
    id: int
    label: str
    slug: str
    notice: str
    description: str
    image: str


class TagScheme(BaseModel):
    id: int
    label: str
    slug: str

class TagCreateScheme(BaseModel):
    label: str
    slug: str


class WorkScheme(BaseModel):
    id: int
    label: str
    slug: str
    category_id: str
    image: str


class WorkCreateScheme(BaseModel):
    label: str
    slug: str
    category_id: str
    image: str

class GoodScheme(BaseModel):
    id: int
    type: str
    label: str
    slug: str
    price: int
    discount: int
    unit: str
    image: str
    create_date: datetime
    update_date: datetime
    category_id: int
    tag_id: int


class GoodCreateScheme(BaseModel):
    type: str
    label: str
    slug: str
    image: str
    price: int
    discount: int
    unit: str
    category_id: int
    tag_id: int


class GoodResponseScheme(BaseModel):
    id: int
    type: str
    label: str
    slug: str
    price: int
    discount: int
    unit: str
    image: str
    create_date: datetime
    update_date: datetime
    category_id: int
    tag_id: int
    category: CategoryScheme
    tag: TagScheme



