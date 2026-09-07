"""Stock movement database queries."""

import sqlite3
from typing import Optional

from database.connection import get_connection
from schemas.inventory import InventoryItem, StockMovementRead


def create_stock_movement(
    product_id: int,
    quantity_change: int,
    reason: str,
    connection: Optional[sqlite3.Connection] = None,
) -> StockMovementRead:
    if connection is None:
        with get_connection() as connection:
            return create_stock_movement(
                product_id=product_id,
                quantity_change=quantity_change,
                reason=reason,
                connection=connection,
            )

    cursor = connection.execute(
        """
        INSERT INTO stock_movements (product_id, quantity_change, reason)
        VALUES (?, ?, ?)
        """,
        (product_id, quantity_change, reason),
    )

    row = connection.execute(
        """
        SELECT id, product_id, quantity_change, reason, created_at
        FROM stock_movements
        WHERE id = ?
        """,
        (cursor.lastrowid,),
    ).fetchone()

    return StockMovementRead(**dict(row))


def get_current_stock(
    product_id: int,
    connection: Optional[sqlite3.Connection] = None,
) -> int:
    if connection is None:
        with get_connection() as connection:
            return get_current_stock(product_id, connection)

    row = connection.execute(
        """
        SELECT COALESCE(SUM(quantity_change), 0) AS current_stock
        FROM stock_movements
        WHERE product_id = ?
        """,
        (product_id,),
    ).fetchone()

    return int(row["current_stock"])


def get_inventory() -> list[InventoryItem]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                products.id AS product_id,
                products.sku,
                products.name,
                products.reorder_level,
                COALESCE(SUM(stock_movements.quantity_change), 0) AS current_stock
            FROM products
            LEFT JOIN stock_movements
                ON stock_movements.product_id = products.id
            GROUP BY products.id
            ORDER BY products.id
            """
        ).fetchall()

    return [InventoryItem(**dict(row)) for row in rows]

def all_stock_movements() -> list[StockMovementRead]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, product_id, quantity_change, reason, created_at
            FROM stock_movements
            ORDER BY created_at DESC
            """
        ).fetchall()

    return [StockMovementRead(**dict(row)) for row in rows]
