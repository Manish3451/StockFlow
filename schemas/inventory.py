"""Inventory request and response schemas."""

from pydantic import BaseModel, Field


class StockMovementCreate(BaseModel):
    sku: str = Field(min_length=1)
    quantity_change: int
    reason: str = Field(min_length=1)


class StockMovementRead(BaseModel):
    id: int
    product_id: int
    quantity_change: int
    reason: str
    created_at: str


class InventoryItem(BaseModel):
    product_id: int
    sku: str
    name: str
    reorder_level: int
    current_stock: int
