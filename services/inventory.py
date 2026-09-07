"""Inventory business logic."""

from database.connection import get_connection
from repositories import products as product_repository
from repositories import stock_movements as stock_movement_repository
from schemas.inventory import InventoryItem, StockMovementCreate, StockMovementRead


class ProductNotFoundError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


class InvalidStockMovementError(Exception):
    pass


def create_stock_movement(movement: StockMovementCreate) -> StockMovementRead:
    if movement.quantity_change == 0:
        raise InvalidStockMovementError("Quantity change cannot be zero.")

    with get_connection() as connection:
        product = product_repository.get_product_by_sku(movement.sku, connection)
        if product is None:
            raise ProductNotFoundError(
                f"Product with SKU '{movement.sku}' was not found."
            )

        current_stock = stock_movement_repository.get_current_stock(
            product.id,
            connection,
        )
        new_stock = current_stock + movement.quantity_change

        if new_stock < 0:
            raise InsufficientStockError(
                f"Cannot apply movement. Current stock is {current_stock}, "
                f"but change was {movement.quantity_change}."
            )

        return stock_movement_repository.create_stock_movement(
            product_id=product.id,
            quantity_change=movement.quantity_change,
            reason=movement.reason,
            connection=connection,
        )


def get_inventory() -> list[InventoryItem]:
    return stock_movement_repository.get_inventory()


def get_low_stock_inventory() -> list[InventoryItem]:
    inventory = get_inventory()
    return [
        item
        for item in inventory
        if item.current_stock <= item.reorder_level
    ]


def get_all_stock_movements() -> list[StockMovementRead]:
    return stock_movement_repository.get_all_stock_movements()
