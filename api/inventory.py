"""Inventory HTTP routes."""

from fastapi import APIRouter, HTTPException, status

from schemas.inventory import InventoryItem, StockMovementCreate, StockMovementRead
from services.inventory import (
    InvalidStockMovementError,
    InsufficientStockError,
    ProductNotFoundError,
    create_stock_movement,
    get_all_stock_movements,
    get_inventory,
    get_low_stock_inventory,
)


router = APIRouter(tags=["inventory"])


@router.post(
    "/stock-movements",
    response_model=StockMovementRead,
    status_code=status.HTTP_201_CREATED,
)
def create_stock_movement_route(movement: StockMovementCreate) -> StockMovementRead:
    try:
        return create_stock_movement(movement)
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except InvalidStockMovementError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except InsufficientStockError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.get("/inventory", response_model=list[InventoryItem])
def get_inventory_route() -> list[InventoryItem]:
    return get_inventory()


@router.get("/inventory/low-stock", response_model=list[InventoryItem])
def get_low_stock_inventory_route() -> list[InventoryItem]:
    return get_low_stock_inventory()


@router.get("/stock-movements", response_model=list[StockMovementRead])
def get_all_stock_movements_route() -> list[StockMovementRead]:
    return get_all_stock_movements()
