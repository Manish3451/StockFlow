"""Product request and response schemas."""

from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    sku: str = Field(min_length=1)
    name: str = Field(min_length=1)
    reorder_level: int = Field(ge=0)


class ProductRead(ProductCreate):
    id: int
    created_at: str


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    reorder_level: Optional[int] = Field(default=None, ge=0)
