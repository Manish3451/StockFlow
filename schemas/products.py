"""Product request and response schemas."""

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    sku: str = Field(min_length=1)
    name: str = Field(min_length=1)
    reorder_level: int = Field(ge=0)


class ProductRead(ProductCreate):
    id: int
    created_at: str
